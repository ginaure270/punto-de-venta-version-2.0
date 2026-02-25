# Punto de Venta (Desktop POS)

## Preview
![Inicio](assets/2026-02-25_08-10-25.png)
![Ventas](assets/2026-02-25_08-12-02.png)
![Inventario](assets/2026-02-25_08-12-25.png)
![Inventario Admin](assets/2026-02-25_08-12-46.png)

## Overview | Descripción
| English | Español |
| --- | --- |
| - Desktop point-of-sale built with Tkinter/CustomTkinter on SQLite (`database_ventas.db`).<br>- Role-based access: standard users and admins (admins see the admin inventory view and get a welcome notice).<br>- Live USD rate from BCV via `pyBCV`; shows prices/totals in Bs while storing USD in DB. | - Sistema de punto de venta de escritorio con Tkinter/CustomTkinter y SQLite (`database_ventas.db`).<br>- Acceso por roles: usuarios y administradores (los admins ven el inventario de administración y reciben aviso de bienvenida).<br>- Toma la tasa USD del BCV con `pyBCV`; muestra precios/totales en Bs mientras guarda USD en la base. |

## Features | Funcionalidades
| English | Español |
| --- | --- |
| **Login & roles**<br>- Sample users: `admin/papo`, `Alejandro/cafe123`, `Danito/Danito`.<br>- Admins unlock the admin inventory view. | **Login y roles**<br>- Usuarios de ejemplo: `admin/papo`, `Alejandro/cafe123`, `Danito/Danito`.<br>- Los admins habilitan la vista de inventario admin. |
| **Home hub**<br>- Buttons to Sales, Inventory, Admin Inventory, Logout.<br>- USD rate tile with last-update label. | **Panel principal**<br>- Botones a Ventas, Inventario, Inventario Admin, Cerrar sesión.<br>- Tarjeta de tasa USD y etiqueta de última actualización. |
| **Weekly production chart**<br>- Matplotlib bar chart for the last 7 days of sales quantities (`ventas.fecha`). | **Gráfico semanal**<br>- Barras de los últimos 7 días con cantidades vendidas (`ventas.fecha`). |
| **Sales (Ventas)**<br>- Search with live suggestions by ID or name; Enter adds qty=1.<br>- Prices/totals shown in Bs (USD price x `usd_rate`).<br>- Stock validation and decrement on payment.<br>- Auto-incremented invoice numbers.<br>- Running total, clock widget, focus on search at open.<br>- Invoice viewer (loads `ventas`, shows amounts in Bs).<br>- Password-protected receipt PDF (default `recibo` or `recibo/password`).<br>- Migrate sales to `cierre` with password; clears `ventas` after migration. | **Ventas (Ventas)**<br>- Búsqueda con sugerencias por ID o nombre; Enter agrega cantidad=1.<br>- Precios/totales en Bs (precio USD x `usd_rate`).<br>- Valida stock y descuenta al cobrar.<br>- Numeración de factura auto-incremental.<br>- Total en pantalla, reloj, foco inicial en búsqueda.<br>- Visor de facturas (lee `ventas`, muestra montos en Bs).<br>- Recibo PDF protegido (clave `recibo` o `recibo/password`).<br>- Migrar ventas a `cierre` con contraseña; limpia `ventas` después. |
| **Inventory (Inventario)**<br>- List/search by ID or name; restock, add, modify, delete.<br>- Product image support (`imagenes_productos/<id>.jpg`) with preview; fallback `null.webp`.<br>- Stock/price changes persist to SQLite; ensures `inventario` exists on startup. | **Inventario (Inventario)**<br>- Lista/búsqueda por ID o nombre; reabastecer, añadir, modificar, borrar.<br>- Soporta imagen (`imagenes_productos/<id>.jpg`) con vista previa; respaldo `null.webp`.<br>- Cambios de stock/precio persisten en SQLite; asegura `inventario` al iniciar. |
| **Admin Inventory (Inventario_Admin)**<br>- Admin-only view with search, add, modify (dedicated window), delete, and preview. | **Inventario Admin (Inventario_Admin)**<br>- Vista solo admin con búsqueda, añadir, modificar (ventana dedicada), borrar y vista previa. |
| **Receipts & closure**<br>- `mover_cierre.py` groups `ventas` into `cierre` (by product and price), sums quantities, recalculates subtotals, then empties `ventas`.<br>- `generar_recibo_cierre.py` builds PDF from `cierre` and saves under Documents `recibos/<date>/`. | **Recibos y cierre**<br>- `mover_cierre.py` agrupa `ventas` en `cierre` (por producto y precio), suma cantidades, recalcula subtotales y limpia `ventas`.<br>- `generar_recibo_cierre.py` crea PDF desde `cierre` y lo guarda en Documentos `recibos/<fecha>/`. |
| **UI helpers**<br>- Custom buttons (`ctk_button.make_ctk_button`) and rounded fallback buttons (`widgets.py`). | **Utilidades UI**<br>- Botones personalizados (`ctk_button.make_ctk_button`) y botones redondeados de respaldo (`widgets.py`). |

