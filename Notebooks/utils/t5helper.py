from transformers import AutoTokenizer, T5EncoderModel
import torch
import pandas as pd
from datetime import datetime


class CustomModel:
    def __init__(self, pooling_function=torch.mean, uuid=datetime.now()):
        self.uuid = uuid
        self.score = pd.DataFrame(columns=["sentence", "similarity"])
        self.pooling_function = pooling_function
        self.tokenizer = AutoTokenizer.from_pretrained(
            "google-t5/t5-small", suppress_warnings=True
        )
        self.model = T5EncoderModel.from_pretrained("google-t5/t5-small")

    def tokenize(self, value):
        return self.tokenizer(value, return_tensors="pt").input_ids

    def encode(self, value):
        outputs = self.model(input_ids=value)
        return outputs.last_hidden_state

    def pool(self, value):
        fn = self.pooling_function
        if fn == torch.max:
            return torch.max(value, dim=1).values.unsqueeze(0)
        elif fn == torch.mean:
            return torch.mean(value, dim=1).unsqueeze(0)

    def evaluate(self, query, text, limit=None):
        tok_query = self.tokenize(query)
        enc_query = self.encode(tok_query)
        pooled_query = self.pool(enc_query)

        for idx, sentence in enumerate(text):
            tok_sentences = self.tokenize(sentence)
            enc_sentence = self.encode(tok_sentences)
            pooled_sentence = self.pool(enc_sentence)

            # why are we doing this ?
            tmp_enc_pool_query = pooled_query.view(1, -1)

            sim = torch.matmul(pooled_sentence, tmp_enc_pool_query.T).item()
            self.score = pd.concat(
                [
                    self.score,
                    pd.DataFrame({"sentence": [sentence], "similarity": [sim]}),
                ],
                ignore_index=True,
            )
            if idx % 100 == 0:
                print(f"Parsed {idx} of {len(text)}")
            if limit is not None and idx > limit:
                return

    def sort_simularity(self):
        self.score = self.score.sort_values(by="similarity", ascending=False)

    def show(self):
        self.sort_simularity()
        print(self.score)

    def toCSV(self):
        self.score.to_csv(f"tmp/{self.uuid}.csv", index=True)