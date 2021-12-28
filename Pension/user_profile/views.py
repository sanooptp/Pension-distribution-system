from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from . import serializers

class ForgotPasswordView(APIView):
    serializer_class = serializers.ForgotPasswordSerializer

    def get(self, request):
        serializer = self.serializer_class(data=request.data)
        email= serializer.validated_data['email']
