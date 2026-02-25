import sqlite3 as sql
from conexion import DB_PATH

def migrar_ventas_a_cierre(db_path=DB_PATH):
    """Elimina los datos de la tabla `cierre` y mueve los datos de `ventas` a `cierre`.

    - Agrupa por `nombre_articulo` y `valor_articulo`.
    - Suma la columna `cantidad`.
    - Mantiene `valor_articulo` tal cual.
    - Calcula `subtotal = cantidad * valor_articulo`.
    - Intenta mantener una columna identificadora `ide` usando MIN(pk) o MIN(rowid).
    """
    conn = sql.connect(db_path)
    conn.row_factory = sql.Row
    cur = conn.cursor()
    try:
        ventas_info = cur.execute("PRAGMA table_info(ventas)").fetchall()
        if not ventas_info:
            raise RuntimeError("La tabla 'ventas' no existe en la base de datos especificada.")

        ventas_cols = [r[1] for r in ventas_info]
        pk_cols = [r[1] for r in ventas_info if r[5] == 1]
        pk_col = pk_cols[0] if pk_cols else None

        # Si no existe la tabla cierre, la creamos con la misma estructura de `ventas` (tipos y pk donde aplique)
        cierre_info = cur.execute("PRAGMA table_info(cierre)").fetchall()
        if not cierre_info:
            cols_defs = []
            for r in ventas_info:
                name = r[1]
                typ = r[2] if r[2] else 'TEXT'
                pk = ' PRIMARY KEY' if r[5] == 1 else ''
                cols_defs.append(f"{name} {typ}{pk}")
            create_sql = "CREATE TABLE cierre (" + ", ".join(cols_defs) + ")"
            cur.execute(create_sql)

        # Eliminar datos existentes en cierre
        cur.execute("DELETE FROM cierre")

        # Preparar consulta de agrupación
        group_cols = ['nombre_articulo', 'valor_articulo']
        select_parts = []
        if pk_col:
            select_parts.append(f"MIN({pk_col}) AS ide")
        else:
            select_parts.append("MIN(rowid) AS ide")
        if 'factura' in ventas_cols:
            select_parts.append('MIN(factura) AS factura')
        select_parts += ['nombre_articulo', 'valor_articulo', 'SUM(cantidad) AS cantidad']

        agg_sql = "SELECT " + ", ".join(select_parts) + " FROM ventas GROUP BY " + ", ".join(group_cols)
        rows = cur.execute(agg_sql).fetchall()

        # Obtener columnas actuales de cierre para construir el INSERT dinámicamente
        cierre_info = cur.execute("PRAGMA table_info(cierre)").fetchall()
        cierre_cols = [r[1] for r in cierre_info]

        # Orden preferido de columnas para insertar
        preferred = ['ide', 'factura', 'nombre_articulo', 'valor_articulo', 'cantidad', 'subtotal']
        insert_cols = [c for c in preferred if c in cierre_cols]

        if not insert_cols:
            raise RuntimeError("La tabla 'cierre' no tiene columnas esperadas para insertar (ide/factura/nombre_articulo/valor_articulo/cantidad/subtotal).")

        insert_sql = f"INSERT INTO cierre ({', '.join(insert_cols)}) VALUES ({', '.join(['?']*len(insert_cols))})"

        inserted = 0
        for r in rows:
            ide = r['ide'] if 'ide' in r.keys() else None
            factura = r['factura'] if 'factura' in r.keys() else None
            nombre = r['nombre_articulo']
            valor = r['valor_articulo']
            cantidad_total = r['cantidad']
            subtotal = (valor or 0) * (cantidad_total or 0)

            vals = []
            for col in insert_cols:
                if col == 'ide':
                    vals.append(ide)
                elif col == 'factura':
                    vals.append(factura)
                elif col == 'nombre_articulo':
                    vals.append(nombre)
                elif col == 'valor_articulo':
                    vals.append(valor)
                elif col == 'cantidad':
                    vals.append(cantidad_total)
                elif col == 'subtotal':
                    vals.append(subtotal)
                else:
                    vals.append(None)

            cur.execute(insert_sql, vals)
            inserted += 1

        # Vaciar la tabla `ventas` después de migrar exitosamente los datos agrupados
        cur.execute("DELETE FROM ventas")

        conn.commit()
        return {'migrated': inserted, 'ventas_emptied': True}

    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == '__main__':
    try:
        resultado = migrar_ventas_a_cierre()
        print('Migración completada:', resultado)
    except Exception as err:
        print('Error durante la migración:', err)
