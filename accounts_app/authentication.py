import requests
from django.contrib.auth import get_user_model
User = get_user_model()

PERSONA_VERIFY_URL = 'https://verifier.login.persona.org/verify'
DOMAIN = 'localhost'


class PersonaAuthenticationBackend(object):

    def authenticate(self, assertion):
        response = requests.post(
            PERSONA_VERIFY_URL,
            data={'assertion': assertion, 'audience': DOMAIN}
        )
        if response.ok and response.json()['status'] == 'okay':
            email = response.json()['email']
            try:
                return User.objects.get(email=email)
            except User.DoesNotExist:
                return User.objects.create(email=email)


    def get_user(self, email):
        try:
            return User.objects.get(email=email)
        # You could just use pass here,
        # since the function would return None by default.
        # However, because we specifically need the function
        # to return None, explicit is better than implicit here. 
        except User.DoesNotExist:
            return None