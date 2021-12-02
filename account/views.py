from django.shortcuts import render
from account.permissions import IsActivePermission
from .serializers import RegisterSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .models import CustomUser


class RegisterView(APIView):

    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                "Successfully registred!", 201
            )


class LogoutView(APIView):
    permissions_classes = [IsActivePermission]

    def post(self, request):
        user = request.user
        Token.objects.filter(user=user).delete()
        return Response("You have successfully signed out")


class ActivationView(APIView):

    def get(self, request, email, activation_code):
        user = CustomUser.objects.filter(
            email=email,
            activation_code=activation_code
        ).first()
        msg_ = (
            "User does not exist",
            "Activated!"
        )
        if not user:
            return Response(msg_, 400)
        user.activation_code = ''
        user.is_active = True
        user.save()
        return Response(msg_[-1], 200)
