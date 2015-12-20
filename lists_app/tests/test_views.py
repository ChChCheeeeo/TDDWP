import unittest
from unittest.mock import Mock, patch
from lists_app.forms import ItemForm, EMPTY_ITEM_ERROR
from lists_app.views import new_list, new_list2
from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from lists_app.views import home_page, new_list
from django.template.loader import render_to_string
from lists_app.models import Item, List
from django.utils.html import escape
from lists_app.forms import (
    DUPLICATE_ITEM_ERROR, EMPTY_ITEM_ERROR,
    ExistingListItemForm, ItemForm,
)
from unittest import skip
from django.contrib.auth import get_user_model
User = get_user_model()

class HomePageTest(TestCase):

    maxDiff = None

    # def test_root_url_resolves_to_home_page_view(self):
    #     found = resolve('/')  #2
    #     # resolve is the function Django uses internally to resolve]
    #     # URLs, and find what view function they should map to. We’re
    #     # checking that resolve, when called with “/”, the root of the
    #     # site, finds a function called home_page. 
    #     self.assertEqual(found.func, home_page)  #3
    # def test_home_page_returns_correct_html(self):
    #     request = HttpRequest()
    #     response = home_page(request)
    #     # We use .decode() to convert the response.content bytes into
    #     # a Python unicode string, which allows us to compare strings
    #     # with strings, instead of bytes with bytes as we did earlier.
    #     # expected_html = render_to_string('home.html')
    #     # self.assertEqual(response.content.decode(), expected_html)
    #     expected_html = render_to_string('home.html', {'form': ItemForm()})
    #     # assertMultiLineEqual is useful for comparing long strings; it gives
    #     # you a diff-style output, but it truncates long diffs by default
    #     # use ith maxDiff
    #     self.assertMultiLineEqual(response.content.decode(), expected_html)

    def test_home_page_renders_home_template(self):
        response = self.client.get('/')
        # eplace our old manual test of the template
        self.assertTemplateUsed(response, 'home.html') #1


    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        # use assertIsInstance to check that our view uses the right kind of form
        self.assertIsInstance(response.context['form'], ItemForm)

