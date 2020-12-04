from django import forms
from .models import Laboratorio, User


class LaboratorioForm(forms.ModelForm):
    class Meta:
        model = Laboratorio
        exclude = ('dados', 'data_criacao')


class UserForm(forms.ModelForm):
    nome = forms.CharField(max_length=32, label='Nome')
    senha = forms.CharField(max_length=32, widget=forms.PasswordInput)
    confirmar_senha = forms.CharField(max_length=32, widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('email', 'username')
