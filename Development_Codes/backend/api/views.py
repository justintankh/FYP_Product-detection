from django.http import HttpResponse
from django.http.response import JsonResponse
from rest_framework import generics, status
from .serializers import *
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
import json
# Google image search
from .utilies import gis_url
# Create your views here.


class OwnerCreate(generics.CreateAPIView):
    queryset = Owner.objects.all()
    serializer_class = CreateOwnerSerializer


class OwnerList(generics.ListAPIView):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer


class OwnerCreateView(APIView):
    serializer_class = CreateOwnerSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if not self.request.session.exists(self.request.session.session_key):
                self.request.session.create()

            username = serializer.data.get('username')
            queryset = Owner.objects.filter(username=username)

            if queryset.exists():
                owner = queryset[0]
                self.request.session['username'] = owner.username
                self.request.session['code'] = owner.code
                return Response({'Bad request': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                owner = Owner(username=username)
                owner.save()
                self.request.session['username'] = owner.username
                owner = Owner.objects.filter(username=username)[0]
                self.request.session['code'] = owner.code
                return Response(OwnerSerializer(owner).data, status=status.HTTP_201_CREATED)
        return Response({'Bad request': 'Invalid entry'}, status=status.HTTP_400_BAD_REQUEST)


class OwnerLoginView(APIView):
    def post(self, request, format=None):
        data = json.loads(self.request.body)
        if data:
            username = data['username']
            queryset = Owner.objects.filter(username=username)
            if not self.request.session.exists(self.request.session.session_key):
                self.request.session.create()
            if queryset.exists():
                owner = queryset[0]
                self.request.session['username'] = owner.username
                self.request.session['code'] = owner.code
                return Response(OwnerSerializer(owner).data, status=status.HTTP_200_OK)
            else:
                return Response({'Bad request': 'Username not found'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'Bad request': 'Invalid username'}, status=status.HTTP_400_BAD_REQUEST)


class PerishableCreate(generics.CreateAPIView):
    queryset = Perishable.objects.all()
    serializer_class = CreatePerishableSerializer


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
            img_url = gis_url(title)
            exp = serializer.data.get('exp')
            qty = serializer.data.get('qty')
            perishable = Perishable(
                username=username, title=title, img_url=img_url, exp=exp, qty=qty)
            perishable.save()
            return Response(PerishableSerializer(perishable).data, status=status.HTTP_201_CREATED)

        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)


class PerishableCreateTestView(APIView):
    serializer_class = CreatePerishableTestSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = 'justintankh'
            title = serializer.data.get('title')
            img_url = gis_url(title)
            exp = '2021-12-26'
            qty = '1'
            perishable = Perishable(
                username=username, title=title, img_url=img_url, exp=exp, qty=qty)
            perishable.save()
            return Response(PerishableSerializer(perishable).data, status=status.HTTP_201_CREATED)

        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)


class GetUsersPerishableByUsername(APIView):
    lookup_url_kwarg = 'username'

    def get(self, request, format=None):
        # fetch("/api/get_user_perish" + "?username=" + this.username)
        # username = self.request.session['username']
        username = request.GET.get(self.lookup_url_kwarg)
        if username != None:
            perishables = Perishable.objects.filter(username=username)
            if len(perishables) > 0:
                data = perishables.values("username", "p_code",
                                          "title", "img_url", "qty", "rtr_date", "exp",)
                return Response(data, status=status.HTTP_200_OK)
            return Response({'Perishables not found': 'Invalid username.'}, status.HTTP_404_NOT_FOUND)
        return Response({'Bad Request': 'Username parameter not found in request'}, status=status.HTTP_400_BAD_REQUEST)


class retrieve_username(APIView):
    def get(self, request, format=None):
        return Response({'username': self.request.session['username']}, status=status.HTTP_200_OK)


def username_by_code(code):
    username = Owner.objects.filter(code=code)[0].username
    return username


class GetUsersPerishableByCode(APIView):
    lookup_url_kwarg = 'code'

    def get(self, request, format=None):
        # fetch("/api/get_user_perish" + "?username=" + this.username)
        # username = self.request.session['username']
        code = request.GET.get(self.lookup_url_kwarg)
        if code != None:
            username = username_by_code(code)
            perishables = Perishable.objects.filter(username=username)
            if len(perishables) > 0:
                data = perishables.values("username", "p_code",
                                          "title", "img_url", "qty", "rtr_date", "exp",)
                return Response(data, status=status.HTTP_200_OK)
            return Response({'Perishables not found': 'Invalid code.'}, status.HTTP_404_NOT_FOUND)
        return Response({'Bad Request': 'Code parameter not found in request'}, status=status.HTTP_400_BAD_REQUEST)


class PerishableDeleteView(APIView):
    serializer_class = DeletePerishableSerializer

    def post(self, request, format=None):
        if request.data['p_code']:
            p_code = request.data['p_code']
            Perishables = Perishable.objects.filter(p_code=p_code)
            if len(Perishables) > 0:
                perishable = Perishables[0]
                perishable.delete()
                return Response({'Message': 'Successfully deleted'}, status=status.HTTP_200_OK)
        return Response({'Message': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)


class PerishableUpdateView(APIView):
    serializer_class = UpdatePerishableSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            p_code = request.data['p_code']
            qty = request.data['qty']
            exp = request.data['exp']
            Perishables = Perishable.objects.filter(p_code=p_code)
            if len(Perishables) > 0:
                perishable = Perishables[0]
                perishable.qty = qty
                perishable.exp = exp
                perishable.save()
                return Response({'Message': 'Successfully updated'}, status=status.HTTP_200_OK)
        return Response({'Message': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)
