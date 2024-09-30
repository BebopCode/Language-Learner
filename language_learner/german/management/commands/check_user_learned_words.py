from django.core.management.base import BaseCommand
from german.models import UserWordsLearned  # Update this to your actual model
from django.contrib.auth.models import User   # If User is from another app, adjust accordingly

class Command(BaseCommand):
    help = 'Check if a user has learned a specific word'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username of the user')
        parser.add_argument('word', type=str, help='Word to check if learned by the user')

    def handle(self, *args, **kwargs):
        username = kwargs['username']
        word = kwargs['word']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User "{username}" does not exist.'))
            return

        # Check if the user has learned the word
        if UserWordsLearned.objects.filter(user=user, word=word).exists():
            self.stdout.write(self.style.SUCCESS(f'Yes, the user "{username}" has learned the word "{word}".'))
        else:
            self.stdout.write(self.style.WARNING(f'No, the user "{username}" has not learned the word "{word}".'))
