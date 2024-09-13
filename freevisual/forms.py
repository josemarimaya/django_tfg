from django import forms
from .models import Creator, Image, Provinces, Brand, Work

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

    tagged_users = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Etiqueta a otros creadores'
        }),
        label="Usuarios etiquetados",
        required=False
    )
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
    
    def save(self, commit=True):
        image = super().save(commit=False)
        tagged_users_str = self.cleaned_data['tagged_users']
        tagged_usernames = [u.strip()[1:] for u in tagged_users_str.split(',') if u.strip().startswith('@')]

        # Buscar los usuarios con esos usernames
        tagged_creators = Creator.objects.filter(username__in=tagged_usernames)

        # Guardar la imagen y luego establecer la relación ManyToMany
        if commit:
            image.save()
            image.tagged_creators.set(tagged_creators)
        return image

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

    work = forms.ModelMultipleChoiceField(
        queryset=Work.objects.all(),
        widget=forms.SelectMultiple(attrs={

            'class': 'form-select',
            'size': '8'
        }),  
        label = "Puestos de trabajo en los que tiene experiencia"
    )

    class Meta:
        model = Creator
        fields = ['profile_pic', 'description', 'provinces', 'brand', 'work']
        widgets = {
            'profile_pic': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control'
            })
        }

class EditImageForm(forms.ModelForm):

    tagged_users = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
        help_text="Agrega los usuarios etiquetados usando la notación @username separados por comas."
    )

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

    def __init__(self, *args, **kwargs):
        super(EditImageForm, self).__init__(*args, **kwargs)
        # Convertimos los usuarios etiquetados actuales en una cadena de texto para mostrarlos en el campo
        if self.instance.pk:
            tagged_usernames = ','.join([f"@{user.username}" for user in self.instance.tagged_creators.all()])
            self.fields['tagged_users'].initial = tagged_usernames

    def save(self, commit=True):
        instance = super(EditImageForm, self).save(commit=False)
        
        # Procesamos el campo 'tagged_users' para obtener los nombres de usuario
        tagged_usernames = self.cleaned_data['tagged_users']
        tagged_usernames_list = [username.strip().replace('@', '') for username in tagged_usernames.split(',') if username.strip()]

        # Buscamos los usuarios en la base de datos
        tagged_users = Creator.objects.filter(username__in=tagged_usernames_list)
        
        # Asignamos los usuarios etiquetados a la imagen
        instance.save()
        instance.tagged_creators.set(tagged_users)  # Actualizamos los usuarios etiquetados

        return instance

