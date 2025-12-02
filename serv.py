from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np

# Загрузка модели и меток классов
model = load_model("C:/Users/User-F/Desktop/pyton/m7u2tgbot/keras/keras_model.h5", compile=False)

with open("keras/labels.txt", "r", encoding="utf-8") as f:
    class_names = [line.strip() for line in f.readlines()]

def prediction(image_path="imgs/image.png"):
    """
    Классификация изображения
    
    Args:
        image_path: путь к изображению
        
    Returns:
        str: результат классификации
    """
    # Загрузка и обработка изображения
    image = Image.open(image_path).convert("RGB")
    image = ImageOps.fit(image, (224, 224), Image.Resampling.LANCZOS)
    
    # Преобразование в numpy массив
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    
    # Подготовка данных для модели
    data = np.expand_dims(normalized_image_array, axis=0)
    
    # Предсказание
    prediction_result = model.predict(data, verbose=0)[0]
    index = np.argmax(prediction_result)
    
    # Получение результата
    class_name = class_names[index]
    confidence = prediction_result[index]
    
    # Убираем нумерацию из названия класса, если есть
    if class_name[1:2] == " ":
        class_name = class_name[2:]
    
    return f"🏷️ {class_name}\n🎯 {confidence:.1%}"
