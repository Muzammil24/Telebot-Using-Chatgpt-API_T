import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types
import openai
import sys

class Reference:
    """
    A class to store previous response from chatGPT API.
    """
    
    def __init__(self) -> None:
        self.response = ""
        
# Load env variable

load_dotenv()

# Set up OpenAI API Key
openai.api_key = os.getenv("OpenAI_API_KEY")


# Create an object of reference class
reference = Reference()

# Bot token can be obtained via https://t.me/BotFather
TOKEN = os.getenv("TOKEN")


# Model used in chatGPT
MODEL_NAME = "gpt-3.5-turbo"
    
    
# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
diapatcher = Dispatcher(bot) 
    

# Clearing past

def clear_past():
    """
    A function to clear the previous conversation and context
    """
    reference.response = ""
    
    
@diapatcher.message_handler(commands=['start'])
async def welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` command
    """
    
    clear_past()
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram. Developed by Muzammil")


@diapatcher.message_handler(commands=['clear'])
async def clear(message: types.Message):
    """
    To clear previous state
    """

    clear_past()
    await message.reply("I've cleared the past conversation and context.")


@diapatcher.message_handler(commands=['help'])
async def helper(message: types.Message):
    """
    To check the hlp commands
    """
    
    help_command = """
    Hi there, I'm chatGPT integrated into Telegram created by Muzammil.
    Please follow the commands below : 
    
    /start - to start the converastion
    /clear - to clear the conversation
    /help - to get this help menu
    
    """
    await message.reply(help_command)


@diapatcher.message_handler()
async def chatgpt(message: types.Message):
    """
    This handler will process the User's input and generate a response
    """
    
    print(f">>> USER: \n\t{message.text}")
    response = openai.ChatCompletion.create(
        model = MODEL_NAME,
        messages = [
            {"role": "assistant", "content":reference.response},
            {"role":"user", "content":message.text}
            ]
        )
    
    reference.response = response['choices'][0]['message']['content']
    
    print(f">>> chatGPT: \n\t{reference.response}")
    await bot.send_message(chat_id = message.chat.id, text = reference.response)


if __name__ == '__main__':
    executor.start_polling(diapatcher, skip_updates=True)