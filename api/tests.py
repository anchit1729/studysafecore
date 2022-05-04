from django.test import TestCase
import json
from rest_framework import status
from rest_framework.test import APITestCase
from api.serializers import *
from api.models import *


# Create your tests here.
class AccessRecordCreateTests(APITestCase):
    def setUp(self):
        data = {
            'venue_code': 'V0001',
            'location': 'HKU',
            'type': 'CR',
            'capacity': 0,
            'members': []
        }
        response = self.client.post('/api/venue/create', data=data)

        data = {
            'uid': 'HKU0001',
            'name': 'Biggus'
        }
        response = self.client.post('/api/member/create', data=data)

    def test_record_create(self):
        data = {
            'member_uid': 'HKU0001',
            'venue_code': 'V0001',
            'access_type': 'IN',
            'record_datetime': '2022-04-11T10:30:00Z'
        }
        response = self.client.post('/api/record/create', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class AccessRecordListTests(APITestCase):
    def setUp(self):
        data = {
            'venue_code': 'V0002',
            'location': 'HKU',
            'type': 'CR',
            'capacity': 0,
            'members': []
        }
        response = self.client.post('/api/venue/create', data=data)

        data = {
            'uid': 'HKU0001',
            'name': 'Biggus'
        }
        response = self.client.post('/api/member/create', data=data)
        data = {
            'uid': 'HKU0002',
            'name': 'Biggus'
        }
        response = self.client.post('/api/member/create', data=data)

        data = {
            'member_uid': 'HKU0001',
            'venue_code': 'V0002',
            'access_type': 'IN',
            'record_datetime': '2022-04-11T10:30:00Z'
        }
        response = self.client.post('/api/record/create', data=data)

        data = {
            'member_uid': 'HKU0002',
            'venue_code': 'V0002',
            'access_type': 'IN',
            'record_datetime': '2022-04-11T10:35:00Z'
        }
        response = self.client.post('/api/record/create', data=data)

    def test_record_list_all(self):
        response = self.client.get('/api/record/access/all')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(isinstance(response.data, list), True)
        self.assertEqual(len(response.data), 2)


class VenueCreateTests(APITestCase):
    def test_venue_create(self):
        data = {
            'venue_code': 'V0001',
            'location': 'HKU',
            'type': 'CR',
            'capacity': 0,
            'members': []
        }
        response = self.client.post('/api/venue/create', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    

class VenueListTests(APITestCase):
    def setUp(self):
        data = {
            'venue_code': 'V0001',
            'location': 'HKU Main Library',
            'type': 'CR',
            'capacity': 0,
            'members': []
        }
        response = self.client.post('/api/venue/create', data=data)

        data = {
            'venue_code': 'V0002',
            'location': 'HKU Centennial Campus',
            'type': 'CR',
            'capacity': 0,
            'members': []
        }
        response = self.client.post('/api/venue/create', data=data)
    
    def test_venue_view(self):
        response = self.client.get('/api/venue/view/V0001')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['venue_code'], 'V0001')
    
    def test_venue_view_all(self):
        response = self.client.get('/api/venue/view-all')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(isinstance(response.data, list), True)
        self.assertEqual(len(response.data), 2)


class VenueModifyTests(APITestCase):
    def setUp(self):
        data = {
            'venue_code': 'V0001',
            'location': 'HKU Main Library',
            'type': 'CR',
            'capacity': 0,
            'members': []
        }
        response = self.client.post('/api/venue/create', data=data)
    
    def test_venue_modify(self):
        data = {
            'location': 'HKU Main Library',
            'type': 'CR',
            'capacity': 2,
            'members': []
        }
        response = self.client.put('/api/venue/modify/V0001', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['capacity'], '2')


class VenueDeleteTests(APITestCase):
    def setUp(self):
        data = {
            'venue_code': 'V0001',
            'location': 'HKU Main Library',
            'type': 'CR',
            'capacity': 0,
            'members': []
        }
        response = self.client.post('/api/venue/create', data=data)
    
    def test_venue_delete(self):
        response = self.client.delete('/api/venue/delete/V0001')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class MemberCreateTests(APITestCase):
    def test_member_create(self):
        data = {
            'uid': 'HKU0001',
            'name': 'Biggus'
        }
        response = self.client.post('/api/member/create', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class MemberListTests(APITestCase):
    def setUp(self):
        data = {
            'uid': 'HKU0001',
            'name': 'Biggus'
        }
        response = self.client.post('/api/member/create', data=data)
        data = {
            'uid': 'HKU0002',
            'name': 'Sugondese'
        }
        response = self.client.post('/api/member/create', data=data)
    
    def test_member_list_all(self):
        response = self.client.get('/api/member/list-all')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(isinstance(response.data, list), True)
        self.assertEqual(len(response.data), 2)
    
    def test_member_view(self):
        response = self.client.get('/api/member/view/HKU0001')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['uid'], 'HKU0001')
        self.assertEqual(response.data['name'], 'Biggus')


class MemberModifyTests(APITestCase):
    def setUp(self):
        data = {
            'uid': 'HKU0001',
            'name': 'Ligma'
        }
        response = self.client.post('/api/member/create', data=data)
    
    def test_member_modify(self):
        data = {
            'name': 'Yuri'
        }
        response = self.client.put('/api/member/modify/HKU0001', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Yuri')


class MemberDeleteTests(APITestCase):
    def setUp(self):
        data = {
            'uid': 'HKU0001',
            'name': 'Joe'
        }
        response = self.client.post('/api/member/create', data=data)
    
    def test_member_delete(self):
        response = self.client.delete('/api/member/delete/HKU0001')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class CloseContactsTests(APITestCase):
    def setUp(self):
        # Create Members
        data = {
            'uid': 'HKU0001',
            'name': 'Amogus'
        }
        response = self.client.post('/api/member/create', data=data)
        data = {
            'uid': 'HKU0002',
            'name': 'Sus'
        }
        response = self.client.post('/api/member/create', data=data)
        data = {
            'uid': 'HKU0003',
            'name': 'Po Tea'
        }
        response = self.client.post('/api/member/create', data=data)

        # Create Venue
        data = {
            'venue_code': 'V0001',
            'location': 'HKU Main Library',
            'type': 'CR',
            'capacity': 0,
            'members': []
        }
        response = self.client.post('/api/venue/create', data=data)

        # Create Access Records
        ## Only HKU0001 and HKU0002 are close contacts
        ## HKU0001 and HKU0002 enter at same time
        data = {
            'member_uid': 'HKU0001',
            'venue_code': 'V0001',
            'access_type': 'IN',
            'record_datetime': '2022-04-11T10:30:00Z'
        }
        response = self.client.post('/api/record/create', data=data)
        data = {
            'member_uid': 'HKU0002',
            'venue_code': 'V0001',
            'access_type': 'IN',
            'record_datetime': '2022-04-11T10:30:00Z'
        }

        ## HKU0001 and HKU0002 leave at same time > 30 minutes
        response = self.client.post('/api/record/create', data=data)
        data = {
            'member_uid': 'HKU0002',
            'venue_code': 'V0001',
            'access_type': 'EX',
            'record_datetime': '2022-04-11T11:30:00Z'
        }
        response = self.client.post('/api/record/create', data=data)
        data = {
            'member_uid': 'HKU0001',
            'venue_code': 'V0001',
            'access_type': 'EX',
            'record_datetime': '2022-04-11T11:30:00Z'
        }
        response = self.client.post('/api/record/create', data=data)

        ## HKU0003 enters after they leave
        data = {
            'member_uid': 'HKU0003',
            'venue_code': 'V0001',
            'access_type': 'IN',
            'record_datetime': '2022-04-11T11:30:00Z'
        }
        response = self.client.post('/api/record/create', data=data)
    
    def test_close_contacts(self):
        response = self.client.get('/api/contacts/HKU0001/2022-04-12')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(isinstance(response.data, list), True)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['uid'], 'HKU0002')


class VisitedVenuesTests(APITestCase):
    def setUp(self):
        data = {
            'uid': 'HKU0001',
            'name': 'Ana'
        }
        response = self.client.post('/api/member/create', data=data)

        data = {
            'venue_code': 'V0001',
            'location': 'HKU Main Library',
            'type': 'CR',
            'capacity': 0,
            'members': []
        }
        response = self.client.post('/api/venue/create', data=data)
        data = {
            'venue_code': 'V0002',
            'location': 'HKU not Main Library',
            'type': 'CR',
            'capacity': 0,
            'members': []
        }
        response = self.client.post('/api/venue/create', data=data)

        data = {
            'member_uid': 'HKU0001',
            'venue_code': 'V0001',
            'access_type': 'IN',
            'record_datetime': '2022-04-11T10:30:00Z'
        }
        response = self.client.post('/api/record/create', data=data)
        data = {
            'member_uid': 'HKU0001',
            'venue_code': 'V0001',
            'access_type': 'EX',
            'record_datetime': '2022-04-11T11:30:00Z'
        }
        response = self.client.post('/api/record/create', data=data)
        data = {
            'member_uid': 'HKU0001',
            'venue_code': 'V0002',
            'access_type': 'IN',
            'record_datetime': '2022-04-13T10:30:00Z'
        }
        response = self.client.post('/api/record/create', data=data)
        data = {
            'member_uid': 'HKU0001',
            'venue_code': 'V0002',
            'access_type': 'EX',
            'record_datetime': '2022-04-13T11:30:00Z'
        }
        response = self.client.post('/api/record/create', data=data)
    
    def test_visited_venues(self):
        response = self.client.get('/api/venues/HKU0001/2022-04-15')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(isinstance(response.data, list), True)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['venue_code'], 'V0002')