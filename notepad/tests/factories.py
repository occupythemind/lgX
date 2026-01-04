from factory.django import DjangoModelFactory
import factory as fct
from account.tests.factories import ProfileFactory
from ..models import Topic, Entry

class TopicFactory(DjangoModelFactory):
    class Meta:
        model = Topic
    
    owner = fct.SubFactory(ProfileFactory)
    title = fct.Faker('paragraph', nb_sentences=3)


class EntryFactory(DjangoModelFactory):
    class Meta:
        model = Entry

    topic = fct.SubFactory(TopicFactory)
    text = fct.Faker('paragraph', nb_sentences=3)