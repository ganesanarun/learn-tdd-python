from django.test import TestCase
from lists.models import Item


class HomePageTest(TestCase):

    def test_home_page_that_returns_html_page(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_post_request(self):
        response = self.client.post('/', {'item_text': 'A new list item'})
        self.assertIn('A new list item', response.content.decode('utf8'))
        self.assertTemplateUsed(response, 'home.html')


class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        all_items = Item.objects.all()
        self.assertEqual(all_items.count(), 2)

        first_saved_item = all_items[0]
        second_saved_item = all_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')
