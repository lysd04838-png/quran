import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

TOKEN = "8820947885:AAEMJEH1HxeWgMJTS4KSWPAt0pmOC7DiCwA"
PASSWORD = "123"

bot = telebot.TeleBot(TOKEN)
authenticated_users = set()

SURAHS = {
    "fatiha": {
        "name": "سورة الفاتحة",
        "audio": "https://server8.mp3quran.net/afs/001.mp3",
    },
    "ikhlas": {
        "name": "سورة الإخلاص",
        "audio": "https://server8.mp3quran.net/afs/112.mp3",
    },
    "falaq": {
        "name": "سورة الفلق",
        "audio": "https://server8.mp3quran.net/afs/113.mp3",
    },
    "nas": {
        "name": "سورة الناس",
        "audio": "https://server8.mp3quran.net/afs/114.mp3",
    },
}


def get_surah_keyboard():
    keyboard = InlineKeyboardMarkup()
    for key, data in SURAHS.items():
        btn = InlineKeyboardButton(text=data["name"], callback_data=key)
        keyboard.add(btn)
    return keyboard


@bot.message_handler(commands=["start"])
def start_cmd(message):
    user_id = message.from_user.id
    if user_id in authenticated_users:
        bot.send_message(
            message.chat.id,
            "📖 اختر السورة للاستماع إليها:",
            reply_markup=get_surah_keyboard(),
        )
    else:
        bot.send_message(
            message.chat.id,
            "🔒 البوت محمي بكلمة سر.\nيرجى إرسال كلمة السر للدخول:",
        )


@bot.message_handler(func=lambda msg: True)
def check_pass(message):
    user_id = message.from_user.id
    if user_id in authenticated_users:
        return

    if message.text == PASSWORD:
        authenticated_users.add(user_id)
        bot.send_message(
            message.chat.id,
            "✅ تم التحقق بنجاح!\n📖 اختر السورة:",
            reply_markup=get_surah_keyboard(),
        )
    else:
        bot.send_message(
            message.chat.id, "❌ كلمة السر غير صحيحة! حاول مجدداً:"
        )


@bot.callback_query_handler(func=lambda call: True)
def play_surah(call):
    surah_key = call.data
    if surah_key in SURAHS:
        surah = SURAHS[surah_key]
        bot.answer_callback_query(
            call.id, text=f"جاري تشغيل {surah['name']}..."
        )
        bot.send_audio(
            chat_id=call.message.chat.id,
            audio=surah["audio"],
            title=surah["name"],
            performer="مشاري راشد العفاسي",
        )


print("🚀 البوت يعمل الآن بنجاح...")
bot.infinity_polling()
