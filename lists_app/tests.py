from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from lists_app.views import home_page #1
from django.template.loader import render_to_string
from lists_app.models import Item

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')  #2
        # resolve is the function Django uses internally to resolve]
        # URLs, and find what view function they should map to. We’re
        # checking that resolve, when called with “/”, the root of the
        # site, finds a function called home_page. 
        self.assertEqual(found.func, home_page)  #3
    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        # We use .decode() to convert the response.content bytes into
        # a Python unicode string, which allows us to compare strings
        # with strings, instead of bytes with bytes as we did earlier.
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)
    def test_home_page_can_save_a_POST_request(self):
        # Use whitespace to:

        # setup the test
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'

        # call the function(s) being tested
        response = home_page(request)

        # 1 check that one new Item has been saved to the database.
        # objects.count() is a shorthand for objects.all().count().
        # 2 objects.first() is the same as doing objects.all()[0].
        # 3 # We check that the item’s text is correct. 

        self.assertEqual(Item.objects.count(), 1)  #1
        new_item = Item.objects.first()  #2
        self.assertEqual(new_item.text, 'A new list item')  #3

    def test_home_page_redirects_after_POST(self):
        
        # setup the test
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'

        # call the function9s) being tested
        response = home_page(request)
        # redirect after saving post
        # HTTP redirect,
        # points the browser towards a new location.
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')

    def test_home_page_only_saves_items_when_necessary(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Item.objects.count(), 0)

class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')

class ListViewTest(TestCase):

    def test_displays_all_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        # Instead of calling the view function directly, we use the
        # Django test client, which is an attribute of the Django
        # TestCase called self.client. We tell it to .get the URL
        # we’re testing—it’s actually a very similar API to the one
        # that Selenium uses. 
        response = self.client.get('/lists/the-only-list-in-the-world/')

        # Instead of using the slightly annoying
        # assertIn/response.content.decode() dance,
        # Django provides the assertContains method which knows how
        # to deal with responses and the bytes of their content. 
        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')