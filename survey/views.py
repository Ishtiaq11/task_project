from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from drf_yasg.utils import swagger_auto_schema
from django.conf import settings


from .models import Option, Quiz, Comment
from .serializers import (OptionSerializer, QuizDetailPageSerializer,
                          QuizListPageSerializer, QuizResultPageSerializer,
                          VoteSerializer, CommentSerializer)

from .celery_task import send_comments_email_task



"""
To provide permission uncomments the 
authentication and permission class.
"""
@swagger_auto_schema(methods=['post',], request_body=QuizListPageSerializer)
@api_view(['GET', 'POST'])
# @authentication_classes([TokenAuthentication,])
# @permission_classes([IsAuthenticated,])
def quizzes_view(request):
    if request.method == 'GET':
        paginator = PageNumberPagination()
        paginator.page_size = 10
        quizs = Quiz.objects.all()
        result_page = paginator.paginate_queryset(quizs, request)
        serializer = QuizListPageSerializer(result_page, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = QuizListPageSerializer(data=request.data)
        if serializer.is_valid():
            if not request.user.is_anonymous: 
                quiz = serializer.save(created_by=request.user)
            else:
               quiz = serializer.save() 
            return Response(QuizListPageSerializer(quiz).data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(methods=['patch',], request_body=QuizDetailPageSerializer)
@api_view(['GET', 'PATCH', 'DELETE'])
def quiz_detail_view(request, alias):
    quiz = get_object_or_404(Quiz, alias=alias)
    if request.method == 'GET':
        serializer = QuizDetailPageSerializer(quiz)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = QuizDetailPageSerializer(quiz,
                                              data=request.data,
                                              partial=True)
        if serializer.is_valid():
            if not request.user.is_anonymous: 
                quiz = serializer.save(created_by=request.user)
            else:
               quiz = serializer.save() 
            return Response(QuizDetailPageSerializer(quiz).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        quiz.delete()
        return Response("Quiz deleted", status=status.HTTP_204_NO_CONTENT)

@swagger_auto_schema(methods=['post',], request_body=OptionSerializer)
@api_view(['POST'])
def options_view(request, alias):
    quiz = get_object_or_404(Quiz, alias=alias)
    serializer = OptionSerializer(data=request.data)
    if serializer.is_valid():
        option = serializer.save(quiz=quiz)
        return Response(OptionSerializer(option).data,
                        status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(methods=['patch',], request_body=VoteSerializer)
@api_view(['PATCH'])
def vote_view(request, alias):
    quiz = get_object_or_404(Quiz, alias=alias)
    serializer = VoteSerializer(data=request.data)
    if serializer.is_valid():
        option = get_object_or_404(Option,
                                   pk=serializer.validated_data['option_id'])
        option.vote_count += 1
        option.save()
        return Response("Voted")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def quiz_result_view(request, alias):
    quiz = get_object_or_404(Quiz, alias=alias)
    serializer = QuizResultPageSerializer(quiz)
    return Response(serializer.data)


def send_email(name, email, quiz, comment):
        send_comments_email_task.delay(name, email, quiz, comment)

class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'alias'
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        alias = self.kwargs.get(self.lookup_field)
        quiz = get_object_or_404(Quiz, alias=alias)
        serializer = CommentSerializer(data=self.request.data)
        if serializer.is_valid():
            comment = serializer.save(content_object=quiz)
            admin_mail = getattr(settings, "ADMIN_MAIL", None)
            #username, admin mail, quiz text, comment_text
            send_email(str(self.request.user), admin_mail, quiz.quiz_text, comment.text )
            return Response(CommentSerializer(comment).data,
                        status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
