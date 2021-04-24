import uuid

from django.db import models
from django.contrib.auth.models import User

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey


class Comment(models.Model):
    text = models.TextField(null=False, blank=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.text[:20]

class Quiz(models.Model):
    alias = models.UUIDField(
        default=uuid.uuid4, editable=False, db_index=True, unique=True)
    quiz_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    comments = GenericRelation(Comment, related_query_name="quiz")
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


