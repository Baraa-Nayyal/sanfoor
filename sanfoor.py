
import asyncio
from datetime import datetime

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)

import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_GROUP_ID = "-1002993388534"
START_LOG_GROUP_ID = "-1003196454615"

COMMUNITY_LINK = "https://t.me/+WYx9Q7_DHcg3Nzk0"

WAIT_USERNAME = 0
WELCOME = 1
EDUCATION = 2
GOVERNORATE = 3
LAPTOP = 4
INFORMATICS = 5
PROGRAMMING = 6
REFERRAL = 7
OTHER_SOURCE = 8
CONFIRMATION = 9


QUESTIONS = {
    "education": {
        "text": "🎓 هل انتهيت من البكالوريا حالياً؟",
        "state": EDUCATION,
        "next": "governorate",
        "options": [
            ("🎓 انتهيت وهالسنة أنا طالب جامعي", "university"),
            ("📚 لسه أنا بكالوريا", "baccalaureate")
        ]
    },
    "governorate": {
        "text": "📍 من أي محافظة؟",
        "state": GOVERNORATE,
        "next": "laptop",
        "options": [
            ("📍 دمشق وريف دمشق", "damascus"),
            ("📍 حلب", "aleppo"),
            ("📍 حمص", "homs"),
            ("📍 حماة", "hama"),
            ("📍 اللاذقية", "latakia"),
            ("📍 طرطوس", "tartous"),
            ("📍 إدلب", "idlib"),
            ("📍 دير الزور", "deir_ezzor"),
            ("📍 الحسكة", "hasakah"),
            ("📍 الرقة", "raqqa"),
            ("📍 السويداء", "sweida"),
            ("📍 درعا", "daraa"),
            ("📍 القنيطرة", "quneitra"),
            ("🌍 خارج سوريا", "outside_syria")
        ]
    },
    "laptop": {
        "text": "💻 هل عندك لابتوب؟",
        "state": LAPTOP,
        "next": "informatics",
        "options": [
            ("✅ نعم", "yes"),
            ("⏳ لسه ما اشتريت ولكن قريباً", "soon")
        ]
    },
    "informatics": {
        "text": "🧑‍💻 مسجل معلوماتية؟",
        "state": INFORMATICS,
        "next": "programming",
        "options": [
            ("✅ إي وضمنان تطلعلي", "registered"),
            ("🤔 لسه مو متأكد من المفاضلة", "not_sure")
        ]
    },
    "programming": {
        "text": "💡 عندك خلفية عن البرمجة؟",
        "state": PROGRAMMING,
        "next": "referral",
        "options": [
            ("💻 إي، متعلم برمجة من زمان", "experienced"),
            ("🌱 ما عندي أبداً، أنا مبتدئ من الصفر", "beginner")
        ]
    },
    "referral": {
        "text": "🔎 من وين تعرفت على شغوف؟",
        "state": REFERRAL,
        "next": None,
        "options": [
            ("📸 Instagram", "instagram"),
            ("📘 Facebook", "facebook"),
            ("✈️ Telegram", "telegram"),
            ("🧑‍🤝‍🧑 من صديق", "friend"),
            ("🎓 من الجامعة", "university"),
            ("🎟️ من فعالية أو ورشة", "event"),
            ("🔗 مصدر آخر", "other")
        ]
    }
}


FIELD_NAMES = {
    "education": "🎓 الحالة الدراسية",
    "governorate": "📍 المحافظة",
    "laptop": "💻 امتلاك لابتوب",
    "informatics": "🧑‍💻 التسجيل بالمعلوماتية",
    "programming": "💡 الخلفية البرمجية",
    "referral": "🔎 مصدر التعرف على شغوف"
}


async def notify_start(context, user):
    username = f"@{user.username}" if user.username else f"ID: {user.id}"

    await context.bot.send_message(
        chat_id=START_LOG_GROUP_ID,
        text=f"{user.full_name}\n{username}"
    )


