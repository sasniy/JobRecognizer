from transformers import BertForTokenClassification, BertTokenizer
import torch
import numpy as np
import spacy

BERT_PATH = 'models/BERT'
SPACY_PATH = 'models/SPACY'

class JobRecognizer:
    _MODELS = ["bert", "spacy"]

    _idx2tag = {
        0: 'O',
        1: 'I-term',
        2: 'I-req',
        3: "PAD"
    }

    def __init__(self, model: str):
        model = model.lower()
        self._tokenizer = None
        self.model_name = None
        self.model = None
        self.change_model(model)

    def change_model(self, model):
        if model not in self._MODELS:
            raise ValueError(f'model must be {self._MODELS}')
        self.model_name = model
        self.model = self.load_model(model)

    def load_model(self, model):
        if model == 'bert':
            self._tokenizer = BertTokenizer.from_pretrained('sberbank-ai/ruBert-base')
            model = BertForTokenClassification.from_pretrained(BERT_PATH)
            return model
        if model == 'spacy':
            model = spacy.load(SPACY_PATH)
            return model

    def predict(self, text):
        if self.model_name == 'bert':
            return self.predict_bert(text)
        if self.model_name == 'spacy':
            return self.predict_spacy(text)

    def predict_bert(self, text):
        tokenized_sentence = self._tokenizer.encode(text)
        input_ids = torch.tensor([tokenized_sentence])

        self.model.eval()
        with torch.no_grad():
            output = self.model(input_ids)
            label_indices = np.argmax(output[0].numpy(), axis=2)
            tokens = self._tokenizer.convert_ids_to_tokens(input_ids.to('cpu').numpy()[0])
            new_tokens, new_labels = [], []
            for token, label_idx in zip(tokens, label_indices[0]):
                if token.startswith("##"):
                    new_tokens[-1] = new_tokens[-1] + token[2:]
                else:
                    new_labels.append(self._idx2tag[label_idx])
                    new_tokens.append(token)

            return self.postprocessing(new_tokens, new_labels)

    def postprocessing(self,tokens, labels):
        ent_dict = {value: [] for value in self._idx2tag.values()}
        previous_tag = 'O'
        seq_words = []

        for word, tag in zip(tokens, labels):
            if previous_tag == tag:
                if tag not in ["O", "PAD"]:
                    seq_words.append(word)
                    previous_tag = tag

            elif previous_tag != tag:
                if previous_tag in ["O", "PAD"]:
                    seq_words.append(word)
                    previous_tag = tag

                else:
                    ent_dict[previous_tag].append(' '.join(seq_words))
                    seq_words = []
                    previous_tag = tag
        return ent_dict
    def predict_spacy(self, text):
        doc = self.model(text)
        ents = [(ent.text, ent.label_) for ent in doc.ents]
        return ents

def main():
    model = JobRecognizer('spacy')
    text = 'Вахта в город Москва.  Обязанности: - армирование каркаса;  Требования: - опыт в строительстве приветствуется; - работа в бригаде;  Условия: - продолжительность вахты 60/30 (продление вахты возможно); - Официальное трудоустройство; - ЗП в срок и без задержек; - Авансирование дважды в месяц по 15 000 рублей, 15 и 30 числа; - Питание трехразовое за счет организации; - Выдача спецодежды и Сизов без вычета из заработной платы; - Организованные отправки до объекта (покупка билетов); - Помощь в прохождение медицинского осмотра; - Возможность получить квалификационные удостоверения; - Карьерный рост до бригадира/мастера;'
    print(model.predict(text))
    # model.change_model('spacy')
    # print(model.predict(text))


if __name__ == '__main__':
    main()
