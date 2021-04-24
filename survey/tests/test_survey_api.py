import json 

from common.test_case import CloudlyTestCase
from django.urls import reverse
from django.contrib.auth.models import User


from ..tests import QuizFactory, UserFactory
from survey.models import Quiz
from rest_framework import status

class QuizListApiTest(CloudlyTestCase):
    # ================================
    # Basic setup  
    # ================================
    url = reverse('quizzes_view')

    def setUp(self):
        super(CloudlyTestCase, self).setUp()

    def test_quiz_list_get(self):
        # ===========================================
        # Check Quiz List get successfully or not 
        # ===========================================
        _ = QuizFactory.create_batch(4)


        request = self.client.get(self.url)

        self.assertSuccess(request)
        self.assertEqual(len(request.data), 4)


    def test_quiz_list_post(self):
        # ===========================================
        # Check quiz data saved successfully or not 
        # ===========================================

        data = {
            'quiz_text': 'Is it hot today?',
            'pub_date': '2021-02-18T00:00'            
        }

        request = self.client.post(self.url, data)
        self.assertCreated(request)

        self.assertEqual(request.data['quiz_text'], data['quiz_text'])
        
class QuizDetailsApiTest(CloudlyTestCase):
    # ================================
    # Basic setup  
    # ================================
    def setUp(self):
        super(CloudlyTestCase, self).setUp()

        # Set an quiz
        self.quiz = QuizFactory()
        
        #set the url
        self.url = reverse('quiz_detail_view', args=[self.quiz.alias])

    def test_quiz_details_get(self):
        # ================================
        # Check quiz get Sucessfully or not  
        # ================================
        request = self.client.get(self.url)

        self.assertSuccess(request)
        self.assertEqual(request.data['id'], self.quiz.id)

    def test_quiz_details_put(self):
        # ================================
        # Check quiz update  
        # ================================
        data = {
            'quiz_text': 'Is it Cold today?',
            'pub_date': '2021-02-18T00:00'  
        }

        request = self.client.patch(self.url, data=json.dumps(dict(data)),
                                    content_type='application/json')

        self.assertSuccess(request)
        self.assertEqual(request.data['quiz_text'], data['quiz_text'])

    def test_quiz_details_delete(self):
        # ================================
        # Check quiz delete  
        # ================================
        request = self.client.get(self.url)
        self.assertEqual(Quiz.objects.count(), 1)

        request = self.client.delete(self.url)
        self.assertTrue(status.is_success(request.status_code))

        request = self.client.delete(self.url)
        self.assertFalse(status.is_success(request.status_code))