import sqlite3

def conectar():
    return sqlite3.connect('negocio.db')

def registrar_categoria(nombre, descripcion=""):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO categorias (nombre, descripcion) VALUES (?, ?)", (nombre, descripcion))
    conn.commit()
    conn.close()
    print(f"Categoría '{nombre}' registrada.")

def registrar_producto(nombre, p_compra, p_venta, stock_inicial, id_cat, id_prov):
    conn = conectar()
    cursor = conn.cursor()
    # Insertar el producto
    cursor.execute("""
        INSERT INTO productos (nombre, precio_compra, precio_venta, stock_actual, id_categoria, id_proveedor)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (nombre, p_compra, p_venta, stock_inicial, id_cat, id_prov))
    
    id_nuevo = cursor.lastrowid
    
    # Registrar el stock inicial como una ENTRADA en el historial de movimientos
    if stock_inicial > 0:
        cursor.execute("""
            INSERT INTO movimientos (id_producto, cantidad, tipo, precio_aplicado)
            VALUES (?, ?, 'ENTRADA', ?)
        """, (id_nuevo, stock_inicial, p_compra))
    
    conn.commit()
    conn.close()
    print(f"Producto '{nombre}' registrado con historial de inversión.")

def registrar_movimiento(id_prod, cantidad, tipo, precio_actual):
    """
    tipo: 'ENTRADA' o 'SALIDA'
    """
    conn = conectar()
    cursor = conn.cursor()
    
    # Registrar el movimiento en el historial
    cursor.execute("""
        INSERT INTO movimientos (id_producto, cantidad, tipo, precio_aplicado)
        VALUES (?, ?, ?, ?)
    """, (id_prod, cantidad, tipo, precio_actual))
    
    # Actualizar el stock en la tabla productos
    if tipo == 'ENTRADA':
        cursor.execute("UPDATE productos SET stock_actual = stock_actual + ? WHERE id_producto = ?", (cantidad, id_prod))
    else:
        cursor.execute("UPDATE productos SET stock_actual = stock_actual - ? WHERE id_producto = ?", (cantidad, id_prod))
    
    conn.commit()
    conn.close()
    print(f"Movimiento de {tipo} registrado.")

def registrar_gasto(descripcion, monto):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO gastos_extra (descripcion, monto) VALUES (?, ?)", (descripcion, monto))
    conn.commit()
    conn.close()
    print("Gasto registrado correctamente.")

def obtener_resumen_financiero():
    conn = conectar()
    cursor = conn.cursor()

    # Ingresos por ventas realizadas
    cursor.execute("SELECT SUM(cantidad * precio_aplicado) FROM movimientos WHERE tipo = 'SALIDA'")
    ingresos = cursor.fetchone()[0] or 0.0

    # Total invertido en compras (Entradas de stock)
    # Aquí contamos todo lo que has pagado por mercadería hasta hoy
    cursor.execute("""
        SELECT SUM(m.cantidad * p.precio_compra) 
        FROM movimientos m 
        JOIN productos p ON m.id_producto = p.id_producto 
        WHERE m.tipo = 'ENTRADA'
    """)
    total_compras = cursor.fetchone()[0] or 0.0

    # Gastos operativos (Luz, internet, pasajes)
    cursor.execute("SELECT SUM(monto) FROM gastos_extra")
    gastos_operativos = cursor.fetchone()[0] or 0.0

    # Ganancia Real = Lo que entró - (Todo lo que salió por productos + Gastos)
    ganancia_neta = ingresos - (total_compras + gastos_operativos)

    conn.close()

    return {
        "ingresos": ingresos,
        "total_compras": total_compras,
        "gastos_extra": gastos_operativos,
        "ganancia_neta": ganancia_neta
    }

def obtener_productos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.id_producto, p.nombre, c.nombre, p.precio_compra, p.precio_venta, p.stock_actual 
        FROM productos p
        LEFT JOIN categorias c ON p.id_categoria = c.id_categoria
    """)
    productos = cursor.fetchall()
    conn.close()
    return productos

def obtener_categorias():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id_categoria, nombre FROM categorias")
    cats = cursor.fetchall()
    conn.close()
    return cats

def eliminar_producto(id_prod):
    conn = conectar()
    cursor = conn.cursor()
    # Primero eliminamos los movimientos asociados para evitar errores de integridad
    cursor.execute("DELETE FROM movimientos WHERE id_producto = ?", (id_prod,))
    cursor.execute("DELETE FROM productos WHERE id_producto = ?", (id_prod,))
    conn.commit()
    conn.close()
    print(f"Producto {id_prod} eliminado.")

def eliminar_categoria(id_cat):
    conn = conectar()
    cursor = conn.cursor()
    # Nota: Esto fallará si hay productos usando esta categoría.
    cursor.execute("DELETE FROM categorias WHERE id_categoria = ?", (id_cat,))
    conn.commit()
    conn.close()

def obtener_productos_por_categoria(id_cat):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT nombre FROM productos WHERE id_categoria = ?", (id_cat,))
    productos = cursor.fetchall()
    conn.close()
    # Retornamos una lista simple de nombres: ['Producto A', 'Producto B']
    return [p[0] for p in productos]
