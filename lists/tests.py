from django.test import TestCase
from lists.views import home_page
from django.urls import resolve
from django.http import HttpRequest


class HomePageTest(TestCase):

    def test_root_uls_resolve_to_home_page(self):
        found = resolve("/")
        self.assertEqual(found.func, home_page)

    def test_home_page_that_returns_html_page(self):
        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>To-do lists</title>', html)
        self.assertTrue(html.endswith('</html>'))