async def show_welcome(message):
    text = (
        "بعرف نشفت عيونك هالسنة بسبب المفاضلة وتأخر صدورها، "
        "الموضوع ممكن يوترك ولكن لا تقلق، نحن هون لنساعدك 😁\n\n"
        "احا كيف ؟ نظمنا مجتمع \"شغوف سنفور\" 🔥\n\n"
        "مجتمع بيجمع طلاب البكالوريا مهندسي المستقبل مع أشخاص "
        "من مختلف الجامعات والتخصصات بالهندسة المعلوماتية ضمن مجتمع شغوف 👀\n\n"
        "🎯 هدفنا نشارك تجاربنا بالحياة الجامعية بدون فلاتر، مجرد تجربة "
        "واقعية رح تخليك تكتشف طبيعة الفرع الحقيقية ونشالله هالمجتمع "
        "رح يكون ذكرى الك طول حياتك الجامعية ورح تضل تدعيلنا وتكتشف "
        "اديه هالفرع فيه ناس فخمة ومستعدة تشارك وتعطي للناس الجديدة 🔥\n\n"
        "ولا تنسى، كل مهندس خبير كان بيوم من الأيام سنفور 🤏\n\n"
        "💬 خلينا نتعرف عليك من خلال كم سؤال بسيط."
    )

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✨ ابدأ التسجيل", callback_data="begin")]
    ])

    await message.reply_text(text, reply_markup=keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    await notify_start(context, user)

    context.user_data.clear()

    if not user.username:
        text = (
            "أهلاً فيك! 👋\n\n"
            "للمتابعة والتسجيل في مجتمع شغوف سنفور، "
            "لازم يكون عندك Telegram Username.\n\n"
            "🛠️ طريقة إضافته:\n\n"
            "1️⃣ افتح Telegram.\n"
            "2️⃣ ادخل إلى Settings.\n"
            "3️⃣ اختر Edit Profile.\n"
            "4️⃣ اضغط Username.\n"
            "5️⃣ أضف معرفاً واحفظ التغييرات.\n\n"
            "✅ بعد إضافته ارجع للبوت واضغط تحقق."
        )

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(
                "🔍 تحقق من Username",
                callback_data="check_username"
            )]
        ])

        await update.message.reply_text(
            text,
            reply_markup=keyboard
        )

        return WAIT_USERNAME

    await show_welcome(update.message)
    return WELCOME


async def check_username(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()

    user = update.effective_user

    if not user.username:
        await query.message.reply_text(
            "⚠️ لسه ما أضفت Username لحسابك.\n"
            "أضفه من إعدادات Telegram وحاول مرة ثانية. 🔄"
        )
        return WAIT_USERNAME

    await show_welcome(query.message)
    return WELCOME


async def begin_registration(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()

    await ask_question(query.message, "education")

    return EDUCATION


async def ask_question(message, question_key):
    question = QUESTIONS[question_key]

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                label,
                callback_data=f"q|{question_key}|{value}"
            )
        ]
        for label, value in question["options"]
    ])

    await message.edit_text(
        question["text"],
        reply_markup=keyboard
    )


async def show_confirmation(message):
    text = (
        "📝 مراجعة وتأكيد التسجيل\n\n"
        "قبل إكمال التسجيل، يرجى التأكد من أن جميع "
        "المعلومات التي أدخلتها صحيحة.\n\n"
        "✅ بالضغط على «أكمل»، أنت تؤكد صحة المعلومات المقدمة، "
        "وتوافق على إمكانية إزالة عضويتك من مجتمع شغوف "
        "في حال ثبوت مخالفتها للواقع.\n\n"
        "هل تؤكد صحة معلوماتك؟ 👇"
    )

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            "✅ أكمل",
            callback_data="confirm|yes"
        )],
        [InlineKeyboardButton(
            "❌ إلغاء",
            callback_data="confirm|no"
        )]
    ])

    await message.edit_text(
        text,
        reply_markup=keyboard
    )


