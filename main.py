import pandas as pd
from PyPDF2 import PdfFileWriter, PdfFileReader
import os
import json


def get_data(values):
    data = {
        'ted': [],
        'bol': [],
        'conv': [],
    }

    historic_column = values['HISTÓRICO']
    value_column = values['VALOR']

    for v in historic_column:
        current_value = historic_column[v]
        if current_value == 'DÉB.TIT.COMPE EFETIVADO':
            data['bol'].append(historic_column[str(int(v) + 1)])
        if current_value == 'DEBITO EMISSÃO TED DIF.TITULARIDADE':
            try:
                receipt_code = int(historic_column[str(int(v) + 2)])
                data['ted'].append(receipt_code)
            except:
                receipt_value = value_column[v]
                data['ted'].append(receipt_value.replace('D', ''))
        if 'DÉB.CONV' in current_value:
            try:
                receipt_code = int(historic_column[str(int(v) + 1)])
                data['conv'].append(receipt_code)
            except:
                receipt_value = value_column[v]
                data['conv'].append(receipt_value.replace('D', ''))
        if 'DÉB.TRANSF.CONTAS' in current_value:
            receipt_value = value_column[v]
            data['ted'].append(receipt_value.replace('D', ''))
    return data


def save_pdfs(values, pdf_path, save_path='./'):
    pdf_reader = PdfFileReader(pdf_path)
    for v in range(len(values)):
        pdf_writer = PdfFileWriter()
        page = pdf_reader.getPage(v)
        pdf_writer.addPage(page)
        file_name_extension = ''

        file_name = f'{values[v]}.pdf'
        full_name = os.path.join(save_path, file_name)

        if os.path.isfile(f'{full_name}'):
            acc = 2
            while os.path.isfile(f'{values[v]}({acc}).pdf'):
                acc = acc + 1

            file_name_extension = f'({acc})'
            file_name = f'{values[v]}{file_name_extension}.pdf'
            full_name = os.path.join(save_path, file_name)

        if not os.path.isdir(save_path):
            os.mkdir(save_path)

        with open(full_name, 'wb') as f:

            pdf_writer.write(f)
            f.close()


infos_json = json.loads(pd.read_excel(
    './pdfs/EXTRATO.xls', skiprows=2).to_json())

receipts = get_data(infos_json)

bol_path = './pdfs/BOL.pdf'
ted_path = './pdfs/TED.pdf'
conv_path = './pdfs/CONV.pdf'
save_path = './comprovantes'

save_pdfs(receipts['bol'], bol_path, save_path=save_path)
save_pdfs(receipts['ted'], ted_path, save_path=save_path)
save_pdfs(receipts['conv'], conv_path, save_path=save_path)
