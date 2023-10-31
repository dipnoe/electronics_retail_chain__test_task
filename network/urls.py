from django.urls import path
from rest_framework import routers

from network.apps import NetworkConfig
from network.views import NetworkElementCreateAPIView, NetworkElementListAPIView, NetworkElementRetrieveAPIView, \
    NetworkElementUpdateAPIView, NetworkElementDestroyAPIView

app_name = NetworkConfig.name

urlpatterns = [
    path('create/', NetworkElementCreateAPIView.as_view(), name='network_element_create'),
    path('', NetworkElementListAPIView.as_view(), name='network_element_list'),
    path('<int:pk>/', NetworkElementRetrieveAPIView.as_view(), name='network_element_retrieve'),
    path('update/<int:pk>/', NetworkElementUpdateAPIView.as_view(), name='network_element_update'),
    path('delete/<int:pk>/', NetworkElementDestroyAPIView.as_view(), name='network_element_destroy'),
]
