from rest_framework import serializers
from .models import Owner, Perishable


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = ('id', 'username', 'code')


class CreateOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = ('username',)


class UpdateOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perishable
        fields = ('username',)


class PerishableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perishable
        fields = ('id', 'username', 'title',
                  'img_url', 'qty', 'rtr_date', 'exp',)


class CreatePerishableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = ('title', 'exp',)


class UpdatePerishableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perishable
        fields = ('code', 'qty', 'exp',)
