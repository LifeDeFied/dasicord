import os
import discord
import openai
from dotenv import load_dotenv
from langdetect import detect

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')
discord_bot_token = os.getenv('DISCORD_BOT_TOKEN')

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user.name}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith("!translate"):
        # Remove the !translate prefix from the message to get the original text
        text = message.content[10:]
        
        # Detect the language of the input text
        input_lang = detect(text)
        
        # Use OpenAI to generate a translated response
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt="Translate from {} to English: {}".format(input_lang, text),
            temperature=0.3,
            max_tokens=100,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        
        # Extract the translated text from the OpenAI response
        translated_text = response.choices[0].text.strip()
        
        # Send the translated text back to the channel as a message from the bot
        await message.channel.send(translated_text)

# Run the Discord bot with the token from the environment variables
client.run(os.getenv("DISCORD_BOT_TOKEN"))