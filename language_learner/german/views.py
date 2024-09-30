from django.shortcuts import render
from rest_framework import generics
import os
import numpy as np
from .models import WordModel, UserWordsLearned
from .serializers import WordModelSerializer
import jwt
from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import google.generativeai as genai
from dotenv import load_dotenv
from django.http import JsonResponse
from .decorators import google_auth_required
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator

load_dotenv()
genai.configure(api_key=os.getenv('API_KEY'))
client_id=os.getenv('CLIENT_ID')


@method_decorator(google_auth_required, name='dispatch')
class ReturnMeaning(APIView):

    def word_LLM(self, word):
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(
            f'Give me the meaning of the word {word} in German and give only two sentences with examples',
            generation_config = genai.GenerationConfig(
                max_output_tokens=200,
                temperature=0.1,
                )
        )
        cleaned_response = response.text.replace('*','')
        return cleaned_response
        print(response.text)

    def post(self, request, *args, **kwargs):
        word = request.data.get('word', None)

        if word:
            meaning = self.word_LLM(word)
            print(meaning)
            response_data = {
                "original_word": word,
                "meaning": meaning,
           }

            # Return the response data with a 200 OK status
            return Response(response_data, status=status.HTTP_200_OK)

        # Return an error response if the word is missing
        return Response({"error": "No word provided"}, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(google_auth_required, name='dispatch')
class RemoveUserData(APIView):

    def delete(self, request, *args, **kwargs):
        email = self.request.user_info.get('email')
        try:
            user = User.objects.get(username=email)  # Use username or User's unique identifier
        except User.DoesNotExist:
            return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

        words_learned = UserWordsLearned.objects.filter(user=user)
        words_learned.delete()
        
        return Response({"message": "Deleted"}, status=status.HTTP_200_OK)

@method_decorator(google_auth_required, name='dispatch')
class WordsLearnedCountView(APIView):
    def get(self, request, *args, **kwargs):
        email = self.request.user_info.get('email')
        try:
            user = User.objects.get(username=email)  # Use username or User's unique identifier
        except User.DoesNotExist:
            return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        words_learned_count = UserWordsLearned.objects.filter(user=user).count()
        return Response({"word_count": words_learned_count}, status=status.HTTP_200_OK)       


@method_decorator(google_auth_required, name='dispatch')
class WordCreateView(generics.ListAPIView):
    serializer_class = WordModelSerializer
    def sample_words(self, offset=1):
        words = []
        user_name = self.request.user_info.get('email')
        print(f'User email: {user_name}')
        while len(words) != 5:
            lmbda = 0.001/offset
            sampled_num = int(np.random.exponential(scale=1/lmbda))
            if sampled_num > 0 and sampled_num < 10000:
                word = WordModel.objects.get(rank=sampled_num)
                if not self.check_learned(word, user_name):
                    words.append(word)
        return words
    
    def check_learned(self, word, user_name):
        print(f'{user_name}, {word}')
        try:
            user = User.objects.get(username=user_name)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User "{user_name}" does not exist.'))
            return
        learned = UserWordsLearned.objects.filter(user=user, word=word).exists()
        return learned



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
    
@method_decorator(google_auth_required, name='dispatch')
class WordUpdateView(generics.CreateAPIView):  # Use CreateAPIView for POST requests
    queryset = UserWordsLearned.objects.all()

    def create(self, request, *args, **kwargs):
        email = self.request.user_info.get('email')
        words = request.data.get('words', [])
        try:
            user = User.objects.get(username=email)  # Use username or User's unique identifier
        except User.DoesNotExist:
            return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)        
        instances = []
        for word in words:
            print(f'word is {word}')
            if self.check_word_exists(user, word):
            # Create an instance for each word with the corresponding username
                instances.append(UserWordsLearned(word=word, user=user))

        # Bulk create for efficiency
        UserWordsLearned.objects.bulk_create(instances) 
        return Response({"message": f"Words added successfully{instances}"}, status=status.HTTP_201_CREATED)
        

    def check_word_exists(self, user_name, word):
        word_exists = WordModel.objects.filter(word=word).exists()
        learned = UserWordsLearned.objects.filter(user=user_name, word=word).exists()
        print(f'word{word},user_name{user_name}word_exists{word_exists} learned{learned}')
        return word_exists and not learned




    
class GoogleLoginView(APIView):
    def post(self, request):
        # Extract the ID token from the request (sent by the Vue frontend)
        id_token_str = request.data.get('id_token')
        if not id_token_str:
            return Response({'error': 'ID token not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Verify and decode the token using Google's public keys
            decoded_token = id_token.verify_oauth2_token(
                id_token_str, 
                requests.Request(), 
                audience=client_id
            )
            
            # Extract user information, such as the email from the decoded token
            email = decoded_token.get('email')
            if not email:
                return Response({'error': 'Email not found in token'}, status=status.HTTP_400_BAD_REQUEST)
            
            # You can now use the email to authenticate or create a new user in your system
            # Example: Check if user exists in DB or create a new user
            user, created = User.objects.get_or_create(username=email, defaults={'email': email})
            
            # Return a success response with user info
            return Response({
                'message': 'User authenticated successfully',
                'email': email,
                'created': created
            }, status=status.HTTP_200_OK)
        
        except ValueError as e:
            # Token is invalid
            return Response({'error': 'Invalid ID token'}, status=status.HTTP_401_UNAUTHORIZED)