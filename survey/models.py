from django.db import models


class Quiz(models.Model):
    quiz_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.quiz_text


class Option(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    option_text = models.CharField(max_length=200)
    vote_count = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text