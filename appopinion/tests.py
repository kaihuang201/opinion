from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import RequestFactory
from appopinion.models import *
from django.contrib.auth.models import User
from datetime import datetime

class userModelTest(TestCase):

    def setUp(self):
        usr = User.objects.create_user('exist', password='exist')
        profile = Profile(
                    user = usr,
                    motto = '',
                )
        profile.save()

        topic = Topic(
                    title = 'News Title',
                    date = datetime.now(),
                    content = 'content',
                    url = 'gogo.com',
                    source = 'CS',
                    likecount = 0
                )
        topic.save()
        
    def test_signin_page(self):
        """
        test if the login page is rendered properly
        """
        response = self.client.get(reverse('appopinion:signin'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sign In")

    def test_signup_page(self):
        """
        test if the signup page is rendered properly
        """
        response = self.client.get(reverse('appopinion:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sign Up")

    def test_normal_signup(self):
        """
        simulate a user sign up
        """
        response = self.client.post(
                        reverse('appopinion:signup'), 
                        {
                            'username':'me',
                            'password':'me',
                            'password_again':'me'
                        }
                    )
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username='me')
        self.assertEqual(user.username, 'me')
    
    def test_username_exist_signup(self):
        """
        simulate a user tries to sign up but username is already used
        """
        response = self.client.post(
                        reverse('appopinion:signup'), 
                        {
                            'username':'exist',
                            'password':'exist',
                            'password_again':'exist'
                        }
                    )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Error:')

    def test_signin(self):
        """
        simulate a user sign in
        """
        response = self.client.post(
                        reverse('appopinion:signin'),
                        {
                            'username':'exist',
                            'password':'exist'
                        }
                    )

        self.assertEqual(response.status_code, 302)
     
    def test_user_profile(self):
        """
        simulate a user visit profile page
        """
        response = self.client.post(
                        reverse('appopinion:signin'),
                        {
                            'username':'exist',
                            'password':'exist'
                        }
                    )

        response = self.client.get(reverse('appopinion:profile'))
        self.assertContains(response, 'Profile')

    def test_user_profile_edit(self):
        """
        test if a user can edit profile
        """
        response = self.client.post(
                        reverse('appopinion:signin'),
                        {
                            'username':'exist',
                            'password':'exist'
                        }
                    )

        response = self.client.post(
                        reverse('appopinion:profile_edit'),
                        {
                            'motto':'my motto'
                        }
                    )
        
        response = self.client.get(reverse('appopinion:profile'))

        self.assertContains(response, 'my motto')

    def test_user_like(self):
        """
        test if a user can like a topic
        """

        response = self.client.post(
                        reverse('appopinion:signin'),
                        {
                            'username':'exist',
                            'password':'exist'
                        }
                    )

        topic = Topic.objects.get(title='News Title')
        self.client.post(
                        reverse('appopinion:like', args=[topic.id])
                    )
        topic = Topic.objects.get(title='News Title')
        self.assertEqual(topic.likecount,1)

        response = self.client.get(reverse('appopinion:profile'))
        self.assertContains(response, 'News Title')
