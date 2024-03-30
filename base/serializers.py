from rest_framework import serializers
from .models import Paragraph, Word, User
from django.contrib.auth.hashers import make_password


class ParagraphSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paragraph
        fields = ["*"]


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ["*"]

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'dob', 'created_at', 'modified_at', 'is_active', 'is_staff', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        # Hash the password before saving
        hashed_password = make_password(password)
        user = User.objects.create(password=hashed_password, **validated_data)
        return user