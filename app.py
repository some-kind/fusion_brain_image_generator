import json
import base64
import datetime

import requests
from PIL import Image
from io import BytesIO

from fusion_brain_requests import FBRequest


def create_images(images_codes: list, name):
    image_number = 1
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M")
    for image_base64_code in images_codes:
        image_bin_code = base64.b64decode(image_base64_code)

        image = Image.open(BytesIO(image_bin_code))

        image.save(f"images/{formatted_datetime}_{name}_{image_number}.jpg")
        print(f"Создан файл: images/{formatted_datetime}_{name}_{image_number}.jpg")
        image_number += 1


def enter_params():
    print("Введите следующие данные через запятую без пробелов:\n"
          "   Кол-во генерируемых изображений (макс. 6, по умолчанию 1),\n"
          "   Ширину изображения в пикселях (макс. 1024, по умолчанию 1024),\n"
          "   Высоту изображения в пикселях (макс. 1024, по умолчанию 1024),\n"
          "  Пример: 3,512,512\n")
    input_params = input("Параметры: ")
    if input_params.count(",") == 2:
        input_params = input_params.split(",")

        if input_params[0].isdigit() and (int(input_params[0]) <= 6):
            number_of_images = int(input_params[0])
        else:
            print("Введены некорректные данные о количестве изображений, применено значение по умолчанию")
            number_of_images = 1

        if input_params[1].isdigit() and (int(input_params[1]) <= 1024):
            width = int(input_params[1])
        else:
            print("Введены некорректные данные о ширине изображений, применено значение по умолчанию")
            width = 1024

        if input_params[2].isdigit() and (int(input_params[2]) <= 1024):
            height = int(input_params[2])
        else:
            print("Введены некорректные данные о высоте изображений, применено значение по умолчанию")
            height = 1024
    else:
        print("Введены некорректные данные, применено значение по умолчанию")
        number_of_images = 1
        width = 1024
        height = 1024

    return number_of_images, width, height


def main():
    # чтение ключей из файла keys.json
    with open("keys.json") as keys_file:
        api_keys = json.load(keys_file)

    fb_request = FBRequest(api_keys["api_key"], api_keys["secret_api_key"])

    # получение ID модели нейросети
    model_id = fb_request.get_model()

    # получение списка стилей
    styles = requests.get(url="https://cdn.fusionbrain.ai/static/styles/api")
    styles = styles.json()

    # основной цикл
    print(" --- Для завершения программы введите 'STOP' в запросе ---")
    while True:
        # ввод промпта
        print("-" * 50)
        text_prompt = ""
        while text_prompt == "":
            text_prompt = input("Запрос на генерацию: ")

        if text_prompt == "STOP":
            print(" --- Программа завершена --- ")
            break

        # ввод параметров
        print("-" * 50)
        images_params = enter_params()

        # ввод негативного промпта (что не надо генерировать)
        print("-" * 50)
        print("Введите вещи, которые не надо генерировать:\n"
              "   Пример: яблоки, деревья, большие рога\n"
              "   Оставьте строку пустой, если не хотите ограничивать генерацию\n")
        negative_prompt = input("Негативный промпт: ")
        if negative_prompt == "":
            negative_prompt = None

        # выбор стиля
        print("-" * 50)
        print("Введите цифру стиля из предложенных:")
        number = 0
        select_style = []
        for input_style in styles:
            print(f" {number} - {input_style["title"]}")
            select_style.append(input_style["name"])
            number += 1
        input_style = input("Стиль (по умолчанию - Свой стиль): ")
        if input_style.isdigit() and (int(input_style) >= 0) and (int(input_style) <= number):
            style = select_style[int(input_style)]
        else:
            print("Введено некорректное значение, выбран стандартный стиль")
            style = "DEFAULT"

        # запрос генерации
        print("-" * 50)
        generation_uuid = fb_request.generate(text_prompt, model_id, *images_params, negative_prompt, style)
        print("Запрос получен, передан в очередь")
        print("...")

        # получение кода/кодов изображения/изображений в формате Base64
        images_codes = fb_request.get_images_codes(generation_uuid)

        # создание изображений из кодов в папке images/
        if images_codes[0] is not None:
            print("-" * 50)
            create_images(images_codes, text_prompt)


if __name__ == '__main__':
    main()
