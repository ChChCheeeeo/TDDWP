from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from lists_app.views import home_page #1
from django.template.loader import render_to_string

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