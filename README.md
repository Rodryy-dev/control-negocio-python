---

# Control de Ventas e Inventario (Python/SQLite)

Este proyecto es una aplicación de escritorio diseñada para la gestión integral de un negocio local en linux. El objetivo principal es centralizar la administración de productos y obtener métricas financieras precisas de manera sencilla y eficiente.

---

## Funciones principales

* **Gestión de Inventario**
* **Cálculo de Ganancia Neta**
* **Validaciones de Seguridad**
* **Interfaz Gráfica**

---

## Instalación en Linux Mint

El programa ha sido desarrollado y optimizado específicamente para el entorno **Linux Mint**.

### 1. Instalar dependencias

Asegúrese de contar con el paquete de Tkinter para Python 3 instalado en su sistema:

```
sudo apt install python3-tk

```

### 2. Inicializar Base de Datos

Ejecute el script de configuración para generar el archivo SQLite y la estructura de tablas inicial:

```
python3 database.py

```

### 3. Ejecutar Aplicación

Inicie la interfaz principal del sistema con el siguiente comando:

```
python3 interfaz.py

```

---

## Especificaciones Técnicas

* **Motor de Base de Datos**: Utiliza **SQLite**, almacenando toda la información localmente en el archivo `negocio.db` para facilitar su portabilidad y respaldo.
* **Seguridad de Datos**: El archivo de la base de datos está incluido en el `.gitignore` por motivos de privacidad, evitando la carga accidental de registros financieros reales al repositorio público.
* **Estructura del Código**: Se mantiene una separación estricta entre la lógica de funciones y la interfaz de usuario (GUI), lo que facilita el mantenimiento y la futura escalabilidad del proyecto.

---
