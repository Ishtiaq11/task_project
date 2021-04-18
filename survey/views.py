from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Quiz, Option
from .serializers import QuizListPageSerializer, QuizDetailPageSerializer, OptionSerializer, VoteSerializer, QuizResultPageSerializer



@api_view(['GET', 'POST'])
def quizzes_view(request):
    if request.method == 'GET':
        quizs = Quiz.objects.all()
        serializer = QuizListPageSerializer(quizs, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = QuizListPageSerializer(data=request.data)
        if serializer.is_valid():
            quiz = serializer.save()
            return Response(QuizListPageSerializer(quiz).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH', 'DELETE'])
def quiz_detail_view(request, alias):
    quiz = get_object_or_404(Quiz, alias=alias)
    if request.method == 'GET':
        serializer = QuizDetailPageSerializer(quiz)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = QuizDetailPageSerializer(quiz, data=request.data, partial=True)
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
        return Response(OptionSerializer(option).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def vote_view(request, alias):
    quiz = get_object_or_404(Quiz, alias=alias)
    serializer = VoteSerializer(data=request.data)
    if serializer.is_valid():
        option = get_object_or_404(Option, pk=serializer.validated_data['option_id'])
        option.vote_count += 1
        option.save()
        return Response("Voted")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def quiz_result_view(request, alias):
    quiz = get_object_or_404(Quiz, alias=alias)
    serializer = QuizResultPageSerializer(quiz)
    return Response(serializer.data)