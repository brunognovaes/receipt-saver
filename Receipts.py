class Receipts:
    def __init__(self, values):
        self.values = values

    def get_data(self):
        data = {
            'ted': [],
            'bol': [],
        }
        historic_column = self.values['HISTÓRICO']

        for v in historic_column:
            if historic_column[v] == 'DÉB.TIT.COMPE EFETIVADO':
                data['bol'].append(historic_column[str(int(v) + 1)])
            if historic_column[v] == 'DEBITO EMISSÃO TED DIF.TITULARIDADE':
                data['ted'].append(historic_column[str(int(v) + 2)])
        return data
