from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import RequestFactory

class userModelTest(TestCase):
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


