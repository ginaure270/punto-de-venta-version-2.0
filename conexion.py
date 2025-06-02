#Contribution by SJLS27

import sqlite3 as sql 
#conexion con sqlote

def buscar_producto(nombre):
    conn = sql.connect("inventario.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE nombre LIKE ?", ('%' + nombre + '%',))
    resultados = cursor.fetchall()
    conn.close()
    return resultados
#entrada a sqlote
def anadir_producto(nombre, cantidad, precio):
    conn = sql.connect("inventario.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO productos (nombre, cantidad, precio) VALUES (?, ?, ?)", (nombre, cantidad, precio))
    conn.commit()
    conn.close()


def borrar_producto(id_producto):
    conn = sql.connect("inventario.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
    conn.commit()
    conn.close()

def modificar_producto(id_producto, nombre, cantidad, precio):
    conn = sql.connect("inventario.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE productos SET nombre=?, cantidad=?, precio=? WHERE id=?", (nombre, cantidad, precio, id_producto))
    conn.commit()
    conn.close()
