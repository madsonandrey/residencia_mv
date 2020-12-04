from usuario.models import Usuario, Exames
from django import forms
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    senha = forms.CharField(max_length=32, widget=forms.PasswordInput)
    confirmar_senha = forms.CharField(max_length=32, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')


class FormUsuario(forms.ModelForm):
    class Meta:
        model = Usuario
        exclude = ('data_criacao', 'usuario')


class FormExames(forms.ModelForm):
    class Meta:
        model = Exames
        exclude = ('data_criacao', 'paciente')



