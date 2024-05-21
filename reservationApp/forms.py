from django import forms
from .models import Ticket


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["train_number", "departure_date", "departure_time", "destination"]
