from django import forms
from events.models import Event
# from cjws import settings


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            "name", "short_desc", "description", "location", "contact_details",
            "start_date", "end_date", "slug"
        ]
