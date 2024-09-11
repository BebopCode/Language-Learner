from django.core.management.base import BaseCommand
import os
from german.models import WordModel
import chardet

class Command(BaseCommand):
    help = 'A custom management command that uses environment variables'
    def detect_encoding(self):
        with open('top10000de.txt', 'rb') as f:
            result = chardet.detect(f.read())
            print(result['encoding'])

    def print_first_entries(self):
        first_ten_entries = WordModel.objects.all()[:10]
        print(first_ten_entries)
    
    def read_entries(self):
        with open('top10000de.txt','r', encoding='iso-8859-9') as file:
            idx = 1
            while True and idx <= 10000:
                
                line= file.readline()
                line=line.replace("\n","")
                word_data = WordModel(
                    rank = idx,
                    word = line
                )
                word_data.save()
                os.system('clear')
                print(f'{idx}, {word_data}')
                idx+=1

    
    def num_entries_database(self):
        entries = WordModel.objects.all()
        print(len(entries))
    
    def delete_database(self):
        WordModel.objects.all().delete()

    def handle(self, *args, **kwargs):
        #self.detect_encoding()
        self.delete_database()
        self.read_entries()
        self.print_first_entries()
        self.num_entries_database()




    