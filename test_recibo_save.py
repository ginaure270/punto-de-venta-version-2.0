from recibo import generate_pdf_receipt, read_company_info, save_pdf_to_documents, _sample_items

if __name__ == '__main__':
    info = read_company_info()
    items = _sample_items()
    pdf = generate_pdf_receipt(items, company_info=info, title='Prueba de guardado')
    path = save_pdf_to_documents(pdf, filename='recibo.pdf')
    print('Saved to:', path)
