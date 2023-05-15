import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, InlineQueryHandler

# Replace with your bot token
TOKEN = 'replace_bot_token_here'

# Initialize the updater and bot
updater = Updater(token=TOKEN, use_context=True)
bot = updater.bot

# Define the function to handle the /start and /help commands
def start_handler(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Hello! I am CodeBot. To use me, send me a special code.")

# Define the function to handle user input
def code_handler(update, context):
    # Replace with the path to your file containing the special codes
    codes_file_path = 'put_file_path_here'
    
    # Read the special codes from the file
    with open(codes_file_path, 'r') as f:
        codes = f.read().splitlines()
    
    # Get the user input
    user_input = update.message.text.strip()
    
    if user_input in codes:
        # Generate a one-time invite link for the group
        group_id = 'put_group_id_here'
        invite_link = bot.export_chat_invite_link(chat_id=group_id)
        
        # Send the link as a message to the user who sent the correct code
        user_id = update.effective_chat.id
        message_text = f"Congratulations! Here is your invite link:"
        
        # Create a button that opens the invite link and expires after 1 use or 5 minutes
        keyboard = [[InlineKeyboardButton("Join Group", url=invite_link)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Send the message with the button
        message = context.bot.send_message(chat_id=user_id, text=message_text, reply_markup=reply_markup)
        context.bot.delete_message(chat_id=message.chat_id, message_id=message.message_id)
		
        # Log the used code to a file
        with open('used_codes.txt', 'a') as f:
            f.write(user_input + '\n')
        
        # Remove the used code from the list of valid codes
        codes.remove(user_input)
        with open(codes_file_path, 'w') as f:
            f.write('\n'.join(codes))
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Sorry, that is not a valid code.")

# Define the function to handle button presses
def button_handler(update, context):
    query = update.inline_query.query
    
    if query == 'delete':
        # Delete the message that contained the button
        context.bot.delete_message(update.inline_query.from_user.id, update.inline_query.message.id)

# Set up the dispatcher to handle commands, user input, and button presses
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('start', start_handler))
dispatcher.add_handler(CommandHandler('help', start_handler))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, code_handler))
dispatcher.add_handler(CallbackQueryHandler(button_handler))

# Start the bot
updater.start_polling()
updater.idle()
