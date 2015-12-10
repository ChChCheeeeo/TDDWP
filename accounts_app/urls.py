from django.conf.urls import url
from accounts_app import views

urlpatterns = [
    url(r'^login$', views.persona_login, name='persona_login'),
]