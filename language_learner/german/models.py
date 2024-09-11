from django.db import models

class WordModel(models.Model):
    rank = models.IntegerField()
    word = models.CharField(max_length=100)
    meaning = models.CharField(max_length=100,null=True)

    def __str__(self) -> str:
        return f"Rank- {self.rank} Word- {self.word} Meaning - {self.meaning}"
    