# The Django TestCase class makes it too easy to write integrated tests.
# As a way of making it "pure", isolated unit tests, 
# only use unittest.TestCase
# NewListForm class class is goign to be used in all tests, so mock it.
@patch('lists_app.views.NewListForm')
class NewListViewIntegratedTest(unittest.TestCase):

    def setUp(self):
        # set up a basic POST request in setUp,
        # building up the request by hand rather than using the
        # (overly integrated) Django Test Client. 
        self.request = HttpRequest()
        self.request.POST['text'] = 'new list item'
        self.request.user = Mock()


    def test_passes_POST_data_to_NewListForm(self, mockNewListForm):
        # initialises its collaborator,
        # the NewListForm, with the correct constructor—the data
        # from the request.
        new_list2(self.request)
        mockNewListForm.assert_called_once_with(data=self.request.POST)

    def test_saves_form_with_owner_if_form_valid(self, mockNewListForm):
        mock_form = mockNewListForm.return_value
        # It should have an is_valid() function which returns True or False
        # appropriately, based on the input data.
        mock_form.is_valid.return_value = True
        new_list2(self.request)
        # The form should have a .save method which will accept a request.user,
        # which may or may not be a logged-in user, and deal with it
        # appropriately.
        mock_form.save.assert_called_once_with(owner=self.request.user)


    def test_does_not_save_if_form_invalid(self, mockNewListForm):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = False
        new_list2(self.request)
        self.assertFalse(mock_form.save.called)

    def test_saving_a_POST_request(self):
        self.client.post(
            '/lists/new',
            data={'text': 'A new list item'}
        )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')


    def test_redirects_after_POST(self):
        # because the Django test client behaves slightly differently
        # to our pure view function; it’s using the full Django stack
        # which adds the domain to our relative URL. Let’s use another
        # of Django’s test helper functions, instead of our two-step
        # check for the redirect
        response = self.client.post(
            '/lists/new',
            data={'text': 'A new list item'}
        )
        new_list = List.objects.first()
        self.assertRedirects(response, '/lists/%d/' % (new_list.id,))

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        # URL and view for new lists will optionally render the same template
        # as the home page, but with the addition of an error message
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = escape("You can't have an empty list item")
        # expected_error = "You can't have an empty list item"
        # print(response.content.decode())
        self.assertContains(response, expected_error)

    def test_invalid_list_items_arent_saved(self):
        self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_renders_home_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')


    def test_validation_errors_are_shown_on_home_page(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))


    def test_for_invalid_input_passes_form_to_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_list_owner_is_saved_if_user_is_authenticated(self):
        request = HttpRequest()
        request.user = User.objects.create(email='a@b.com')
        request.POST['text'] = 'new list item'
        new_list2(request)
        list_ = List.objects.first()
        self.assertEqual(list_.owner, request.user)

    # patch decorators are applied innermost first, so the new mock is
    # injected to our method as before the mockNewListForm.
    @patch('lists_app.views.redirect')
    def test_redirects_to_form_returned_object_if_form_valid(
        self, mock_redirect, mockNewListForm
    ):
        mock_form = mockNewListForm.return_value
        # specify testing case where form is valid
        mock_form.is_valid.return_value = True

        response = new_list2(self.request)

        # check view response is the result of the redirect function.
        self.assertEqual(response, mock_redirect.return_value)
        # check redirect function was called with the object that
        # the form returns on save.
        # The mocked form.save function is returning an object
        # which we expect our view to be able to use.
        # The form’s .save method should return a new list object, for our
        # view to redirect the user to.
        mock_redirect.assert_called_once_with(mock_form.save.return_value)

    def test_renders_home_template_with_form_if_form_invalid(
        self, mock_render, mockNewListForm
    ):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = False

        response = new_list2(self.request)

        self.assertEqual(response, mock_render.return_value)
        # When using assert methods on mocks, like assert_called_ once_with,
        # it’s doubly important to make sure you run the test and see it fail.
        # It’s all too easy to make a typo in your assert function name and end
        # up calling a mock method that does nothing.
        mock_render.assert_called_once_with(
            self.request, 'home.html', {'form': mock_form}
        )

class ListViewTest(TestCase):

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % (list_.id,))
        self.assertTemplateUsed(response, 'list.html')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/lists/%d/' % (correct_list.id,))
        self.assertEqual(response.context['list'], correct_list)

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)

        response = self.client.get('/lists/%d/' % (correct_list.id,))

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            '/lists/%d/' % (correct_list.id,),
            data={'text': 'A new item for an existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            '/lists/%d/' % (correct_list.id,),
            data={'text': 'A new item for an existing list'}
        )

        self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))
    def test_validation_errors_end_up_on_lists_page(self):
        list_ = List.objects.create()
        response = self.client.post(
            '/lists/%d/' % (list_.id,),
            data={'text': ''}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)
    def test_displays_item_form(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % (list_.id,))
        self.assertIsInstance(response.context['form'], ExistingListItemForm)
        self.assertContains(response, 'name="text"')

    def post_invalid_input(self):
        list_ = List.objects.create()
        return self.client.post(
            '/lists/%d/' % (list_.id,),
            data={'text': ''}
        )
    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ExistingListItemForm)

    def test_for_invalid_input_shows_error_on_page(self):
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_duplicate_item_validation_errors_end_up_on_lists_page(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='textey')
        response = self.client.post(
            '/lists/%d/' % (list1.id,),
            data={'text': 'textey'}
        )

        expected_error = escape(DUPLICATE_ITEM_ERROR)
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, 'list.html')
        self.assertEqual(Item.objects.all().count(), 1)


class MyListsTest(TestCase):


    def test_my_lists_url_renders_my_lists_template(self):
        User.objects.create(email='a@b.com')
        response = self.client.get('/lists/users/a@b.com/')
        self.assertTemplateUsed(response, 'my_lists.html')


    def test_passes_correct_owner_to_template(self):
        User.objects.create(email='wrong@owner.com')
        correct_user = User.objects.create(email='a@b.com')
        response = self.client.get('/lists/users/a@b.com/')
        self.assertEqual(response.context['owner'], correct_user)