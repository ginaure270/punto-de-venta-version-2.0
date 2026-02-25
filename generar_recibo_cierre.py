"""Script sencillo para generar un recibo (PDF) usando los datos de la tabla `cierre`.

Uso:
    python generar_recibo_cierre.py

El script leerá los registros de `cierre`, calculará el total vendido, generará
un PDF con `recibo.generate_pdf_receipt` y lo guardará en `Documents/recibos/<fecha>/`.
"""
from recibo import generate_pdf_receipt, read_company_info, save_pdf_to_documents, fetch_cierre_items
import sys


def generate_and_save_receipt(filename=None):
    """Genera el recibo usando la tabla `cierre` y lo guarda. Devuelve la ruta del archivo guardado.

    Si `filename` es None, genera un nombre único basado en la fecha y hora
    para evitar sobrescribir recibos anteriores (ej. `recibo_2025-11-19_153012.pdf`).

    Lanza RuntimeError si no hay registros para generar.
    """
    info = read_company_info()
    items = fetch_cierre_items()

    if not items:
        raise RuntimeError('No se encontraron registros en la tabla `cierre`.')

    pdf_bytes = generate_pdf_receipt(items, company_info=info, title='Cierre de ventas')
    # Generar nombre de archivo único si no se proporcionó uno
    if not filename:
        from datetime import datetime
        ts = datetime.now().strftime('%Y-%m-%d_%H%M%S')
        filename = f'recibo_cierre_{ts}.pdf'

    path = save_pdf_to_documents(pdf_bytes, filename=filename)
    return path


def main():
    try:
        path = generate_and_save_receipt()
        print('Recibo generado y guardado en:', path)
    except RuntimeError as e:
        print('Error:', e)
        sys.exit(1)


if __name__ == '__main__':
    main()
