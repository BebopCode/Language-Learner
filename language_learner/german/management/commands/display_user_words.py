from django.core.management.base import BaseCommand
from german.models import UserWordsLearned  # Replace with your actual app name

class Command(BaseCommand):
    help = 'Displays all user words'

    def handle(self, *args, **kwargs):
        words = UserWordsLearned.objects.all()
        if not words.exists():
            self.stdout.write(self.style.WARNING('No words found.'))
        else:
            self.stdout.write(self.style.SUCCESS('User Words:'))
            for word in words:
                self.stdout.write(f'- {word.word} (Username: {word.user})')
