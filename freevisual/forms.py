from django import forms
from .models import Creator

class CreateCreatorForm(forms.ModelForm):

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirma tu contraseña'}),
        label='Confirma tu contraseña'
    )

    class Meta:
        model = Creator
        fields = ['name', 'username','email', 'password']
        widgets = { # Estilizamos importando el modelo inyectando los estilos de boostrap
            'name': forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'Escribe tu nombre'}),
            'username': forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'Escribe tu nombre de usuario'}),
            'email': forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'Escribe tu email'}),
            'password': forms.PasswordInput(attrs={'class' : 'form-control', 'placeholder': 'Escribe tu contraseña'})
        }

class LoginForm(forms.ModelForm):
    
    class Meta:
        model = Creator
        fields = ['username','password']
        widgets = {
            'username': forms.TextInput(attrs={'class' : 'form-control text-center', 'placeholder': 'Escribe tu nombre de usuario'}),
            'password': forms.PasswordInput(attrs={'class' : 'form-control text-center', 'placeholder': 'Escribe tu contraseña'})
        }
