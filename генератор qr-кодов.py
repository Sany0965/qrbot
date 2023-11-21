import telebot
import qrcode

bot = telebot.TeleBot('YOUR_BOT_TOKEN')

def generate_qr_code(text):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Я бот для генерации QR-кодов. Пожалуйста, отправьте мне текст, который вы хотите закодировать в QR-код.")

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    try:
        user_input = message.text
        
        # Проверяем, если команда /code, то отправляем ссылку на GitHub
        if user_input.lower() == '/code':
            github_url = 'https://github.com/Sany0965/qrbot'
            bot.send_message(message.chat.id, f"Исходный код бота доступен по ссылке:\n{github_url}")
        else:
            qr_image = generate_qr_code(user_input)
            qr_image.save("qr_code.png")
            
            # Отправляем текст вместе с QR-кодом
            with open("qr_code.png", "rb") as photo:
                bot.send_photo(message.chat.id, photo, caption=user_input)
    except Exception as e:
        error_message = 'Произошла ошибка при создании QR-кода. Пожалуйста, попробуйте еще раз.'
        bot.send_message(message.chat.id, error_message)

if __name__ == "__main__":
    bot.polling(none_stop=True)
