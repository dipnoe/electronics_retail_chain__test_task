from django.shortcuts import render
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from network.models import NetworkElement
from network.serializers import NetworkElementSerializer


# Create your views here.
class NetworkElementCreateAPIView(CreateAPIView):
    queryset = NetworkElement.objects.all()
    serializer_class = NetworkElementSerializer


class NetworkElementListAPIView(ListAPIView):
    queryset = NetworkElement.objects.all()
    serializer_class = NetworkElementSerializer
    filter_backends = [SearchFilter]
    search_fields = ['provider__contacts__country']


class NetworkElementRetrieveAPIView(RetrieveAPIView):
    queryset = NetworkElement.objects.all()
    serializer_class = NetworkElementSerializer


class NetworkElementUpdateAPIView(UpdateAPIView):
    queryset = NetworkElement.objects.all()
    serializer_class = NetworkElementSerializer


class NetworkElementDestroyAPIView(DestroyAPIView):
    queryset = NetworkElement.objects.all()
    serializer_class = NetworkElementSerializer

