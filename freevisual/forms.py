from django import forms
from .models import Creator, Image, Provinces, Brand, Work, Tags

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
        label = "Provincias en las que trabajas",
        required = False
    )

    brand = forms.ModelMultipleChoiceField(
        queryset=Brand.objects.all(),
        widget=forms.SelectMultiple(attrs={

            'class': 'form-select',
            'size': '8'
        }),  
        label = "Marcas de herramientas con las que has trabajado",
        required = False
    )

    work = forms.ModelMultipleChoiceField(
        queryset=Work.objects.all(),
        widget=forms.SelectMultiple(attrs={

            'class': 'form-select',
            'size': '8'
        }),  
        label = "Puestos de trabajo en los que tiene experiencia",
        required = False
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
        help_text="Agrega los usuarios etiquetados usando la notación @username separados por comas.",
        label="Usuarios etiquetados"
    )

    tags = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
        help_text="Agrega los tags usando la notación #tag separados por comas.",
        label="Etiquetas asociadas"
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

            tag_names = ','.join([f"#{tag.name}" for tag in self.instance.tags.all()])
            self.fields['tags'].initial = tag_names

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

        # Procesamos el campo 'tags' para obtener los nombres de tags
        tags_input = self.cleaned_data['tags']
        tag_names_list = [tag.strip().replace('#', '') for tag in tags_input.split(',') if tag.strip()]

        # Buscamos o creamos los tags en la base de datos
        tags = []
        for tag_name in tag_names_list:
            tag, created = Tags.objects.get_or_create(name=tag_name)
            tags.append(tag)

        # Asignamos los tags a la imagen
        instance.tags.set(tags)  # Actualizamos los tags asociados

        return instance


class EditImageForm_v2(forms.ModelForm):
    tagged_users = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
        help_text="Agrega los usuarios etiquetados usando la notación @username separados por comas.",
        label="Usuarios etiquetados"
    )

    tags = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
        help_text="Agrega los tags usando la notación #tag separados por comas.",
        label="Etiquetas asociadas"
    )

    class Meta:
        model = Image
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Corrección: Llamar a super sin especificar clase y self
        if self.instance.pk:
            # Muestra usuarios ya etiquetados
            tagged_usernames = ','.join([f"@{user.username}" for user in self.instance.tagged_creators.all()])
            self.fields['tagged_users'].initial = tagged_usernames

            # Muestra tags ya asociados
            tag_names = ','.join([f"#{tag.name}" for tag in self.instance.tags.all()])
            self.fields['tags'].initial = tag_names

        # Listado de etiquetas válidas para el sistema (puede añadirse como `help_text` o mostrar debajo del campo)
        valid_tags = Tags.objects.all().values_list('name', flat=True)
        self.fields['tags'].help_text += f" Etiquetas válidas: {', '.join([f'#{tag}' for tag in valid_tags])}"

    def save(self, commit=True):
        instance = super().save(commit=False)  # Corrección: super() sin parámetros

        # Procesa los usuarios etiquetados
        tagged_usernames = self.cleaned_data['tagged_users']
        tagged_usernames_list = [username.strip().replace('@', '') for username in tagged_usernames.split(',') if username.strip()]
        tagged_users = Creator.objects.filter(username__in=tagged_usernames_list)
        instance.save()
        instance.tagged_creators.set(tagged_users)

        # Procesa las etiquetas
        tags_input = self.cleaned_data['tags']
        tag_names_list = [tag.strip().replace('#', '') for tag in tags_input.split(',') if tag.strip()]
        tags = [Tags.objects.get_or_create(name=tag_name)[0] for tag_name in tag_names_list]
        instance.tags.set(tags)

        return instance
