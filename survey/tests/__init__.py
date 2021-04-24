import random
import factory
from django.utils import timezone
from django.contrib.auth.models import User

from survey.models import Comment, Quiz, Option


class CommentFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Comment
    
    text = factory.Faker('first_name')
    
class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User
    email = 'rakibulbasharrakib@gmail.com'
    username = 'testuser'
    password = 'rakibvai'
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('first_name')


class QuizFactory(factory.django.DjangoModelFactory):
    
    class Meta:
        model = Quiz

    quiz_text = factory.Faker('first_name')
    pub_date =  factory.Faker('date_time', tzinfo=timezone.utc)
   

class OptionFactory(factory.django.DjangoModelFactory):
    
    class Meta:
        model = Option

    option_text = factory.Faker('first_name')
    vote_count = random.randrange(1, 10)

