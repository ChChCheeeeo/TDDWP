import logging
import requests
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()
logger = logging.getLogger(__name__)
PERSONA_VERIFY_URL = 'https://verifier.login.persona.org/verify'

class PersonaAuthenticationBackend(object):

    def authenticate(self, assertion):
        # logging.warning('entering authenticate function')
        response = requests.post(
            PERSONA_VERIFY_URL,
            data={'assertion': assertion, 'audience': settings.DOMAIN}
        )
        # logging.warning('got response from persona')
        # logging.warning(response.content.decode())
        if response.ok and response.json()['status'] == 'okay':
            email = response.json()['email']
            try:
                return User.objects.get(email=email)
            except User.DoesNotExist:
                return User.objects.create(email=email)
        else:
            logger.warning(
            'Persona says no. Json was: {}'.format(response.json())
        )


    def get_user(self, email):
        try:
            return User.objects.get(email=email)
        # You could just use pass here,
        # since the function would return None by default.
        # However, because we specifically need the function
        # to return None, explicit is better than implicit here. 
        except User.DoesNotExist:
            return None