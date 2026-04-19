from google import genai
from dotenv import load_dotenv
import os, io
from gtts import gTTS


# loading the environment variable
load_dotenv()

my_api_key = os.getenv("GEMINI_API_KEY")

# initializing a client
client = genai.Client(api_key=my_api_key)


# note generator
def text_generator(image):

    prompt = f"Convert this image to text"

    response = client.models.generate_content(
        model="gemini-3-flash-preview", contents=[image, prompt]
    )

    return response.text
