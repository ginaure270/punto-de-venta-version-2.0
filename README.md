# Punto de Venta (Desktop POS)

## Overview (English)
- Desktop point-of-sale built with Tkinter/CustomTkinter, focused on sales, inventory, and end-of-day closure, backed by SQLite (`database_ventas.db`).
- Multi-role access: standard users and admins (admins unlock the admin inventory view and receive an admin welcome notice).
- Uses live USD rate from BCV (via `pyBCV`) to show prices/totals in Bs while storing values in USD in the DB.

## Features
- **Login & roles:** Simple credential gate with sample users (`admin/papo`, `Alejandro/cafe123`, `Danito/Danito`). Admins gain access to the admin inventory view.
- **Home hub:** Buttons to Sales, Inventory, Admin Inventory, Logout, plus a USD rate tile and last-update label.
- **Weekly production chart:** Matplotlib bar chart for the last 7 days of sales quantities (reads `ventas.fecha`).
- **Sales module (`Ventas`):**
  - Product search with live suggestions by ID or name; Enter adds with quantity=1.
  - Displays prices and totals in Bs (multiplies stored USD price by `usd_rate`).
  - Validates stock before selling; decrements inventory on payment.
  - Invoice numbering auto-increments from the DB.
  - Shows running total; clock widget; focuses search box on open.
  - View invoices (loads from `ventas` table, shows amounts converted to Bs).
  - Generate receipt PDF (password-protected; default password "recibo" or value in `recibo/password`).
  - Migrate sales to closure (`cierre`) with password confirmation; clears `ventas` after migration.
- **Inventory module (`Inventario`):**
  - List/search by ID or name, restock selected item, add, modify, delete.
  - Each product can have an image (`imagenes_productos/<id>.jpg`), previewed on selection; fallback image `null.webp`.
  - Stock and price edits persist to SQLite; ensures `inventario` table exists on startup.
- **Admin Inventory (`Inventario_Admin`):**
  - Admin-only view with search, add, modify (opens dedicated window), delete, and image preview.
- **Receipts & closure:**
  - `mover_cierre.py` groups `ventas` into `cierre` (by product and price), sums quantities, recomputes subtotals, then empties `ventas`.
  - `generar_recibo_cierre.py` builds a PDF from `cierre` (via `recibo.generate_pdf_receipt`) and saves it in the user Documents folder under `recibos/<date>/`.
- **UI helpers:** Custom buttons (`ctk_button.make_ctk_button`), rounded fallback buttons (`widgets.py`).

## Dependencies
- Python 3.10+ (with `tkinter`/`python3-tk` available on your OS)
- Packages (install via pip): `customtkinter`, `Pillow`, `matplotlib`, `pyBCV`, `fpdf`, `streamlit`
- Built-ins: `sqlite3`, `tkinter`, `webbrowser`, `os`, `datetime`

