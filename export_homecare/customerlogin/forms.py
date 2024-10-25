# forms.py

from django import forms

class ChatForm(forms.Form):
    message = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Type your message here...',
        'class': 'input--style-4'
    }))
