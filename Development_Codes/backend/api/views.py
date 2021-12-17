from re import T
from django.http import HttpResponse
from django.http.response import JsonResponse
from rest_framework import generics, status
from .serializers import *
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core import serializers

import json


def obj_dict(obj):
    return obj.__dict__

# Create your views here.


class OwnerCreate(generics.CreateAPIView):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer


class OwnerList(generics.ListAPIView):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer


class OwnerCreateView(APIView):
    serializer_class = CreateOwnerSerializer

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.data.get('username')
            # host = self.request.session.session_key
            queryset = Owner.objects.filter(username=username)
            if queryset.exists():
                owner = queryset[0]
                self.request.session['username'] = owner.username
                return Response(OwnerSerializer(owner).data, status=status.HTTP_200_OK)
            else:
                owner = Owner(username=username)
                owner.save()
                self.request.session['username'] = owner.username
                return Response(OwnerSerializer(owner).data, status=status.HTTP_201_CREATED)

        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)


class PerishableCreate(generics.CreateAPIView):
    queryset = Perishable.objects.all()
    serializer_class = PerishableSerializer


class PerishableList(generics.ListAPIView):
    queryset = Perishable.objects.all()
    serializer_class = PerishableSerializer


class PerishableCreateView(APIView):
    serializer_class = CreatePerishableSerializer

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = self.request.session['username']
            title = serializer.data.get('title')
            exp = serializer.data.get('exp')
            perishable = Perishable(username=username, title=title, exp=exp)
            perishable.save()
            return Response(PerishableSerializer(perishable).data, status=status.HTTP_201_CREATED)

        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)


class GetUsersPerishable(APIView):
    serializer_class = PerishableSerializer
    lookup_url_kwarg = 'username'

    def get(self, request, format=None):
        # fetch("/api/get_user_perish" + "?username=" + this.username)
        # username = self.request.session['username']
        username = request.GET.get(self.lookup_url_kwarg)
        if username != None:
            perishables = Perishable.objects.filter(username=username)
            if len(perishables) > 0:
                data = perishables.values(
                    "title", "img_url", "qty", "rtr_date", "exp",)
                return Response(data, status=status.HTTP_200_OK)
            return Response({'Perishables not found': 'Invalid Room Code.'}, status.HTTP_404_NOT_FOUND)
        return Response({'Bad Request': 'Username parameter not found in request'}, status=status.HTTP_400_BAD_REQUEST)
