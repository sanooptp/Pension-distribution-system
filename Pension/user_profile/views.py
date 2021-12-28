from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from .serializers import RegistrationSerializer
from rest_framework.generics import GenericAPIView


class RegisterView(GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self,request):
        serializer =RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = "successfully registered a new user"

        else:
            data = serializer.errors
        return Response(data)

