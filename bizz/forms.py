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
        fields = ('category', 'name', 'photo', 'photo1', 'photo2', 'photo3', 'video', 'description', 'price', 'stock', 'available')

        widgets = {
            'available' : forms.HiddenInput,
            'name':forms.TextInput(attrs={'placeholder':'sunan kaya'}),
            'description' : forms.Textarea(attrs={'placeholder':'bayanin kaya'}),
            'price' : forms.TextInput(attrs={'placeholder':'kudin kaya'}),
            'stock':forms.TextInput(attrs={'placeholder':'samfur nawa ne?'})

        }


class UpdateProductForm(forms.Form):
    MAX_QUANTITY = ((i, str(i)) for i in range(0, 31))  # a user can buy a maximum of 20 products

    quantity = forms.TypedChoiceField(choices=MAX_QUANTITY,
                                      coerce=int)




