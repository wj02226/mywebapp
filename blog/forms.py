from django import forms
from .models import Blog

class BlogForm(forms.Form):
    text = forms.CharField(widget=forms.HiddenInput, min_length=1, max_length=20)

    def clean(self):
        text = self.cleaned_data.get('text', '').strip()
        if text == '':
            raise forms.ValidationError('没有输入内容')
        text = self.cleaned_data['text']
        return self.cleaned_data