from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserRegistrationForm(forms.ModelForm):

    GENDER = (
        ('male', 'Male'),
        ('female', 'Female'),
    )


    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)

    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)
                                

    gender = forms.TypedChoiceField(choices=GENDER, coerce=str)


    class Meta:
        model = User
        fields = ('first_name', 'username', 'email')

        widgets = {
            'username':forms.TextInput(attrs={'placeholder':'No space and symbols, just text eg abdul, farida12, tosiFashion'}),
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('The two passwords don\'t match')

        return cd['password2']

# form for editing user's info
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = True
        self.fields['phone'].required = True

    class Meta:
        model = Profile
        fields = ('image', 'phone')


class SearchForm(forms.Form):
    query = forms.CharField(label='Search for products', help_text='Enter your username')

class FriendSearchForm(forms.Form):
    search = forms.CharField(label='Search for friends')    