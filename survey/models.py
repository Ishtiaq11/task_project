from django.db import models
import uuid


class Quiz(models.Model):
    alias = models.UUIDField(
        default=uuid.uuid4, editable=False, db_index=True, unique=True)
    quiz_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.quiz_text

    def options(self):
        if not hasattr(self, '_options'):
            self._options = self.option_set.all()
        return self._options


class Option(models.Model):
    alias = models.UUIDField(
        default=uuid.uuid4, editable=False, db_index=True, unique=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    option_text = models.CharField(max_length=200)
    vote_count = models.IntegerField(default=0)

    def __str__(self):
        return self.option_text