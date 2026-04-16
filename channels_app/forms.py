from django import forms
from .models import Channel, Article, Comment


class ChannelForm(forms.ModelForm):
    class Meta:
        model = Channel
        fields = ['title', 'slug', 'description', 'avatar']

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        if Channel.objects.filter(slug=slug).exists():
            raise forms.ValidationError('Такая ссылка канала уже занята.')
        return slug


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'cover', 'status']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Написать комментарий...'
            })
        }