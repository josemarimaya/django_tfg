from django import forms
from .models import Creator, Image, Provinces, Brand

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


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image', 'title' , 'description']
        widgets ={
            'title': forms.TextInput(attrs={
                'class': 'form-control',  # Clases de Bootstrap o personalizadas
                'placeholder': 'Ponle un título a tu imagen',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ponle una descripción',
                'rows': 3,
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            })
        }

class EditProfileForm(forms.ModelForm):

    provinces = forms.ModelMultipleChoiceField(
        queryset=Provinces.objects.all(),
        widget=forms.SelectMultiple(attrs={

            'class': 'form-select',
            'size': '8'
        }),  
        label = "Provincias en las que trabajas"
    )

    brand = forms.ModelMultipleChoiceField(
        queryset=Brand.objects.all(),
        widget=forms.SelectMultiple(attrs={

            'class': 'form-select',
            'size': '8'
        }),  
        label = "Marcas de herramientas con las que has trabajado"
    )

    class Meta:
        model = Creator
        fields = ['profile_pic', 'description', 'provinces', 'brand']
        widgets = {
            'profile_pic': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control'
            })
        }

class EditImageForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control'
            })
        }