## Setup
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install customtkinter Pillow matplotlib pyBCV fpdf streamlit
```
If `tkinter` is missing on Linux, install your distro package (e.g., `sudo apt-get install python3-tk`).

## Running
```bash
python index.py
```
The app adapts window size to your screen and uses a dark-accented theme. On first run, SQLite tables are created automatically.

## Data & credentials
- Database: `database_ventas.db` in the repo root.
- Tables: `inventario`, `ventas` (created/used by app), `cierre` (created on first migration).
- Sample credentials: `admin/papo`, `Alejandro/cafe123`, `Danito/Danito` (admins: `admin`, `Danito`).

## Receipts and passwords
- Sales receipts (from Sales view) require a password: default `recibo`, or override by creating `recibo/password` with the desired text.
- Closure receipts read company metadata from files under `recibo/` (`logo.pnj`, `nombre_empresa`, `rif`, `Ubicacion_empresa`).

## Project layout (key files)
- `index.py` – launches login.
- `inicio.py` – login window, role flag.
- `manager.py` – main window host.
- `container.py` – home hub, USD tile, chart, navigation.
- `ventas.py` – sales UI, stock check, invoicing, receipts, migration.
- `inventario.py` – inventory CRUD/restock with images.
- `inventario_admin.py` – admin inventory view.
- `conexion.py` – SQLite helpers and initialization.
- `recibo.py`, `generar_recibo_cierre.py`, `mover_cierre.py` – PDF generation and closing.
- `imagenes_productos/` – product images (optional); `imagenes/` – UI assets.

## Tests
- `test_ctk.py` (button helper), `test_recibo_save.py` (receipt saving). Run with `python -m pytest` (requires `pytest` if you install it).

## License
- Apache 2.0 (see `LICENSE`).


# Punto de Venta (Escritorio)

## Descripción (Español)
- Sistema de punto de venta de escritorio con Tkinter/CustomTkinter para ventas, inventario y cierre diario, usando SQLite (`database_ventas.db`).
- Acceso por roles: usuarios estándar y administradores (los admins ven el inventario de administración y reciben aviso de bienvenida).
- Usa la tasa USD del BCV (`pyBCV`) para mostrar precios/totales en Bs mientras almacena valores en USD en la base.

## Funcionalidades
- **Login y roles:** Credenciales de ejemplo (`admin/papo`, `Alejandro/cafe123`, `Danito/Danito`). Los admins habilitan el inventario de administración.
- **Panel principal:** Botones a Ventas, Inventario, Inventario Admin, Cerrar sesión; tarjeta de tasa USD y etiqueta de última actualización.
- **Gráfico semanal:** Barras de los últimos 7 días con cantidades vendidas (lee `ventas.fecha`).
- **Ventas (`Ventas`):**
  - Búsqueda con sugerencias por ID o nombre; Enter agrega con cantidad 1.
  - Muestra precios y totales en Bs (multiplica el precio USD por `usd_rate`).
  - Valida stock antes de vender; descuenta inventario al pagar.
  - Numeración de factura auto-incremental.
  - Total en pantalla; reloj; foco inicial en la barra de búsqueda.
  - Ver facturas (lee `ventas`, muestra montos en Bs).
  - Generar recibo PDF protegido (clave "recibo" por defecto o la de `recibo/password`).
  - Migrar ventas a cierre con contraseña; vacía `ventas` tras migrar.
- **Inventario (`Inventario`):**
  - Lista/búsqueda por ID o nombre, reabastecer seleccionado, añadir, modificar, borrar.
  - Cada producto puede tener imagen (`imagenes_productos/<id>.jpg`); vista previa con respaldo `null.webp`.
  - Persistencia en SQLite; garantiza la tabla `inventario` al iniciar.
- **Inventario Admin (`Inventario_Admin`):**
  - Vista solo admin con búsqueda, añadir, modificar (ventana dedicada), borrar e imagen previa.
- **Recibos y cierre:**
  - `mover_cierre.py` agrupa `ventas` en `cierre` (por producto y precio), suma cantidades, recalcula subtotales y luego limpia `ventas`.
  - `generar_recibo_cierre.py` genera PDF desde `cierre` y lo guarda en Documentos/`recibos/<fecha>/`.
- **Utilidades UI:** Botones personalizados (`ctk_button.make_ctk_button`) y botones redondeados de reserva (`widgets.py`).

## Dependencias
- Python 3.10+ (con `tkinter`/`python3-tk` disponible en tu SO)
- Paquetes via pip: `customtkinter`, `Pillow`, `matplotlib`, `pyBCV`, `fpdf`, `streamlit`
- Incluidos en Python: `sqlite3`, `tkinter`, `webbrowser`, `os`, `datetime`

## Instalación
```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install customtkinter Pillow matplotlib pyBCV fpdf streamlit
```
Si falta `tkinter` en Linux, instala el paquete de tu distro (ej.: `sudo apt-get install python3-tk`).

## Ejecución
```bash
python index.py
```
La ventana se adapta a tu pantalla y usa tema oscuro. En el primer inicio se crean automáticamente las tablas SQLite.

## Datos y credenciales
- Base: `database_ventas.db` en la raíz.
- Tablas: `inventario`, `ventas` (creadas/usadas por la app), `cierre` (se crea en la primera migración).
- Credenciales de ejemplo: `admin/papo`, `Alejandro/cafe123`, `Danito/Danito` (admins: `admin`, `Danito`).

## Recibos y contraseñas
- Los recibos desde Ventas piden contraseña: por defecto `recibo`, o define otra en `recibo/password`.
- Los datos de la empresa para recibos de cierre se leen de archivos en `recibo/` (`logo.pnj`, `nombre_empresa`, `rif`, `Ubicacion_empresa`).

## Estructura (archivos clave)
- `index.py` – arranque del login.
- `inicio.py` – ventana de login y rol.
- `manager.py` – ventana principal.
- `container.py` – panel inicial, tasa USD, gráfico, navegación.
- `ventas.py` – UI de ventas, stock, facturación, recibos, migración.
- `inventario.py` – CRUD/reabastecer inventario con imágenes.
- `inventario_admin.py` – vista de inventario para admins.
- `conexion.py` – helpers SQLite e inicialización.
- `recibo.py`, `generar_recibo_cierre.py`, `mover_cierre.py` – PDFs y cierre.
- `imagenes_productos/` – imágenes opcionales; `imagenes/` – recursos de UI.

## Pruebas
- `test_ctk.py` (botones) y `test_recibo_save.py` (guardado de recibos). Ejecuta con `python -m pytest` (requiere `pytest` si lo instalas).

## Licencia
- Apache 2.0 (ver `LICENSE`).