async def handle_choice(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()

    _, question_key, value = query.data.split("|", 2)

    question = QUESTIONS[question_key]

    selected_label = next(
        label
        for label, option_value in question["options"]
        if option_value == value
    )

    context.user_data[question_key] = selected_label

    if question_key == "referral" and value == "other":
        await query.message.edit_text(
            "✍️ يرجى كتابة المصدر الذي تعرفت من خلاله على شغوف:"
        )
        return OTHER_SOURCE

    next_question = question["next"]

    if next_question:
        await ask_question(query.message, next_question)
        return QUESTIONS[next_question]["state"]

    await show_confirmation(query.message)
    return CONFIRMATION


async def handle_other_source(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    context.user_data["referral"] = update.message.text.strip()

    await show_confirmation(update.message)
    return CONFIRMATION


async def handle_confirmation(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()

    user = update.effective_user

    if query.data == "confirm|no":
        context.user_data.clear()

        await query.message.edit_text(
            "❌ تم إلغاء عملية التسجيل.\n\n"
        )

        return ConversationHandler.END

    data = context.user_data

    username = f"@{user.username}"

    registration_date = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    admin_message = (
        " تسجيل جديد في شغوف سنفور\n\n"
        f" الاسم: {user.first_name}\n"
        f"Username: {username}\n"
    )

    for key, field_name in FIELD_NAMES.items():
        admin_message += (
            f"{field_name}: {data[key]}\n"
        )

    await context.bot.send_message(
        chat_id=ADMIN_GROUP_ID,
        text=admin_message
    )

    context.user_data.clear()

    await query.message.edit_text(
        "🔍 جاري تجهيز طلب انضمامك إلى مجتمع شغوف..."
    )

    await asyncio.sleep(2)

    await query.message.reply_text(
        "⏳ يرجى الانتظار قليلاً، عم نجهزلك مكانك بالمجتمع! 💛"
    )

    await asyncio.sleep(2)

    welcome_message = (
        "🎉 تمت الموافقة على انضمامك بنجاح!\n\n"
        "أهلاً وسهلاً فيك بعائلة شغوف سنفور ❤️\n\n"
        "🔗 رابط المجتمع:\n"
        f"{COMMUNITY_LINK}\n\n"
        "فريق شغوف رح يوافق على طلب انضمامك بالوقت القريب ان شاء الله\n\n"
        "📌 ملاحظات مهمة:\n\n"
        "1️⃣ المجتمع مخصص لطلاب البكالوريا والطلاب الجامعيين الجدد.\n"
        "2️⃣ يحق لفريق شغوف إزالة عضويتك في حال كانت "
        "المعلومات المقدمة أثناء التسجيل مغلوطة.\n"
        "3️⃣ رابط المجتمع مخصص لانضمامك فقط، ومشاركته "
        "مع الآخرين تؤدي إلى حظرك وحظر الشخص الذي انضم عن طريقه.\n"
        "4️⃣ لإضافة رفقاتك، يرجى إرسال رابط البوت لهم "
        "حتى يسجلوا وينضموا بالطريقة الصحيحة.\n\n"

         "‼️ قبولك بهالمجتمع يعني التزامك بالتفاعل واعطاؤه جزء مهم من وقتك لهيك جهزلها نفسيتك \n\n"
        "🌟 نتمنى تكون تجربتك معنا مفيدة وممتعة!\n\n"
        "فريق شغوف ❤️"
    )

    await query.message.reply_text(welcome_message)

    return ConversationHandler.END


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    conversation = ConversationHandler(
        entry_points=[
            CommandHandler("start", start)
        ],
        states={
            WAIT_USERNAME: [
                CallbackQueryHandler(
                    check_username,
                    pattern="^check_username$"
                )
            ],
            WELCOME: [
                CallbackQueryHandler(
                    begin_registration,
                    pattern="^begin$"
                )
            ],
            EDUCATION: [
                CallbackQueryHandler(
                    handle_choice,
                    pattern="^q\\|education\\|"
                )
            ],
            GOVERNORATE: [
                CallbackQueryHandler(
                    handle_choice,
                    pattern="^q\\|governorate\\|"
                )
            ],
            LAPTOP: [
                CallbackQueryHandler(
                    handle_choice,
                    pattern="^q\\|laptop\\|"
                )
            ],
            INFORMATICS: [
                CallbackQueryHandler(
                    handle_choice,
                    pattern="^q\\|informatics\\|"
                )
            ],
            PROGRAMMING: [
                CallbackQueryHandler(
                    handle_choice,
                    pattern="^q\\|programming\\|"
                )
            ],
            REFERRAL: [
                CallbackQueryHandler(
                    handle_choice,
                    pattern="^q\\|referral\\|"
                )
            ],
            OTHER_SOURCE: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    handle_other_source
                )
            ],
            CONFIRMATION: [
                CallbackQueryHandler(
                    handle_confirmation,
                    pattern="^confirm\\|"
                )
            ]
        },
        fallbacks=[],
        allow_reentry=True
    )

    application.add_handler(conversation)

    print("Shaghoof Sanfoor Bot is running...")

    BASE_URL = os.getenv("BASE_URL")
    WEBHOOK_PATH = os.getenv("WEBHOOK_PATH")

    if not BASE_URL or not WEBHOOK_PATH:
        application.run_polling()
    else:
        PORT = int(os.getenv("PORT", 8443))
        SECRET_TOKEN = os.getenv("SECRET_TOKEN")

        # Safely combine them to ensure there is exactly one slash between them
        full_webhook_url = f"{BASE_URL.rstrip('/')}/{WEBHOOK_PATH.lstrip('/')}"

        application.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            secret_token=SECRET_TOKEN,
            webhook_url=full_webhook_url,
            drop_pending_updates=True,
            url_path=WEBHOOK_PATH,
        )


if __name__ == "__main__":
    main()
