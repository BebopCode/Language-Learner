from django.core.management.base import BaseCommand
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv('API_KEY'))
word = 'los'

class Command(BaseCommand):
    help = 'A custom management command that uses environment variables'

    def handle(self, *args, **kwargs):
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(
            f'Give me the meaning of the word {word} in German and give only two sentences with examples',
            generation_config = genai.GenerationConfig(
                max_output_tokens=200,
                temperature=0.1,
                )
        )

        print(response.text)
    