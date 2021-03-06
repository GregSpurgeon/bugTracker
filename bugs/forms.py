from django import forms
from bugs.models import Ticket


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ("title", "description")
