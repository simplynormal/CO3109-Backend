from django.contrib.auth.hashers import make_password
from django.urls import reverse
from rest_framework import status
from rest_framework.test import (APIClient, APITestCase)

from mainframe.models import (CustomUser, Order, Machine, Product)

NUM_MACHINE = 10


class OrderTests(APITestCase):
    def setUp(self):
        user = CustomUser.objects.create(
            email=f'tester@localhost.com',
            password=make_password('iamtester'),
            first_name=f'Tester',
            last_name='User',
            phone=f'0969696969',
        )
        item = Product.objects.create(
            uuid='3964ff86-161f-4bcf-a211-0f2dd5f91812',
            image='',
            name=f'Sample product',
            price=47,
            unit='335mL',
            desc=''
        )
        machine = Machine.objects.create(name='Ground floor of A5')
        Order.objects.create(
            user=user, item=item, machine=machine, order_id=69, quantity=420
        )

    def test_view_order(self):
        url = reverse('v1_order:view') + '?order_id=69'
        client = APIClient()
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_set_quantity(self):
        url = reverse('v1_order:item_quantity')
        client = APIClient()
        response = client.put(
            url, {
                'order_id': 69,
                'item_uuid': '3964ff86-161f-4bcf-a211-0f2dd5f91812',
                'new_quantity': 4
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
