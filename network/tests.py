import datetime

import jwt
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from network.models import NetworkElement, Contact, Product
from users.models import User


# Create your tests here.
class NetworkElementTestCase(APITestCase):

    def setUp(self):
        # Create a test user for authentication
        self.user = User.objects.create(email='test@test.com', is_active=True)
        self.user.set_password('12345')
        self.user.save()

        # Create a test contact
        self.contacts = Contact.objects.create(
            email='contact@test.com',
            country='Canada',
            city='Quebec',
            street='Rue Fortin',
            building_num=235
        )

        # Create a test product
        self.product = Product.objects.create(
            name='Test name',
            model='Test model',
            launch_date=datetime.date.today()
        )

        # Create a test network element
        self.network_element = NetworkElement.objects.create(
            name='Test network element',
            contacts=self.contacts,
            product=self.product,
            level='0'
        )

    def test_create_network_element(self):
        """ Test creating a network element """

        self.client.force_authenticate(self.user)

        data = {
            'name': 'Test name',
            'contacts': self.contacts.pk,
            'product': self.product.pk,
            'provider': self.network_element.pk
        }
        response = self.client.post(
            reverse('network:network_element_create'),
            data=data
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            NetworkElement.objects.count(),
            2
        )
        self.assertEqual(
            NetworkElement.objects.get(pk=1).name,
            'Test network element'
        )

    def test_negative_create_network_element(self):
        self.client.force_authenticate(self.user)

        data = {
            'name': 'Negative'
        }
        response = self.client.post(
            reverse('network:network_element_create'),
            data=data
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_greater_than_2_level(self):
        self.client.force_authenticate(self.user)

        data = {
            'level': '3'
        }
        response = self.client.patch(
            reverse('network:network_element_update', kwargs={'pk': self.network_element.pk}),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json()['level'],
            '0'
        )

    def test_provider_level(self):
        self.client.force_authenticate(self.user)

        network_element = NetworkElement.objects.create(
            name='Test IE',
            contacts=self.contacts,
            product=self.product,
            provider=self.network_element,
            level='2'
        )
        data = {
            'provider': 8
        }
        response = self.client.patch(
            reverse('network:network_element_update', kwargs={'pk': self.network_element.pk}),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            response.json(),
            [f'Нельзя выбрать {network_element.name} поставщиком.']
        )

    def test_list_network_element(self):
        """ Test show the list of network element """
        self.client.force_authenticate(self.user)

        response = self.client.get(
            reverse('network:network_element_list')
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            len(response.data),
            4
        )

    def test_retrieve_network_element(self):
        self.client.force_authenticate(self.user)

        response = self.client.get(
            reverse('network:network_element_retrieve', kwargs={'pk': self.network_element.pk})
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertGreater(
            response.data['created_at'],
            str(datetime.datetime.now())
        )

    def test_update_network_element(self):
        self.client.force_authenticate(self.user)
        data = {
            'name': 'New name'
        }

        response = self.client.patch(
            reverse('network:network_element_update', kwargs={'pk': self.network_element.pk}),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.data['name'],
            'New name'
        )

    def test_destroy_network_element(self):
        self.client.force_authenticate(self.user)

        response = self.client.delete(
            reverse('network:network_element_destroy', kwargs={'pk': self.network_element.pk})
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
