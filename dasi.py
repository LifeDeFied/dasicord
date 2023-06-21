import os
import discord
import openai
from dotenv import load_dotenv
from langdetect import detect

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')
discord_bot_token = os.getenv('DISCORD_BOT_TOKEN')

#Define the intents that your will use
intents = discord.Intents.default()
intents.members = True

# Create a new client with the specified intents
client = discord.Client(intents=intents)

# Set up OpenAI credentials
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define the FAQ responses
faq_responses = {
    "What is LifeDeFied?": "LifeDeFied is a blockchain-based platform that provides advanced security solutions for individuals and businesses.",
    "How does LifeDeFied work?": "LifeDeFied uses advanced cryptographic techniques to secure data and transactions on the blockchain.",
    "What are the benefits of using LifeDeFied?": "Some benefits of using LifeDeFied include enhanced security, reduced risk of fraud and data breaches, and greater transparency and accountability.",
    "How can I get started with LifeDeFied?": "You can get started with LifeDeFied by visiting our website and creating an account. From there, you can explore our platform and learn more about our services.",
    "Is LifeDeFied secure?": "Yes, LifeDeFied is highly secure and uses advanced cryptographic techniques to protect data and transactions on the blockchain.",
    "Can LifeDeFied be used for personal as well as business purposes?": "Yes, LifeDeFied is designed to meet the needs of both individuals and businesses, and provides advanced security solutions for a wide range of use cases.",
    "What sets LifeDeFied apart from other blockchain security platforms?": "LifeDeFied stands out from other blockchain security platforms due to its advanced cryptographic techniques, user-friendly interface, and commitment to providing exceptional customer support.",
    "🌼": "These are hidden collectibles found on the platform and mobile app that unlock rarity items." 
}

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

    if message.content.startswith("!dasi"):
        # Remove the "/dasi" prefix from the message to get the query
        query = message.content[6:]
        
        # Use OpenAI to generate a response to the query
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=query,
            temperature=0.3,
            max_tokens=100,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        
        # Extract the response text from the OpenAI response
        dasi_response = response.choices[0].text.strip()
        
        # Send the Dasi response back to the channel as a message from the bot
        await message.channel.send(dasi_response)

    if message.content.startswith("!faq"):
        # Remove the !FAQ prefix from the message to get the question
        question = message.content[5:]
        
        # Check if the question is in the FAQ responses
        if question in faq_responses:
            # Send the FAQ response back to the channel as a message from the bot
            await message.channel.send(faq_responses[question])
        else:
            # If the question is not in the FAQ responses, send a message indicating that the bot doesn't know the answer
            await message.channel.send("I'm sorry, I don't know the answer to that question.")
        
# Run the Discord bot with the token from the environment variables
client.run(os.getenv("DISCORD_BOT_TOKEN"))
