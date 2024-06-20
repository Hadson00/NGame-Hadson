from django import forms
from django.forms import ModelForm
from myapp.models import *

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['title', 'path', 'description','value', 'quantity']
        labels = {
            'title': "Título:",
            'path': "Faça upload:",
            'description': "Descrição:",
            'value' : 'Valor:',
            'quantity': 'Quantidade:'       
            }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titulo'}),
            'path': forms.ClearableFileInput(attrs={'class': 'form-control',}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'value': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Valor'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantidade'})
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': "Comentário:",
        }
        widgets = {
            'content': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write your comment here...'}),
        }