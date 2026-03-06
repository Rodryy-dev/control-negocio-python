import sqlite3

def crear_base_de_datos():
    # Conecta a la base de datos (se creará el archivo si no existe)
    conexion = sqlite3.connect('negocio.db')
    cursor = conexion.cursor()

    # 1. Tabla de Categorías
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categorias (
            id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT
        )
    ''')

    # 2. Tabla de Proveedores
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS proveedores (
            id_proveedor INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            contacto TEXT,
            telefono TEXT
        )
    ''')

    # 3. Tabla de Productos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio_compra REAL NOT NULL,
            precio_venta REAL NOT NULL,
            stock_actual INTEGER DEFAULT 0,
            id_categoria INTEGER,
            id_proveedor INTEGER,
            FOREIGN KEY (id_categoria) REFERENCES categorias (id_categoria),
            FOREIGN KEY (id_proveedor) REFERENCES proveedores (id_proveedor)
        )
    ''')

    # 4. Tabla de Entradas y Salidas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movimientos (
            id_movimiento INTEGER PRIMARY KEY AUTOINCREMENT,
            id_producto INTEGER,
            tipo TEXT CHECK(tipo IN ('ENTRADA', 'SALIDA')),
            cantidad INTEGER NOT NULL,
            precio_aplicado REAL NOT NULL,
            fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_producto) REFERENCES productos (id_producto)
        )
    ''')

    # 5. Tabla de Gastos Extra
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gastos_extra (
            id_gasto INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion TEXT NOT NULL,
            monto REAL NOT NULL,
            fecha DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conexion.commit()
    conexion.close()
    print("¡Base de datos y tablas creadas con éxito en 'negocio.db'!")

if __name__ == "__main__":
    crear_base_de_datos()
