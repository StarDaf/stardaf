from django import forms
from .models import Shop, Product

class CreateShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ('business_name', 'business_address', 'shop_address', 'home_address', 'logo')

class ShopEditForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ('logo', 'business_name', 'business_address', 'shop_address', 'home_address', 'description')


class AddProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('category', 'name', 'photo', 'video', 'description', 'price', 'stock', 'available')

        widgets = {
            'available' : forms.HiddenInput,
            'name':forms.TextInput(attrs={'placeholder':'sunan kaya'}),
            'description' : forms.Textarea(attrs={'placeholder':'bayanin kaya'}),
            'price' : forms.TextInput(attrs={'placeholder':'kudin kaya'}),
            'stock':forms.TextInput(attrs={'placeholder':'samfur nawa ne?'})

        }


