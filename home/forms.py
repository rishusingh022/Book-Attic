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