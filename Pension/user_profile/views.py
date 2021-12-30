from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from . import serializers
from rest_framework import status
from .serializers import RegistrationSerializer,OtpVerificationSerializer
from rest_framework.generics import GenericAPIView

class RegisterView(GenericAPIView):
    serializer_class = RegistrationSerializer
    def post(self,request):
        serializer =RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = "An otp has sent to the phone number  and verify  your account "
        else:
            data = serializer.errors
        return Response(data)



class OtpVerificationView(GenericAPIView):
    serializer_class = OtpVerificationSerializer
    def post(self,request):

        serializer = OtpVerificationSerializer(data=request.data)
        data ={}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = "phone verified ,please login"
        else:
            data = serializer.errors
        return Response(data)


class ForgotPasswordView(APIView):
    serializer_class = serializers.ForgotPasswordSerializer

    def get(self, request):
        serializer = self.serializer_class(data=request.data)
        email= serializer.validated_data['email']
