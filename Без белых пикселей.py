# Необходимые библиотеки

from tkinter import filedialog
from tkinter import *
from PIL import Image, UnidentifiedImageError, ImageFilter
import os

# Максимальная ширина и неизменные данные

MAX_WIDTH = 1200
SUFFIX = '_process'


# Функция для обработки изображений
def processed_image(path, out_jpegs_dir, out_webps_dir):
    try:

        # Открытие изображения

        with Image.open(path) as img:
            img.load()

        # Проверка на подходящий формат

        if img.format == 'PNG' or img.format == 'JPEG':

            width, height = img.size

            if img.mode != "RGBA":
                img = img.convert('RGBA')

            # Манипуляция изменения размеров картинки

            if width > MAX_WIDTH:
                new_w = MAX_WIDTH
                new_h = int(height * (new_w / width))
                img = img.resize((new_w, new_h), Image.LANCZOS)
                img = img.filter(ImageFilter.MinFilter(3))
                img = img.filter(ImageFilter.MaxFilter(3))

            else:
                new_w = MAX_WIDTH
                new_h = int(height * (new_w / width))
                img = img.resize((new_w, new_h), Image.LANCZOS)
                img = img.filter(ImageFilter.MinFilter(3))
                img = img.filter(ImageFilter.MaxFilter(3))

            if img.mode != "RGB":
                img = img.convert('RGB')

            # Создание путей для сохранения измененного файла

            base = os.path.splitext(os.path.basename(path))[0]
            out_jpeg = os.path.join(out_jpegs_dir, f"{base}{SUFFIX}.jpg")
            out_webp = os.path.join(out_webps_dir, f"{base}{SUFFIX}.webp")

            # Сохранение измененного файла

            try:
                img.save(out_jpeg, format='JPEG')
                print(f"Сохранение JPEG -> {out_jpeg}")
            except Exception as e:
                print(f"Щшибка при сохранении JPEG: {e}")

            try:
                img.save(out_webp, format='WEBP')
                print(f"Сохранение WEBP -> {out_webp}")
            except Exception as e:
                print(f"Щшибка при сохранении WEBP: {e}")

        # Различные ошибки

        else:
            print('Неправильное расширение файла')
            return

    except UnidentifiedImageError:
        print(f'Непонятный файл {path}')
    except Exception as e:
        print(f'Ошибка обработки {path}: {e}')


# Функция для получения пути для файла

def main_file():
    # Открытие проводника для записи пути

    script_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = filedialog.askopenfilename()

    # Ошибка на отсутствие файла

    if images_dir == '':
        print('Файл отсутствует')
        return

    # Создание путей для сохранения файла

    out_dir = os.path.join(script_dir, 'out')
    out_jpegs = os.path.join(out_dir, 'jpegs')
    out_webps = os.path.join(out_dir, 'webps')

    # Создание катологов

    os.makedirs(out_jpegs, exist_ok=True)
    os.makedirs(out_webps, exist_ok=True)

    # Вызов функии для обработки изображения

    processed_image(images_dir, out_jpegs, out_webps)


# Функция для полученияя путей файлов в папке
def main_papka():
    # Открытие проводника для записи пути

    script_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = filedialog.askdirectory()

    # Ошибка на отсутствие папки

    if images_dir == '':
        print('Файл отсутствует')
        return

    # Создание списка путей файлов

    files = [os.path.join(images_dir, f) for f in os.listdir(images_dir)]

    # Ошибка на пустую папки

    if not files:
        print('Папка с файлами пустая')
        return

    # Создание путей для сохранения файла

    out_dir = os.path.join(script_dir, 'out')
    out_jpegs = os.path.join(out_dir, 'jpegs')
    out_webps = os.path.join(out_dir, 'webps')

    # Создание катологов

    os.makedirs(out_jpegs, exist_ok=True)
    os.makedirs(out_webps, exist_ok=True)

    # Вызов функии для обработки изображения

    for file in files:
        processed_image(file, out_jpegs, out_webps)


# Основной процесс

if __name__ == '__main__':
    # СОздание окна

    window = Tk()
    window.title("Задание")
    window.geometry('400x250')

    # Создание текста на окне

    lbl = Label(window, text="Выберите формат выбора файла/ов:")
    lbl.grid(column=0, row=0)

    # Создание кнопок на окне

    btn_1 = Button(window, text="Папкой", command=main_papka)
    btn_1.grid(column=0, row=4)
    btn_2 = Button(window, text="Файлом", command=main_file)
    btn_2.grid(column=3, row=4)

    # Для показа окна

    window.mainloop()