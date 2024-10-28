from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Item, Auction
from django.utils import timezone


class UserSignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='First Name')
    last_name = forms.CharField(max_length=30, required=True, help_text='Last Name')
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class AuctionItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'price', 'item_description']
        labels = {
            'name': 'Item Name',
            'price': 'Starting Price',
            'item_description': 'Description',
        }


class AuctionForm(forms.ModelForm):
    start_date = forms.DateTimeField(
        initial=timezone.now,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label="Auction Start Date",
    )
    end_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label="Auction End Date",
    )

    class Meta:
        model = Auction
        fields = ['start_date', 'end_date']
        labels = {
            'start_date': 'Start Date and Time',
            'end_date': 'End Date and Time',
        }