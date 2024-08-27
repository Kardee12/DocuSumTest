"""EXAMPLES"""
import apihelper

class huggingFaceAPis:

    def __init__(self):
        self.helper = apihelper.apiHelper()

    def sumQuery(self, model, text, max_length, min_length):
        APIURL, modelKey = self.helper.base(model)
        payload = {"inputs": text}
        if modelKey != "FLAN-T5":
            payload.update({
                "max_length": max_length,
                "min_length": min_length
            })
        if modelKey in ["FLAN-T5"]:
            payload["inputs"] = f"Summarize: {text}"

        return self.helper.closure(APIURL, payload)

    def transQuery(self, model, text, langTTF, langTTT):
        APIURL, modelKey = self.helper.base(model)
        src_lang_code = langTTF
        tgt_lang_code = langTTT
        payload = {
            "inputs": text,
            "parameters": {
                "src_lang": src_lang_code,
                "tgt_lang": tgt_lang_code
            }
        }
        print(payload)
        print("DONE")
        return self.helper.closure(APIURL, payload)

    def askQuery(self, model, text, question):
        APIURL, modelKey = self.helper.base(model)
        payload = {
            "inputs": {
                "question": question,
                "context": text
            }
        }

        print(payload)
        return self.helper.closure(APIURL, payload)

    def sentimentQuery(self, model, text):
        APIURL, modelKey = self.helper.base(model)
        payload = {
            "inputs": f"What is the sentiment of this? {text}"
        }
        return self.helper.closure(APIURL, payload)
