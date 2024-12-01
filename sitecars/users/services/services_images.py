from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

def load_default_image():
    """
       Загрузка изображения по умолчанию (default_user_image.jpg) из хранилища и возвращение
       его в виде объекта ContentFile.

       Эта функция используется для загрузки изображения, которое будет использовано в
       качестве изображения по умолчанию для пользователя,
       если пользователь не загрузил собственное изображение.

       Returns:
           ContentFile: Объект ContentFile, содержащий данные изображения и его имя.
       """
    image = ContentFile(default_storage.open('users/default_user_image.jpg').read(),
                        name='default_user_image.jpg'
                        )
    return image


def convert_to_jpeg_if_needed(img):
    """
    Проверяет формат изображения и преобразует его в JPEG, если необходимо.

    :param img: Изображение, которое нужно проверить и, при необходимости, преобразовать.
    :return: Изображение в формате JPEG (или уже в JPEG, если оно им было изначально).
    """

    if img.mode != 'RGB':
        img = img.convert('RGB')

        # Создаем новый файл JPEG
    output = BytesIO()
    img.save(output, format='JPEG', quality=85)
    output.seek(0)

    # Заменяем оригинальное изображение на преобразованное
    return ContentFile(output.read(), name='user_avatar_image.jpg')

def resize_image(img, size):
    """
       Изменяет размер изображения до заданных параметров.

       :param img: Объект изображения, который необходимо изменить.
       :param size: Кортеж с двумя целочисленными значениями (ширина, высота), которые указывают
                    новый размер изображения.

       :return: Измененный объект изображения (тип Image.Image).

       :raises ValueError: Если переданный объект не является изображением или размер не является кортежем из двух чисел.
       """

    return img.resize(size, Image.Resampling.LANCZOS)