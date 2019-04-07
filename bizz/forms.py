from django import forms
from .models import Shop, Product, Post

class CreateShopForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreateShopForm, self).__init__(*args, **kwargs)
        self.fields['logo'].required = True
        self.fields['business_name'].required = True
        self.fields['business_address'].required = True
        self.fields['shop_address'].required = True
        self.fields['home_address'].required = True
        self.fields['description'].required = True
        


    class Meta:
        model = Shop
        fields = ('business_name', 'business_address', 'shop_address', 'home_address', 'logo', 'description','Bank', 'account_number', 'account_name')

class ShopEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ShopEditForm, self).__init__(*args, **kwargs)
        self.fields['logo'].required = True
        self.fields['business_name'].required = True
        self.fields['business_address'].required = True
        self.fields['shop_address'].required = True
        self.fields['home_address'].required = True
        self.fields['description'].required = True
        self.fields['Bank'].required = True
        self.fields['account_number'].required = True
        self.fields['account_name'].required = True
    
    class Meta:
        model = Shop
        fields = ('logo', 'business_name', 'business_address', 'shop_address', 'home_address', 'description', 'Bank', 'account_number', 'account_name')


class AddProductForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(AddProductForm, self).__init__(*args, **kwargs)
        self.fields['photo'].required = True
        self.fields['description'].required = True
        self.fields['price'].required = True
        self.fields['stock'].required = True

    class Meta:
        model = Product
        fields = ('category', 'name', 'tags','photo', 'photo1', 'photo2', 'photo3', 'video', 'description', 'price', 'stock', 'available')

        widgets = {
            'available' : forms.HiddenInput,
            'tags':forms.TextInput(attrs={'placeholder':'eg: fashion, clothing, zafas'}),
            

        }


class UpdateProductForm(forms.Form):
    MAX_QUANTITY = ((i, str(i)) for i in range(0, 31))  # a user can buy a maximum of 20 products

    quantity = forms.TypedChoiceField(choices=MAX_QUANTITY,
                                      coerce=int)




class AddPostForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(AddPostForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = True
        self.fields['post'].required = True
        self.fields['title'].required = True

    class Meta:
        model = Post
        fields = ('title', 'post', 'tags', 'image', 'video', 'question')

        widgets = {
            'introduction' : forms.Textarea(attrs={'placeholder':'optional(can be left blank)'}),
            'paragraph_1' : forms.Textarea(attrs={'placeholder':'optional(can be left blank)'}),
            'paragraph_2' : forms.Textarea(attrs={'placeholder':'optional(can be left blank)'}),
            'paragraph_3' : forms.Textarea(attrs={'placeholder':'optional(can be left blank)'}),
            'paragraph_4' : forms.Textarea(attrs={'placeholder':'optional(can be left blank)'}),
            'paragraph_5' : forms.Textarea(attrs={'placeholder':'optional(can be left blank)'}),
            'question' : forms.Textarea(attrs={'placeholder':'can be left blank'}),
            'tags':forms.TextInput(attrs={'placeholder':'eg: fashion, zahraKitchen'}),
        }