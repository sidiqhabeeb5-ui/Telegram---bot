import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Your bot token (already added)
BOT_TOKEN = "7701592611:AAHGpBuu1L5KDGdhtOn-u14fZLyM9bFrADw"

# In-memory storage (you can later connect this to a database)
users = {}
referrals = {}
tasks = {
    "Join Group 1": "https://chat.whatsapp.com/KovPtm4hikeIgpihTLUI8T",
    "Join Group 2": "https://chat.whatsapp.com/CHqeegifglOGrbgSjX9XHf",
    "Join Channel": "https://whatsapp.com/channel/0029Vb7LctaCcW4nu161W91p"
}

# Start command
async def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id not in users:
        users[user_id] = {"balance": 0, "referrals": 0, "tasks_done": []}

        # Handle referral
        if context.args:
            referrer_id = int(context.args[0])
            if referrer_id in users and referrer_id != user_id:
                users[referrer_id]["balance"] += 50
                users[referrer_id]["referrals"] += 1

    referral_link = f"https://t.me/{context.bot.username}?start={user_id}"
    message = (
        f"👋 Welcome {update.effective_user.first_name}!\n\n"
        f"💰 Balance: ₦{users[user_id]['balance']}\n"
        f"👥 Referrals: {users[user_id]['referrals']}\n\n"
        f"🔗 Your referral link:\n{referral_link}"
    )
    await update.message.reply_text(message)

# Task command
async def tasks_command(update: Update, context: CallbackContext):
    keyboard = []
    for task_name, link in tasks.items():
        keyboard.append([InlineKeyboardButton(task_name, url=link)])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📋 Complete these tasks to earn ₦50 each:", reply_markup=reply_markup)

# Balance command
async def balance(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    balance = users.get(user_id, {}).get("balance", 0)
    referrals_count = users.get(user_id, {}).get("referrals", 0)
    await update.message.reply_text(
        f"💰 Your balance: ₦{balance}\n👥 Referrals: {referrals_count}"
    )

# Withdraw command
async def withdraw(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    balance = users.get(user_id, {}).get("balance", 0)
    if balance >= 500:
        users[user_id]["balance"] -= 500
        await update.message.reply_text("✅ Withdrawal request sent! You will be paid manually.")
    else:
        await update.message.reply_text("❌ Minimum withdrawal is ₦500.")

# Main function
def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("tasks", tasks_command))
    application.add_handler(CommandHandler("balance", balance))
    application.add_handler(CommandHandler("withdraw", withdraw))

    application.run_polling()

if __name__ == "__main__":
    main()
