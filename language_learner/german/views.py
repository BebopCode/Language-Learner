from django.shortcuts import render
from rest_framework import generics
import os
import numpy as np
from .models import WordModel
from .serializers import WordModelSerializer
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()
genai.configure(api_key=os.getenv('API_KEY'))

class WordCreateView(generics.ListAPIView):
    serializer_class = WordModelSerializer
    def sample_words(self, offset=1):
        words = []
        while len(words) != 5:
            lmbda = 0.001/offset
            sampled_num = int(np.random.exponential(scale=1/lmbda))
            if sampled_num > 0 and sampled_num < 10000:
                words.append(WordModel.objects.get(rank=sampled_num))
        return words
    


    def word_LLM(self, word):
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(
            f'Give me the meaning of the word {word} in German and give only two sentences with examples',
            generation_config = genai.GenerationConfig(
                max_output_tokens=200,
                temperature=0.1,
                )
        )

        print(response.text)

    def handle(self, *args, **kwargs):
        
        for i in range(1,10):
            words = self.sample_words(i)
            print(words)
        #word_test = words[4]
        #print('word is', word_test.word)
        #self.word_LLM(word_test.word)
        #self.detect_encoding()
    def get_queryset(self):
        words = self.sample_words()
        return words