from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models.mango import Mango
from .models.species import Species
from .models.user import User
from .models.genus import Genus


class MangoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mango
        fields = ('id', 'name', 'color', 'ripe', 'owner')

class SpeciesSerializer(serializers.ModelSerializer):
  class Meta:
    model = Species
    fields = ('id', 'name', 'description', 'owner')

class GenusSerializer(serializers.ModelSerializer):
  class Meta:
    model = Genus
    fields = ('id', 'name')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True, write_only=True)

class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old = serializers.CharField(required=True)
    new = serializers.CharField(required=True)
