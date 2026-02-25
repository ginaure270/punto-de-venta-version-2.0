import os
import streamlit as st
import datetime as dt
from fpdf import FPDF
from io import BytesIO
import sqlite3 as sql
import conexion as con


def _read_text_file(path):
	try:
		with open(path, 'r', encoding='utf-8') as f:
			return f.read().strip()
	except Exception:
		return ''


def read_company_info():
	"""Lee los archivos dentro de la carpeta `recibo` y devuelve un dict con los datos.

	Espera encontrar los archivos: logo.pnj, nombre_empresa, rif, Ubicacion_empresa
	"""
	base = os.path.join(os.path.dirname(__file__), 'recibo')
	info = {}
	info['logo'] = os.path.join(base, 'logo.pnj') if os.path.exists(os.path.join(base, 'logo.pnj')) else None
	info['nombre_empresa'] = _read_text_file(os.path.join(base, 'nombre_empresa'))
	info['rif'] = _read_text_file(os.path.join(base, 'rif'))
	info['ubicacion'] = _read_text_file(os.path.join(base, 'Ubicacion_empresa'))
	return info


def _safe_float(v):
	try:
		return float(v)
	except Exception:
		return 0.0


def generate_pdf_receipt(items, company_info=None, title='Recibo', date=None):
	"""Genera un PDF de recibo y devuelve bytes.

	items: lista de dicts con keys: id, producto, cantidad, precio
	company_info: dict con keys: logo, nombre_empresa, rif, ubicacion
	"""
	if company_info is None:
		company_info = read_company_info()

	if date is None:
		date = dt.datetime.now()

	pdf = FPDF(orientation='P', unit='mm', format='A4')
	pdf.add_page()

	# Logo
	if company_info.get('logo') and os.path.exists(company_info['logo']):
		try:
			pdf.image(company_info['logo'], x=10, y=8, w=30)
		except Exception:
			# imagen no compatible o error: ignorar
			pass

	pdf.set_font('Arial', 'B', 14)
	pdf.cell(0, 10, company_info.get('nombre_empresa', ''), ln=1, align='C')

	pdf.set_font('Arial', '', 10)
	if company_info.get('rif'):
		pdf.cell(0, 5, f"RIF: {company_info.get('rif')}", ln=1, align='C')
	if company_info.get('ubicacion'):
		pdf.cell(0, 5, company_info.get('ubicacion'), ln=1, align='C')

	pdf.ln(5)
	pdf.set_font('Arial', 'B', 12)
	pdf.cell(0, 8, title, ln=1, align='L')
	pdf.set_font('Arial', '', 9)
	pdf.cell(0, 6, f"Fecha: {date.strftime('%Y-%m-%d %H:%M:%S')}", ln=1)
	pdf.ln(4)

	# Table header
	col_widths = [15, 80, 25, 30, 30]  # ID, Producto, Cantidad, Precio, Subtotal
	headers = ['ID', 'Producto', 'Cantidad', 'Precio', 'Subtotal']
	pdf.set_font('Arial', 'B', 10)
	for w, h in zip(col_widths, headers):
		pdf.cell(w, 8, h, border=1, align='C')
	pdf.ln()

	pdf.set_font('Arial', '', 10)
	total = 0.0
	for it in items:
		pid = str(it.get('id', ''))
		producto = str(it.get('producto', ''))
		cantidad = _safe_float(it.get('cantidad', 0))
		precio = _safe_float(it.get('precio', 0))
		subtotal = cantidad * precio
		total += subtotal

		pdf.cell(col_widths[0], 7, pid, border=1)
		# producto: permitir que ocupe varias líneas si es largo
		pdf.multi_cell(col_widths[1], 7, producto, border=1)
		# multi_cell mueve el cursor a la siguiente línea; para mantener columnas alineadas,
		# simplificamos colocando las siguientes celdas en la misma altura aproximada.
		x_after = pdf.get_x()
		y_after = pdf.get_y()
		# volver al inicio de la fila para escribir cantidad, precio, subtotal en una nueva línea
		pdf.set_xy(pdf.l_margin + sum(col_widths[:2]), y_after - 7)
		pdf.cell(col_widths[2], 7, f"{cantidad:g}", border=1, align='C')
		pdf.cell(col_widths[3], 7, f"{precio:,.2f}", border=1, align='R')
		pdf.cell(col_widths[4], 7, f"{subtotal:,.2f}", border=1, align='R')
		pdf.ln()

	# Totals
	pdf.ln(2)
	pdf.set_font('Arial', 'B', 11)
	pdf.cell(sum(col_widths[:-1]), 8, 'TOTAL', border=1, align='R')
	pdf.cell(col_widths[-1], 8, f"{total:,.2f}", border=1, align='R')

	# Output as bytes
	out = pdf.output(dest='S')
	if isinstance(out, str):
		out = out.encode('latin-1')
	return out


