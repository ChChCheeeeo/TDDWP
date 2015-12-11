from unittest.mock import patch
from django.test import TestCase

from accounts_app.authentication import (
    PERSONA_VERIFY_URL, DOMAIN, PersonaAuthenticationBackend
)
from django.contrib.auth import get_user_model
User = get_user_model()


# You can apply a patch at the class level as well,
# and that has the effect that every test method in the class will
# have the patch applied, and the mock injected. 
@patch('accounts_app.authentication.requests.post')
class AuthenticateTest(TestCase):

    # use the setUp function to prepare any useful variables
    # to use in all of the tests. 
    def setUp(self):
        self.backend = PersonaAuthenticationBackend()


    def test_sends_assertion_to_mozilla_with_domain(self, mock_post):
        self.backend.authenticate('an assertion')
        mock_post.assert_called_once_with(
            PERSONA_VERIFY_URL,
            data={'assertion': 'an assertion', 'audience': DOMAIN}
        )


    def test_returns_none_if_response_errors(self, mock_post):
        # Now each test is only adjusting the setup variables it needs,
        # rather than setting up a load of duplicated boilerplate,
        # it’s more readable.
        mock_post.return_value.ok = False
        user = self.backend.authenticate('an assertion')
        self.assertIsNone(user)


    def test_returns_none_if_status_not_okay(self, mock_post):
        # Now each test is only adjusting the setup variables it needs,
        # rather than setting up a load of duplicated boilerplate,
        # it’s more readable.
        mock_post.return_value.json.return_value = {'status': 'not okay!'}
        user = self.backend.authenticate('an assertion')
        self.assertIsNone(user)

    def test_finds_existing_user_with_email(self, mock_post):
        mock_post.return_value.json.return_value = {'status': 'okay', 'email': 'a@b.com'}
        actual_user = User.objects.create(email='a@b.com')
        found_user = self.backend.authenticate('an assertion')
        self.assertEqual(found_user, actual_user)