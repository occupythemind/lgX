from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status
from account.tests.factories import UserFactory
from .factories import TopicFactory, EntryFactory
from ..models import Topic, Entry

class TestTopicAPI(APITestCase):
    def setUp(self):
        self.user = UserFactory() # create a user
        # Authenticate this user for all requests
        self.client.force_authenticate(user=self.user)

    def test_list_topics(self):
        # generate some data
        TopicFactory.create_batch(6)

        # hit the API
        url = reverse('topics')
        response = self.client.get(url)

        # confirm thr results
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 6)