## Dependencies | Dependencias
| English | Español |
| --- | --- |
| - Python 3.10+ (with `tkinter`/`python3-tk`).<br>- Pip packages: `customtkinter`, `Pillow`, `matplotlib`, `pyBCV`, `fpdf`, `streamlit`.<br>- Built-ins: `sqlite3`, `tkinter`, `webbrowser`, `os`, `datetime`. | - Python 3.10+ (con `tkinter`/`python3-tk`).<br>- Paquetes pip: `customtkinter`, `Pillow`, `matplotlib`, `pyBCV`, `fpdf`, `streamlit`.<br>- Incluidos: `sqlite3`, `tkinter`, `webbrowser`, `os`, `datetime`. |

## Setup | Instalación
| English | Español |
| --- | --- |
| - `python -m venv .venv`<br>- `source .venv/bin/activate` (Windows: `.venv\\Scripts\\activate`)<br>- `pip install --upgrade pip`<br>- `pip install customtkinter Pillow matplotlib pyBCV fpdf streamlit`<br>- If `tkinter` is missing on Linux: `sudo apt-get install python3-tk`. | - `python -m venv .venv`<br>- `source .venv/bin/activate` (Windows: `.venv\\Scripts\\activate`)<br>- `pip install --upgrade pip`<br>- `pip install customtkinter Pillow matplotlib pyBCV fpdf streamlit`<br>- Si falta `tkinter` en Linux: `sudo apt-get install python3-tk`. |

## Running | Ejecución
| English | Español |
| --- | --- |
| - `python index.py`<br>- Window adapts to your screen; dark-accent theme.<br>- SQLite tables auto-create on first run. | - `python index.py`<br>- Ventana se adapta a tu pantalla; tema oscuro.<br>- Las tablas SQLite se crean en el primer inicio. |

## Data & credentials | Datos y credenciales
| English | Español |
| --- | --- |
| - Database: `database_ventas.db` in repo root.<br>- Tables: `inventario`, `ventas`, `cierre` (created on first migration).<br>- Sample credentials: `admin/papo`, `Alejandro/cafe123`, `Danito/Danito` (admins: `admin`, `Danito`). | - Base: `database_ventas.db` en la raíz.<br>- Tablas: `inventario`, `ventas`, `cierre` (se crea en la primera migración).<br>- Credenciales de ejemplo: `admin/papo`, `Alejandro/cafe123`, `Danito/Danito` (admins: `admin`, `Danito`). |

## Receipts & passwords | Recibos y contraseñas
| English | Español |
| --- | --- |
| - Sales receipts need a password: default `recibo`, or override with `recibo/password` file.<br>- Closure receipts read company info from `recibo/` (`logo.pnj`, `nombre_empresa`, `rif`, `Ubicacion_empresa`). | - Los recibos de Ventas piden contraseña: por defecto `recibo`, o define otra en `recibo/password`.<br>- Los recibos de cierre leen datos de empresa desde `recibo/` (`logo.pnj`, `nombre_empresa`, `rif`, `Ubicacion_empresa`). |

## Project layout | Estructura
| English | Español |
| --- | --- |
| - `index.py` – launches login.<br>- `inicio.py` – login window, role flag.<br>- `manager.py` – main window host.<br>- `container.py` – home hub, USD tile, chart, navigation.<br>- `ventas.py` – sales UI, stock, invoicing, receipts, migration.<br>- `inventario.py` – inventory CRUD/restock with images.<br>- `inventario_admin.py` – admin inventory view.<br>- `conexion.py` – SQLite helpers and initialization.<br>- `recibo.py`, `generar_recibo_cierre.py`, `mover_cierre.py` – PDFs and closing.<br>- `imagenes_productos/` – product images; `imagenes/` – UI assets. | - `index.py` – arranque del login.<br>- `inicio.py` – ventana de login y rol.<br>- `manager.py` – ventana principal.<br>- `container.py` – panel inicial, tasa USD, gráfico, navegación.<br>- `ventas.py` – UI de ventas, stock, facturación, recibos, migración.<br>- `inventario.py` – CRUD/reabastecer inventario con imágenes.<br>- `inventario_admin.py` – vista de inventario para admins.<br>- `conexion.py` – helpers SQLite e inicialización.<br>- `recibo.py`, `generar_recibo_cierre.py`, `mover_cierre.py` – PDFs y cierre.<br>- `imagenes_productos/` – imágenes de productos; `imagenes/` – recursos de UI. |

## Tests | Pruebas
| English | Español |
| --- | --- |
| - `test_ctk.py` (button helper).<br>- `test_recibo_save.py` (receipt saving).<br>- Run: `python -m pytest` (install `pytest` if needed). | - `test_ctk.py` (botones).<br>- `test_recibo_save.py` (guardado de recibos).<br>- Ejecuta: `python -m pytest` (instala `pytest` si hace falta). |

## License | Licencia
| English | Español |
| --- | --- |
| - Apache 2.0 (`LICENSE`). | - Apache 2.0 (`LICENSE`). |
