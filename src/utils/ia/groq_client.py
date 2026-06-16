import os

from dotenv import load_dotenv

from groq import AsyncGroq


load_dotenv()


client = AsyncGroq(
    api_key=os.getenv("GROQ_API_KEY")
)