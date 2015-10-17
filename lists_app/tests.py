from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from lists_app.views import home_page #1

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')  #2
        # resolve is the function Django uses internally to resolve]
        # URLs, and find what view function they should map to. We’re
        # checking that resolve, when called with “/”, the root of the
        # site, finds a function called home_page. 
        self.assertEqual(found.func, home_page)  #3

    def test_home_page_returns_correct_html(self):
        # 1 create an HttpRequest object, which is what Django will
        # see when a user’s browser asks for a page.
        # 2 pass it to our home_page view, which gives us a response.
        # You won’t be surprised to hear that this object is an
        # instance of a class called HttpResponse. Then, we assert
        # that the .content of the response—which is the HTML that we
        # send to the user—has certain properties.
        # We want it to start with an <html> tag which gets closed at
        # the end. Notice that response.content is raw bytes, not a
        # Python string, so we have to use the b'' syntax to compare
        # them. More info is available in Django’s Porting to Python
        # 3 docs.
        # And we want a <title> tag somewhere in the middle, with the
        # words "To-Do lists" in it—because that’s what we specified
        # in our functional test. 
        request = HttpRequest()  #1
        response = home_page(request)  #2
        self.assertTrue(response.content.startswith(b'<html>'))  #3
        self.assertIn(b'<title>To-Do lists</title>', response.content)  #4
        self.assertTrue(response.content.endswith(b'</html>'))