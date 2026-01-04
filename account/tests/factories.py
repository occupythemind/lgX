from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory
import factory as fct
from ..models import Profile

class UserFactory(DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = fct.Sequence(lambda n:f'testuser_{n}')
    email = fct.LazyAttribute(lambda o:f'{o.username}tester@example.com')

class ProfileFactory(DjangoModelFactory):
    class Meta:
        model = Profile

    user = fct.SubFactory(UserFactory)
    name = fct.Sequence(lambda n:f'Test{n} User{n}')
