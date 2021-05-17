from django.test import TestCase
from lists.views import home_page
from django.urls import resolve


class HomePageTest(TestCase):

    def test_home_page_that_returns_html_page(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
