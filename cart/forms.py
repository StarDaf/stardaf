from django import forms


class CartAddForm(forms.Form):
    MAX_QUANTITY = ((i, str(i)) for i in range(1, 5))  # a user can buy a maximum of 20 products

    quantity = forms.TypedChoiceField(choices=MAX_QUANTITY,
                                      coerce=int)

    update = forms.BooleanField(initial=False,
                                 required=False,
                                 widget=forms.HiddenInput)