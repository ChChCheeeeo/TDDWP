from django.test import TestCase
from unittest.mock import patch

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