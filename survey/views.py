from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Option, Quiz
from .serializers import (OptionSerializer, QuizDetailPageSerializer,
                          QuizListPageSerializer, QuizResultPageSerializer,
                          VoteSerializer)


@api_view(['GET', 'POST'])
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
            quiz = serializer.save()
            return Response(QuizListPageSerializer(quiz).data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
            quiz = serializer.save()
            return Response(QuizDetailPageSerializer(quiz).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        quiz.delete()
        return Response("Quiz deleted", status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def options_view(request, alias):
    quiz = get_object_or_404(Quiz, alias=alias)
    serializer = OptionSerializer(data=request.data)
    if serializer.is_valid():
        option = serializer.save(quiz=quiz)
        return Response(OptionSerializer(option).data,
                        status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

