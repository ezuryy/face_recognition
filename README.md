# Руководство администратора

До начала работы необходимо установить на машину python версии 3.10

Далее создаем виртуальное пространство и устанавливаем необходимые библиотеки. Это может занять некоторое время
```
python3.10 -m venv myvenv
source myvenv/bin/activate
pip3 install -r requirements.txt 
```

После выполнения данных команд нужно добавить в папку `train_images` 
фотографии лиц людей, которых мы собираемся распознавать. Важно, что 
названия фотографий должны иметь формат `ФИО.jpg` или `ФИО.png` 

После загрузки фотографий можно запускать скрипт, который распознает 
человека по изображению в веб камере и записывает результат распознавания (ФИО),
время и тип события (на будущее: вход `entrance` и выход `exit`)

```
python3.10 video_face_recognition.py
```
