import telebot
from service import prediction
import tempfile
import os

# Загрузка токена
with open('token.txt', 'r') as file:
    TG_TOKEN = file.read().strip()

bot = telebot.TeleBot(TG_TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 
                     "👋 Привет! Отправь мне фото для классификации.")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    """Обработка фото из чата"""
    bot.send_message(message.chat.id, "🔄 Обрабатываю...")
    
    # Получаем фото
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    # Сохраняем во временный файл
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
        tmp_file.write(downloaded_file)
        tmp_path = tmp_file.name
    
    # Классифицируем
    result = prediction(tmp_path)
    
    # Отправляем результат
    bot.send_message(message.chat.id, f"🔍 Результат:\n{result}")
    
    # Удаляем временный файл
    os.unlink(tmp_path)

if __name__ == "__main__":
    bot.infinity_polling()
