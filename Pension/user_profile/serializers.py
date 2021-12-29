from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import ExtendedUserProfile
from rest_framework.response import Response







class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    phone = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username','email', 'password', 'password2','phone' )
        extra_kwargs = {
            'password': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],

        )
        userprofile = ExtendedUserProfile.objects.create(
            user=user,
            phone=validated_data['phone'],

        )
        user.set_password(validated_data['password'])
        user.save()
        userprofile.save()

        return Response({
            'status': True,
             'user':user,
             'userprofile':userprofile,

        })

