from unittest.mock import patch
from django.conf import settings
from django.test import TestCase

from django.contrib.auth import get_user_model
User = get_user_model()

from accounts_app.authentication import (
    PERSONA_VERIFY_URL, PersonaAuthenticationBackend
)

import logging



# You can apply a patch at the class level as well,
# and that has the effect that every test method in the class will
# have the patch applied, and the mock injected. 
@patch('accounts_app.authentication.requests.post')
class AuthenticateTest(TestCase):

    # use the setUp function to prepare any useful variables
    # to use in all of the tests. 
    def setUp(self):
        self.backend = PersonaAuthenticationBackend()
        self.backend = PersonaAuthenticationBackend()
        user = User(email='other@user.com')
        # By default, Django’s users have a username attribute,
        # which has to be unique, so this value is just a placeholder
        # to allow us to create multiple users. Later on, get rid of
        # usernames in favour of using emails as the primary key. 
        user.username = 'otheruser'
        user.save()


    def test_sends_assertion_to_mozilla_with_domain(self, mock_post):
        self.backend.authenticate('an assertion')
        mock_post.assert_called_once_with(
            PERSONA_VERIFY_URL,
            data={'assertion': 'an assertion', 'audience': settings.DOMAIN}
        )


    def test_returns_none_if_response_errors(self, mock_post):
        # Now each test is only adjusting the setup variables it needs,
        # rather than setting up a load of duplicated boilerplate,
        # it’s more readable.
        mock_post.return_value.ok = False
        mock_post.return_value.json.return_value = {}
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


    def test_creates_new_user_if_necessary_for_valid_assertion(self, mock_post):
        mock_post.return_value.json.return_value = {'status': 'okay', 'email': 'a@b.com'}
        found_user = self.backend.authenticate('an assertion')
        new_user = User.objects.get(email='a@b.com')
        self.assertEqual(found_user, new_user)


    def test_logs_non_okay_responses_from_persona(self, mock_post):
        response_json = {
            'status': 'not okay', 'reason': 'eg, audience mismatch'
        }
        # set up test with some data that should cause some logging
        mock_post.return_value.ok = True
        mock_post.return_value.json.return_value = response_json


        # retrieve the actual logger for the module being tested 
        logger = logging.getLogger('accounts_app.authentication')
        # use patch.object to temporarily mock out its warning function,
        # by using with to make it a context manager around the function
        # being tested
        with patch.object(logger, 'warning') as mock_log_warning:
            self.backend.authenticate('an assertion')


        # then it’s available to make assertions against
        mock_log_warning.assert_called_once_with(
            'Persona says no. Json was: {}'.format(response_json)
        )


class GetUserTest(TestCase):

    def test_gets_user_by_email(self):
        backend = PersonaAuthenticationBackend()
        other_user = User(email='other@user.com')
        other_user.username = 'otheruser'
        other_user.save()
        desired_user = User.objects.create(email='a@b.com')
        found_user = backend.get_user('a@b.com')
        self.assertEqual(found_user, desired_user)


    def test_returns_none_if_no_user_with_that_email(self):
        backend = PersonaAuthenticationBackend()
        self.assertIsNone(
            backend.get_user('a@b.com')
        )