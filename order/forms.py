from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('quantity', 'city', 'address', 'phone_number', 'discount_code')

        widgets = {
            'discount_code':forms.TextInput(attrs={'placeholder':'can be left blank'}),
        }