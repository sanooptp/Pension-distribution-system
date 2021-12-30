from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from . import serializers
from rest_framework import status
from .serializers import RegistrationSerializer,OtpVerificationSerializer
from rest_framework import status, generics
from rest_framework.response import Response
from .serializers import ForgotPasswordSerializer, RegistrationSerializer, SetNewPasswordSerializer
from rest_framework.generics import GenericAPIView
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.core.mail import send_mail
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError

class RegisterView(GenericAPIView):
    serializer_class = RegistrationSerializer
    def post(self,request):
        serializer =RegistrationSerializer(data=request.data)

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
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

class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            redirect_url = serializer.data.get('redirect_url')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(
                request=request).domain
            relativeLink = reverse('password-token-verify', kwargs={'uidb64': uidb64, 'token': token})
            absurl = 'http://'+current_site + relativeLink
            email_body = 'Hello, \n Use link below to reset your password  \n' + absurl
            # data = {'email_body': email_body, 'to_email': user.email,
            #         'email_subject': 'Reset your passsword'}
            send_mail(
                'Pension Distribution System- Reset your password',
                email_body,
                None,
                [user.email],
                fail_silently=False,
            )
        else:
            data = {'response': 'Email does not registerd with us'}
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)



class ResetPassword(APIView):
    serializer_class = SetNewPasswordSerializer

    def post(self, request, uidb64, token):
        serializer= self.serializer_class(data=request.data)
        if serializer.is_valid():
                password = serializer.data.get('password')
                try:
                    uid = force_str(urlsafe_base64_decode(uidb64))
                    user = User.objects.get(pk=uid)
                except(TypeError, ValueError, OverflowError, User.DoesNotExist):
                    user = None
                if user is not None and PasswordResetTokenGenerator().check_token(user, token):
                    user.set_password(password)
                    user.save()
                    data = {'response': 'Password reset successfully'}
                else:
                    return Response({'response': 'Link Expired'}, status=status.HTTP_404_NOT_FOUND)
        else:
            data = serializer.errors
        return Response(data, status=status.HTTP_200_OK)
            # return Response({'response': 'valid token'}, status=status.HTTP_200_OK)
            
