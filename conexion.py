import sqlite3 as sql

# Conexiones y adaptadores para usar la base de datos de ventas
# Esta versión hace que las funciones de inventario trabajen sobre
# la base `database_ventas.db` y mapeen la tabla `inventario` a la
# estructura que espera la UI (id, nombre, cantidad, precio).

DB_PATH = "database_ventas.db"

def buscar_producto(nombre):
    """Devuelve filas con la forma (id, nombre, cantidad, precio).
    Mapea la tabla `inventario` (rowid, nombre, stock, precio) a ese esquema.
    """
    conn = sql.connect(DB_PATH)
    cursor = conn.cursor()
    # Si la tabla tiene columna 'ide' preferimos devolverla como id, si no, usamos rowid
    cursor.execute("SELECT COALESCE(ide, rowid) as id, nombre, stock, precio FROM inventario WHERE nombre LIKE ?", ('%' + nombre + '%',))
    resultados = cursor.fetchall()
    conn.close()
    return resultados


def buscar_por_id_o_nombre(term):
    """Busca por ide, rowid o por nombre usando LIKE.
    Devuelve filas en la forma (id, nombre, stock, precio).
    """
    conn = sql.connect(DB_PATH)
    cursor = conn.cursor()
    if term is None:
        term = ""
    like_term = '%' + term + '%'
    # Intentamos buscar por ide exacto, por rowid exacto o por nombre LIKE
    try:
        cursor.execute(
            "SELECT COALESCE(ide, rowid) as id, nombre, stock, precio FROM inventario WHERE ide = ? OR rowid = ? OR nombre LIKE ?",
            (term, term, like_term)
        )
    except Exception:
        # En caso de cualquier problema, caer a búsqueda por nombre
        cursor.execute("SELECT COALESCE(ide, rowid) as id, nombre, stock, precio FROM inventario WHERE nombre LIKE ?", (like_term,))

    resultados = cursor.fetchall()
    conn.close()
    return resultados

def anadir_producto(nombre, cantidad, precio, ide=None):
    """Inserta en la tabla `inventario` y devuelve el id (rowid).

    Si `ide` se proporciona, lo guarda en la columna `ide`. Si la columna
    `ide` no existe, la crea automáticamente.
    """
    if ide is None or str(ide).strip() == '':
        raise ValueError('El campo "ide" es obligatorio.')

    conn = sql.connect(DB_PATH)
    cursor = conn.cursor()
    # comprobar duplicado de ide
    try:
        cursor.execute("SELECT 1 FROM inventario WHERE ide = ? LIMIT 1", (ide,))
        if cursor.fetchone():
            conn.close()
            raise ValueError(f"Ya existe un producto con ide '{ide}'")
    except sql.Error:
        # si la tabla no existe aún, continuar
        pass
    # Verificar si la columna 'ide' existe; si no, añadirla
    cols = [r[1] for r in cursor.execute("PRAGMA table_info(inventario)").fetchall()]
    if 'ide' in cols:
        cursor.execute("INSERT INTO inventario (ide, nombre, stock, precio) VALUES (?, ?, ?, ?)", (ide, nombre, cantidad, precio))
    else:
        # Añadir la columna 'ide' y luego insertar (sqlite permite ADD COLUMN)
        try:
            cursor.execute("ALTER TABLE inventario ADD COLUMN ide TEXT")
            conn.commit()
        except Exception:
            # si falla (por ejemplo la tabla no existe), continuar
            pass
        cursor.execute("INSERT INTO inventario (ide, nombre, stock, precio) VALUES (?, ?, ?, ?)", (ide, nombre, cantidad, precio))

    conn.commit()
    id_producto = cursor.lastrowid
    conn.close()
    return id_producto


def borrar_producto(id_producto):
    conn = sql.connect(DB_PATH)
    cursor = conn.cursor()
    # borrar por ide o por rowid
    cursor.execute("DELETE FROM inventario WHERE ide = ? OR rowid = ?", (id_producto, id_producto))
    conn.commit()
    conn.close()

def modificar_producto(id_producto, nombre, cantidad, precio, ide=None):
    """Modifica un producto. `id_producto` puede ser el valor de `ide` o el `rowid`.
    Si `ide` se entrega, también actualiza la columna `ide`.
    """
    conn = sql.connect(DB_PATH)
    cursor = conn.cursor()
    # Asegurar que la columna 'ide' exista
    cols = [r[1] for r in cursor.execute("PRAGMA table_info(inventario)").fetchall()]
    if 'ide' not in cols:
        try:
            cursor.execute("ALTER TABLE inventario ADD COLUMN ide TEXT")
            conn.commit()
        except Exception:
            pass

    if ide is not None:
        cursor.execute("UPDATE inventario SET ide=?, nombre=?, stock=?, precio=? WHERE ide = ? OR rowid = ?", (ide, nombre, cantidad, precio, id_producto, id_producto))
    else:
        cursor.execute("UPDATE inventario SET nombre=?, stock=?, precio=? WHERE ide = ? OR rowid = ?", (nombre, cantidad, precio, id_producto, id_producto))

    conn.commit()
    conn.close()

def inicializar_base_datos():
    """Inicializa la base de datos si no existe."""
    conn = sql.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("CREATE TABLE IF NOT EXISTS inventario (ide TEXT, nombre TEXT, stock INTEGER, precio REAL)")
        conn.commit()
    except sql.Error as e:
        print(f"Error al inicializar la base de datos: {e}")
    finally:
        conn.close()

# Llamar a la inicialización al importar el módulo
inicializar_base_datos()