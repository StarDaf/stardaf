from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body', 'active')

        widgets = {
            'active' : forms.HiddenInput,
            'body' : forms.Textarea(attrs={'placeholder':'comment here', 'rows':1,})
        }
        # def __init__(self, *args, **kwargs):
        #     super(CommentForm, self).__init__(*args, **kwargs)
        #     self.fields['body'].widget.attrs.update({'placeholder':'comment here'})