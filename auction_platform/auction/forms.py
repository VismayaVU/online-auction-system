from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Item, Auction, Tag
from django.utils import timezone


class UserSignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='First Name')
    last_name = forms.CharField(max_length=30, required=True, help_text='Last Name')
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class AuctionItemForm(forms.ModelForm):
    starting_price = forms.DecimalField(label="Starting Price", min_value=0)

    class Meta:
        model = Item
        fields = ['name', 'price', 'item_description']
        labels = {
            'name': 'Item Name',
            'price': 'Starting Price',
            'item_description': 'Description',
        }
        exclude = ['price']


class AuctionForm(forms.ModelForm):
    title = forms.CharField(max_length=255, label="Auction Title")
    description = forms.CharField(widget=forms.Textarea, label="Auction Description")
    start_date = forms.DateTimeField(
        initial=timezone.now,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label="Auction Start Date",
    )
    end_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label="Auction End Date",
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Select Tags for Auction",
    )

    class Meta:
        model = Auction
        fields = ['title', 'description', 'start_date', 'end_date']
        labels = {
            'start_date': 'Start Date and Time',
            'end_date': 'End Date and Time',
        }
        exclude = ['starting_bid']
