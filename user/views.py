import json

from django.contrib.auth.models import User
from rest_framework import status, exceptions, decorators
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import login as django_login
from user.permissions.permissions import IsAdminUser, IsNotAdminUser
from drf_yasg.utils import swagger_auto_schema

from user.models import Role
from user.serializers import LoginSerializer, UserSerializer, AuthUserSerializer, UserByIdSerializer, \
    UserUpdateSerializer


class LoginView(APIView):
    # @swagger_auto_schema(method='post', request_body=LoginSerializer)
    @swagger_auto_schema(operation_description="description", request_body=LoginSerializer)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        django_login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, 'status': status.HTTP_200_OK})


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        request.user.auth_token.delete()
        return Response({'data': 'Logout successfully'}, status=status.HTTP_200_OK)


class UserCreate(APIView):
    @swagger_auto_schema(request_body=UserSerializer)
    def post(self, request):
        json_parser = JSONParser()
        data = json_parser.parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthUserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = User.objects.get(pk=request.user.id)
        serializer = AuthUserSerializer(user)
        return Response({'user': serializer.data, 'status': status.HTTP_200_OK})


class UserListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        user = User.objects.all().order_by('first_name')
        serializer = AuthUserSerializer(user, many=True)
        return Response({'users': serializer.data, 'status': status.HTTP_200_OK})


class UserByIdView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist as e:
            raise exceptions.ValidationError(
                {'error': 'User object not found.', 'status': status.HTTP_404_NOT_FOUND})

    def get(self, request, id=None):
        try:
            instance = self.get_object(id)
            user = UserByIdSerializer(instance.id)
            return Response({'user': user.data, 'status': status.HTTP_200_OK})
        except User.DoesNotExist as e:
            return Response({'error': 'User object not found.', 'status': status.HTTP_404_NOT_FOUND})
    @swagger_auto_schema(request_body=UserUpdateSerializer)
    def put(self, request, id=None):
        try:
            instance = self.get_object(id)
            json_parser = JSONParser()
            data = json_parser.parse(request)
            serializer = UserUpdateSerializer(instance, data=data)
            if serializer.is_valid():
                serializer.save()
                user = UserByIdSerializer(instance)
                return Response(
                    {'message': 'User profile updated successfully!', 'user': user.data, 'status': status.HTTP_200_OK})
            return Response(
                {'error': 'Failed to update user profile information', 'status': status.HTTP_406_NOT_ACCEPTABLE})
        except User.DoesNotExist as e:
            return Response({'error': 'User object not found.', 'status': status.HTTP_404_NOT_FOUND})


class UserDeleteAndUpdateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def get_object(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist as e:
            raise exceptions.ValidationError(
                {'error': 'User object not found.', 'status': status.HTTP_404_NOT_FOUND})

    def delete(self, request, id=None):
        try:
            instance = self.get_object(id)
            role = Role.objects.filter(user_id=id).first()
            if request.user.id == instance.id:
                return Response({'message': 'You are logged in, so you cannot delete your own details!',
                                 'status': status.HTTP_406_NOT_ACCEPTABLE})
            role.delete()
            instance.delete()
            return Response({'message': 'Deleting successfully', 'status': status.HTTP_200_OK})
        except User.DoesNotExist as e:
            return Response({'error': 'User object not found.', 'status': status.HTTP_404_NOT_FOUND})
