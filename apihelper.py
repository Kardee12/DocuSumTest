import PyPDF2
import json
import logging

import requests

with open('config.json', 'r') as file:
    configFile = json.load(file)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
hf_token_header = {"Authorization": f"Bearer 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"}
class apiHelper:
    def base(self, model):
        logger.info("The config file is loaded.")
        modelKey = model.upper()
        APIURL = configFile["APIs"].get(modelKey)
        if not APIURL:
            logger.error(f"API URL for model {model} not found.")
            return None

        return APIURL, modelKey

    def closure(self, APIURL, payload):
        try:
            response = requests.post(APIURL, headers=hf_token_header, json=payload)
            response.raise_for_status()
            logger.info(response.json())
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            return None
