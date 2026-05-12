from django.test import TestCase
from rest_framework.test import APITestCase
from connections import models
from connections import serializers
from accounts.models import User
from skills.models import UserSkill, Skill
from rest_framework_simplejwt.tokens import AccessToken
from connections.models import ConnectionRequest
from django.urls import reverse
from rest_framework import status
# Create your tests here.
class ConnectionTests(APITestCase):
    def setUp(self):
        """
        Since for most of the cases, we'll need two users, their UserSkill set and 
        also a ConnectionRequest between them. We created this setUp to handle it automatically
        for each views test.
        """
        self.sk1= Skill.objects.create(name="Python", is_approved=True)
        self.sk2= Skill.objects.create(name="C++", is_approved=True)
        """
        Created 2 skills to add to the User's Userskill model instances.
        """
        self.user= User.objects.create_user(username="fz", password="123admin")
        self.tok1=AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.tok1))
        """
        Created a user, gave it direct access tokens instead of by making it hit
        the 'api/token/' endpoint. And gave it the logged in credentials.
        """
        self.user2= User.objects.create_user(username="ak", password="456admin")
        self.tok2=AccessToken.for_user(self.user2)
        self.user3= User.objects.create_user(username="fzz", password="789admin")
        self.tok3=AccessToken.for_user(self.user3)
        self.usk1a= UserSkill.objects.create(user=self.user, skill=self.sk1, skill_type="s")
        self.usk1b= UserSkill.objects.create(user=self.user, skill=self.sk2, skill_type="o")
        self.usk2a= UserSkill.objects.create(user=self.user2, skill=self.sk2, skill_type="s")
        self.usk2b= UserSkill.objects.create(user=self.user2, skill=self.sk1, skill_type="o")
        self.cr= ConnectionRequest.objects.create(sender=self.user, receiver=self.user2)
        """
        Set Up a connection between the 2 users.
        """

    def test_SendRequest(self):
        data={"receiver": self.user3.id}
        response=self.client.post(reverse("connections:sentreq"), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_duplicate_requests(self):
        data={"receiver": self.user3.id}
        response1=self.client.post(reverse("connections:sentreq"), data, format='json')
        response2=self.client.post(reverse("connections:sentreq"), data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_ListConnections(self):
        ConnectionRequest.objects.create(sender=self.user, receiver=self.user3, connectionStatus="a")
        response = self.client.get(reverse("connections:listcon"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['sender'], self.user.id)
    
    def test_PendingConnections(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+ str(self.tok2))
        response=self.client.get(reverse("connections:penCon"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['receiver'], self.user2.id)
