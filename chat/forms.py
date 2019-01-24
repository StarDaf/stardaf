from django import forms
from .models import ChatMessage

class ComposeForm(forms.Form):
    message = forms.CharField(
            widget=forms.TextInput(
                attrs={"class": "form-control"}
                )
            )


class ChatForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ('message',)

        