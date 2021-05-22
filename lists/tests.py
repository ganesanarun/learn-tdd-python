from urllib import response
from django.test import TestCase
from lists.models import Item, List


class HomePageTest(TestCase):

    def test_home_page_that_returns_html_page(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')

        self.assertTemplateUsed(response, 'list.html')
        self.assertEqual(response.context['list'], list_)

    def test_displays_only_items_for_that_list(self):
        list1 = List.objects.create()
        Item.objects.create(text='first item', list=list1)
        Item.objects.create(text='second item', list=list1)
        other_list = List.objects.create()
        Item.objects.create(text='other list first item', list=other_list)
        Item.objects.create(text='other list second item', list=other_list)

        response = self.client.get(f'/lists/{list1.id}/')

        self.assertContains(response, 'first item')
        self.assertContains(response, 'second item')
        self.assertNotContains(response, 'other list second item')
        self.assertNotContains(response, 'other list first item')


class NewListTest(TestCase):

    def test_can_save_a_post_request(self):
        self.client.post('/lists/new', {'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        first_item = Item.objects.first()
        self.assertEqual(first_item.text, 'A new list item')

    def test_redirects_after_post(self):
        response = self.client.post(
            '/lists/new', {'item_text': 'A new list item'})
        list_ = List.objects.first()

        self.assertRedirects(response, f'/lists/{list_.id}/')


class NewItemTest(TestCase):

    def test_can_save_a_POST_request_to_an_existing_list(self):
        list_ = List.objects.create()

        self.client.post(f'/lists/{list_.id}/add_item',
                         {'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        item = Item.objects.first()
        self.assertEqual(item.list, list_)

    def test_redirects_to_list_view(self):
        list_ = List.objects.create()

        response = self.client.post(f'/lists/{list_.id}/add_item',
                                    {'item_text': 'A new list item'})

        self.assertRedirects(response, f'/lists/{list_.id}/')


class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()

        all_items = Item.objects.all()
        self.assertEqual(all_items.count(), 2)

        first_saved_item = all_items[0]
        second_saved_item = all_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list_)
