from django.db import models
from django.contrib.auth.models import User
 
class WordModel(models.Model):
    rank = models.IntegerField()
    word = models.CharField(max_length=100)
    meaning = models.CharField(max_length=100,null=True)

    def __str__(self) -> str:
        return f"Rank- {self.rank} Word- {self.word} Meaning - {self.meaning}"
    

class UserWordsLearned(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        to_field='username'
    )
    word = models.CharField(max_length=100)  # A column to store the word learned

    class Meta:
        unique_together = ['user', 'word']  # Ensures a user can't have duplicate word entries

    def __str__(self):
        return f'{self.user.username} - Word: {self.word}'
