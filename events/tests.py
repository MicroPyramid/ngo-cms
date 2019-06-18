from django.test import TestCase
from events.forms import *

# Create your tests here.


class Setup_Class(TestCase):

    def setUp(self):
        self.event = Event.objects.create(name="Rug distribution",
                                          short_desc="abcd",
                                          description="xyz",
                                          location="Hyderbad",
                                          contact_details="12345",
                                          start_date="2018-12-02",
                                          end_date="2018-12-31",
                                          slug="rug-distribution")


class Event_Form_Test(TestCase):

    def test_EventForm_valid(self):
        form = EventForm(data={'name': "Rug distribution",
                               'short_desc': "abcd",
                               'description': "xyz",
                               'location': "Hyderabad",
                               'contact_details': "12345",
                               'start_date': "2018-12-02",
                               "end_date": "2018-12-31",
                               'slug': 'rug-distribution'})
        print(form.errors)
        self.assertTrue(form.is_valid())

    def test_EventForm_invalid(self):
        form = EventForm(data={'name': "", 'short_desc': "fghj",
                               'description': "dfgvbhn",
                               'location': "kamareddy",
                               'contact_details': "",
                               'start_date': "",
                               'end_date': "", 'slug': ""})
        self.assertFalse(form.is_valid())
