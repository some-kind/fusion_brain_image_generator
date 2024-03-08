import json
import time

import requests


class FBRequest:
    """
    Accessing the Fusion Brain API
    """
    def __init__(self, api_key, secret_key, url="https://api-key.fusionbrain.ai/"):
        """
        Initialization
        :param url: URL address Fusion Brain API
        :param api_key: Your API Key
        :param secret_key: Your Secret Key
        """
        self.__url = url
        self.__auth_headers = {
            "X-Key": f"Key {api_key}",
            "X-Secret": f"Secret {secret_key}",
        }

    def get_model(self):
        """
        Getting the ID of the neural network model available for the API
        :return: ID of model
        """
        response = requests.get(self.__url + "key/api/v1/models", headers=self.__auth_headers)
        if response.status_code == 401:
            print("Неправильные API ключи")
            return None
        else:
            data = response.json()
            return data[0]["id"]

    def generate(self, prompt, model, width=1024, height=1024, negative_prompt=None, style="DEFAULT"):
        """
        Request for image generation
        :param prompt: Description of the desired image
        :param model: ID of model (you can get it using the 'get_model' method)
        :param width: Width of image
        :param height: Height of image
        :param negative_prompt: Description of prohibited items for generation
        :param style: Style of image
        :return: unique operation number (UUID)
        """

        # во время тех работ вместо uuid вернётся словарь (но это не точно)
        # {
        #   "model_status": "DISABLED_BY_QUEUE"
        # }
        params = {
            "type": "GENERATE",
            "numImages": 1,
            "width": width,
            "height": height,
            "style": style,
            "negativePromptUnclip": negative_prompt,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            "model_id": (None, model),
            "params": (None, json.dumps(params), "application/json")
        }

        response = requests.post(self.__url + "key/api/v1/text2image/run", headers=self.__auth_headers, files=data)
        generation_data = response.json()
        return generation_data["uuid"]

    def __check_generation(self, request_uuid):
        """
        Checking the generation status
        :param request_uuid: Unique operation number (you can get it using the 'generate' method)
        :return: dictionary with data of generation
        """
        response = requests.get(self.__url + 'key/api/v1/text2image/status/' + request_uuid,
                                headers=self.__auth_headers)
        data = response.json()
        return data

    def get_images_codes(self, generation_uuid):
        """
        Checking the generation status and getting the image code
        :param generation_uuid: Unique operation number (you can get it using the 'generate' method)
        :return: A list of Base64 format strings in which the generated image is encoded
        """
        delay_time_sec = 2
        for _ in range(60):
            result = self.__check_generation(generation_uuid)
            if result["censored"] is True:
                print("Ваш запрос не прошёл цензуру Fusion Brain")
                break
            if result["status"] == "INITIAL":
                print("В очереди на генерацию")
            elif result["status"] == "PROCESSING":
                print("Генерация изображений")
            elif result["status"] == "FAIL":
                print(f"Возникла ошибка: {result["errorDescription"]}")
                break
            elif result["status"] == "DONE":
                print("Генерация завершена\n")
                return result["images"]

            print("...")
            time.sleep(delay_time_sec)
        return [None]
