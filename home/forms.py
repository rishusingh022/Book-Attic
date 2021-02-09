from . models import books
from django import forms

class sellbookform(forms.ModelForm):
    class Meta:
        model = books
        fields = [
            'book_name',
            'category',
            'price',
            'image',
            'pickuplocation'
        ]

class ContactForm(forms.Form):
    name= forms.CharField(max_length=500, label="Name")
    email= forms.EmailField(max_length=500, label="Email")
    comment= forms.CharField(label='',widget=forms.Textarea(
                        attrs={'placeholder': 'Enter your message here'}))
