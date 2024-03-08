# fusion_brain_image_generator
This program is a console application for generating images using the API fusionbrain.ai

For the application to work, you will need to install dependencies from the file requirements.txt 
You can do this with the pip3 install -r command requirements.txt

You must also create an "images" folder in the program folder. The generated images will be saved in it
In addition, you will also need the "keys.json" file in the program folder with the following contents:

{
  "secret_api_key": "00000000000000000000000000000",
  "api_key": "000000000000000000000000000"
}

In this file, you must specify your API keys for the Fusion Brain account.
Instructions for obtaining API keys can be found here https://fusionbrain.ai/docs/doc/poshagovaya-instrukciya-po-upravleniu-api-kluchami/

After installing all the dependencies, creating a file with API keys and the "images" folder, you can run the program 
  python3 app.py

You will be asked to enter a prompt (a request for generation), specify the parameters and the number of images, and select a style.
If errors are made when entering data, the default data will be selected.

The generated images are placed in the "images" folder and have the name of the format "date_and_time_of_generation_text_query_number_of_image.jpg"



############ RUSSIAN ##############

Эта программа является консольным приложением для генерирования изображений с помощью API fusionbrain.ai

Для работы приложения вам понадобится установить зависимости из файла requirements.txt
Сделать это можно командой pip3 install -r requirements.txt

Также в папке с программой необходимо создать папку "images". В ней будут сохраняться сгенерированные изображения
Кроме того также в папке с программой вам понадобится файл "keys.json" со следующим содержимым:

{
  "secret_api_key": "00000000000000000000000000000",
  "api_key": "000000000000000000000000000"
}

В этом файле необходимо указать ваши API ключи от аккаунта Fusion Brain.
Инструкцию по получению API ключей можно найти здесь https://fusionbrain.ai/docs/doc/poshagovaya-instrukciya-po-upravleniu-api-kluchami/

После установки всех зависимостей, создания файла с API ключами и папки images, можно запускать программу 
  python3 app.py

Вас попросят ввести промпт (запрос для генерации), указать параметры и количество изображений, выбрать стиль.
Если будут допущены ошибки при вводе данных, будут выбраны данные по умолчанию.

Сгенерированные изображения помещаются в папку images и имеют название формата "дата_и_время_генерации_текст_запроса_номер_изображения.jpg"