def _sample_items():
	return [
		{'id': '001', 'producto': 'Camiseta', 'cantidad': 2, 'precio': 10.0},
		{'id': '002', 'producto': 'Pantalones', 'cantidad': 1, 'precio': 25.5},
		{'id': '003', 'producto': 'Gorra', 'cantidad': 3, 'precio': 5.75},
	]


def fetch_cierre_items(db_path=None):
	"""Lee las filas de la tabla `cierre` y devuelve una lista de dicts
	con las keys: id, producto, cantidad, precio.

	Si la tabla no existe o ocurre un error, devuelve lista vacía.
	"""
	if db_path is None:
		db_path = con.DB_PATH
	items = []
	try:
		conn = sql.connect(db_path)
		cur = conn.cursor()
		# Intentar seleccionar columnas comunes: ide, nombre_articulo, cantidad, valor_articulo
		cur.execute("SELECT ide, nombre_articulo, cantidad, valor_articulo FROM cierre")
		rows = cur.fetchall()
		for r in rows:
			# r may be tuple (ide, nombre_articulo, cantidad, valor_articulo)
			items.append({
				'id': r[0],
				'producto': r[1],
				'cantidad': r[2],
				'precio': r[3],
			})
	except sql.Error:
		# Si la tabla no tiene exactamente esas columnas, intentar seleccionar por orden genérico
		try:
			cur.execute("SELECT * FROM cierre")
			rows = cur.fetchall()
			cols = [c[0] for c in cur.description]
			# buscar índices de columnas esperadas
			idx_id = None
			idx_nombre = None
			idx_cantidad = None
			idx_valor = None
			for i, col in enumerate(cols):
				name = col.lower()
				if name in ('ide', 'id', 'rowid') and idx_id is None:
					idx_id = i
				if 'nombre' in name and idx_nombre is None:
					idx_nombre = i
				if 'cantidad' in name and idx_cantidad is None:
					idx_cantidad = i
				if 'valor' in name or 'precio' in name and idx_valor is None:
					idx_valor = i

			for r in rows:
				items.append({
					'id': r[idx_id] if idx_id is not None else '',
					'producto': r[idx_nombre] if idx_nombre is not None else '',
					'cantidad': r[idx_cantidad] if idx_cantidad is not None else 0,
					'precio': r[idx_valor] if idx_valor is not None else 0,
				})
		except Exception:
			# no se pudo leer la tabla cierre; devolver lista vacía
			items = []
	finally:
		try:
			conn.close()
		except Exception:
			pass
	return items


def total_from_items(items):
	t = 0.0
	for it in items:
		try:
			cantidad = float(it.get('cantidad', 0) or 0)
			precio = float(it.get('precio', 0) or 0)
			t += cantidad * precio
		except Exception:
			continue
	return t


def main():
	st.title('Generar recibo')
	info = read_company_info()
	st.write('Empresa: ', info.get('nombre_empresa', ''))
	st.write('RIF: ', info.get('rif', ''))
	st.write('Ubicación: ', info.get('ubicacion', ''))

	# Intentar leer los items desde la tabla `cierre`
	items = fetch_cierre_items()
	if not items:
		st.warning('No se encontraron registros en la tabla `cierre`. Mostrando ejemplo.')
		items = _sample_items()
		st.subheader('Items (ejemplo)')
		st.table(items)
	else:
		st.subheader('Items (desde tabla `cierre`)')
		st.table(items)
		total_vendido = total_from_items(items)
		st.markdown(f"**Total vendido:** {total_vendido:,.2f}")

	if st.button('Generar recibo PDF'):
		pdf_bytes = generate_pdf_receipt(items, company_info=info, title='Recibo de venta')
		# Guardar en Documents/recibos/<fecha_hoy>/
		try:
			saved_path = save_pdf_to_documents(pdf_bytes)
			st.success(f'Recibo generado y guardado en: {saved_path}')
		except Exception as e:
			st.error(f'Error al guardar recibo: {e}')
		st.download_button('Descargar recibo', data=pdf_bytes, file_name='recibo.pdf', mime='application/pdf')


if __name__ == '__main__':
	main()


def save_pdf_to_documents(pdf_bytes, filename=None):
	"""Guarda el PDF en la carpeta Documentos/recibos/<fecha_hoy>/ y devuelve la ruta absoluta.

	filename: opcional, si no se entrega se genera recibo_HHMMSS.pdf
	"""
	today = dt.datetime.now().strftime('%Y-%m-%d')
	home = os.path.expanduser('~')
	base_dir = os.path.join(home, 'Documents', 'recibos', today)
	os.makedirs(base_dir, exist_ok=True)
	if filename is None:
		ts = dt.datetime.now().strftime('%H%M%S')
		filename = f'recibo_{ts}.pdf'
	path = os.path.join(base_dir, filename)
	with open(path, 'wb') as f:
		f.write(pdf_bytes)
	return path


