import pandas as pd
from PyPDF2 import PdfFileWriter, PdfFileReader
import os
import json
from Receipts import Receipts


def save_pdfs(values, pdf_path, save_path='./'):
    pdf_reader = PdfFileReader(pdf_path)
    for v in range(len(values)):
        pdf_writer = PdfFileWriter()
        page = pdf_reader.getPage(v)
        pdf_writer.addPage(page)
        file_name_extension = ''

        if os.path.isfile(f'{values[v]}.pdf'):
            acc = 2
            while os.path.isfile(f'{values[v]}({acc}).pdf'):
                acc = acc + 1

            file_name_extension = f'({acc})'

        file_name = f'{values[v]}{file_name_extension}.pdf'
        full_name = os.path.join(save_path, file_name)
        with open(full_name, 'wb') as f:
            pdf_writer.write(f)
            f.close()


infos_json = json.loads(pd.read_excel(
    './examples/extrato.xls', skiprows=2).to_json())

receipts = Receipts(values=infos_json).get_data()

bol_path = './examples/BOL.pdf'
ted_path = './examples/TED.pdf'


save_pdfs(receipts['bol'], bol_path)
save_pdfs(receipts['ted'], ted_path)
