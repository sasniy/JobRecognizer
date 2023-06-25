import pandas as pd

class DataWorker:
    available_column = ['responsibilities','description']
    def __init__(self,contents):
        self._df = pd.read_excel(contents)
        self._check_column()
    def _check_column(self):
        for column in self.available_column:
            if column in self._df.columns:
                self.column = column
                return
        raise ValueError('need column not found')

    def get_need_columns(self,model):
        descriptions = self._df[self.column].values
        answers = [model.predict(text) for text in descriptions]
        req = []
        terms = []
        charge = []
        notes = []
        for answers in answers:
            temp_req,temp_terms,temp_charge,temp_notes = self.preprocessed_text(answers)
            req.append(temp_req)
            terms.append(temp_terms)
            charge.append(temp_charge)
            notes.append(temp_notes)
        # req = self.from_list(req)
        # terms = self.from_list(terms)
        # charge = self.from_list(charge)
        # notes = self.from_list(notes)
        temp_df = pd.DataFrame({'Полное описание':descriptions,'Требования':req,'Условия':terms,'Обязанности':charge,'Примечания':notes})
        self._df = temp_df

    @staticmethod
    def from_list(arr):
        formatted_string = '\n'.join(['\n'.join([str(element) for element in sublist]) for sublist in arr])
        return formatted_string
    @staticmethod
    def preprocessed_text(annotations):
        req = []
        terms = []
        charge = []
        notes = []
        for text, label in annotations:
            if label == 'req':
                req.append(text)
            elif label == 'term':
                terms.append(text)
            elif label == 'resp':
                charge.append(text)
            elif label == 'note':
                notes.append(text)
        return req, terms, charge, notes

