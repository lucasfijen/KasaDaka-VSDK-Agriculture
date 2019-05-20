from django.test import Client
import pytest
from mixer.backend.django import mixer

c = Client()
response = c.post('/vxml/region/1', {'redirect_url': '/vxml/offers/33',
                                     'region_id': 1,
                                     'caller_id': 123})

response2 = c.post('/vxml/product/33', {'redirect_url': '/vxml/offers/33',
                'product_id': 1,
                'caller_id': 123})