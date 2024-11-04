import telebot
from telebot import types
from pytube import YouTube
from pydub import AudioSegment
import instaloader

# Telegram bot tokenini kiriting
bot = telebot.TeleBot("7941943981:AAFPJvHzVPX0iAlplPXaPJzBuPkgZI9rz6o")

# Instagram yuklovchi uchun instaloader
loader = instaloader.Instaloader()

# Foydalanuvchi video yoki reals linkini yuborganda
@bot.message_handler(commands=['start'])
def welcome_message(message):
    bot.send_message(
        message.chat.id, 
        "Salom! Menga Instagram yoki YouTube video yoki reals linkini yuboring."
    )

@bot.message_handler(func=lambda message: 'instagram.com' in message.text or 'youtube.com' in message.text)
def handle_video_link(message):
    video_url = message.text
    markup = types.InlineKeyboardMarkup()
    
    # "To'liq qo'shiqni topish" tugmasi
    full_song_btn = types.InlineKeyboardButton("Qo'shiqni to'lig'ini topish", callback_data="find_full_song")
    # "Videodagi qo'shiqni ajratib olish" tugmasi
    extract_audio_btn = types.InlineKeyboardButton("Videodagi qo'shiqni ajratib olish", callback_data="extract_audio")
    
    markup.add(full_song_btn, extract_audio_btn)
    
    bot.send_message(
        message.chat.id, 
        "Tanlang:", 
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data in ["find_full_song", "extract_audio"])
def handle_buttons(call):
    video_url = call.message.reply_to_message.text

    if call.data == "find_full_song":
        # Bu yerda qo'shiqni qidirish uchun audio tanib olish xizmatidan foydalaning
        bot.send_message(call.message.chat.id, "Kechirasiz, hozircha bu funksiyani qo'llab-quvvatlay olmaymiz.")
    
    elif call.data == "extract_audio":
        try:
            if 'youtube.com' in video_url:
                yt = YouTube(video_url)
                stream = yt.streams.filter(only_audio=True).first()
                audio_file = stream.download(filename="video_audio.mp3")
            elif 'instagram.com' in video_url:
                loader.download_post(video_url, target="video_audio.mp4")
                audio = AudioSegment.from_file("video_audio.mp4")
                audio.export("video_audio.mp3", format="mp3")
            
            with open("video_audio.mp3", "rb") as audio:
                bot.send_audio(call.message.chat.id, audio)
                
        except Exception as e:
            bot.send_message(call.message.chat.id, f"Xatolik yuz berdi: {str(e)}")

bot.polling()
