from django import forms
from .models import TrackedCoin

# You can define allowed coins as tuples (coin_id, coin_name)
COIN_CHOICES = [
    ('bitcoin', 'Bitcoin'),
    ('ethereum', 'Ethereum'),
    ('dogecoin', 'Dogecoin'),
    ('litecoin', 'Litecoin'),

    # Add more as needed
]

class TrackedCoinForm(forms.ModelForm):
    coin_name = forms.ChoiceField(choices=COIN_CHOICES, label="Select Coin")

    class Meta:
        model = TrackedCoin
        fields = ['coin_name']
