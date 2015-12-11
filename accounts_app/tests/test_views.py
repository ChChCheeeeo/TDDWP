from django.http import HttpRequest
from accounts_app.views import persona_login
from django.contrib.auth import get_user_model, SESSION_KEY
from django.test import TestCase
from unittest.mock import patch
# Here get_user_model from django.contrib.auth finds the project’s user model
# and it works whether you’re using the standard user model or a custom one,
User = get_user_model()

class LoginViewTest(TestCase):

    # patch is a bit like the Sinon mock function.
    # It lets you specify an object you want to "mock out".
    # In this case it's mocking out the authenticate function,
    # which we expect to be using in accounts/views.py
    @patch('accounts_app.views.authenticate')
    def test_calls_authenticate_with_assertion_from_post(
        self, mock_authenticate
    ):
        # The decorator adds the mock object as an additional argument to the
        # function it’s applied to. 
        # It can then onfigure the mock so that it has certain behaviours.
        # Having authenticate return None is the simplest, set the special
        # .return_value attribute. Otherwise it would return another mock,
        # and that would probably confuse our view. 
        mock_authenticate.return_value = None
        self.client.post('/accounts/login', {'assertion': 'assert this'})
        # Mocks can make assertions. In this case, they can check whether
        # they were called, and what with. 
        mock_authenticate.assert_called_once_with(assertion='assert this')
    @patch('accounts_app.views.authenticate')
    def test_returns_OK_when_user_found(
        self, mock_authenticate
    ):
        user = User.objects.create(email='a@b.com')
        user.backend = ''  # required for auth_login to work
        mock_authenticate.return_value = user
        self.client.post('/accounts/login', {'assertion': 'a'})
        # The Django test client keeps track of the session for its user.
        # For the case where the user gets authenticated successfully, 
        # check that their user ID (the primary key, or pk) is associated
        # with their session. 
        self.assertEqual(self.client.session[SESSION_KEY], str(user.pk))
    @patch('accounts_app.views.authenticate')
    def test_does_not_get_logged_in_if_authenticate_returns_None(
        self, mock_authenticate
    ):
        mock_authenticate.return_value = None
        self.client.post('/accounts/login', {'assertion': 'a'})
        # In the case where the user should not be authenticated,
        # the SESSION_KEY should not appear in their session. 
        self.assertNotIn(SESSION_KEY, self.client.session)
    # An alternative way of testing that the Django login function
    # was called correctly would be to mock it out too
    @patch('accounts_app.views.login')
    @patch('accounts_app.views.authenticate')
    def test_calls_auth_login_if_authenticate_returns_a_user(
        self, mock_authenticate, mock_login
    ):
        request = HttpRequest()
        request.POST['assertion'] = 'asserted'
        mock_user = mock_authenticate.return_value
        persona_login(request)
        mock_login.assert_called_once_with(request, mock_user)