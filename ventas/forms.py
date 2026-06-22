from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegistroCompletoForm(UserCreationForm):
    """Formulario para capturar datos adicionales durante el registro"""
    email = forms.EmailField(
        required=True, 
        label="Correo Electrónico",
        widget=forms.EmailInput(attrs={'placeholder': 'ejemplo@correo.com'})
    )
    first_name = forms.CharField(
        max_length=100, 
        required=True, 
        label="Nombres",
        widget=forms.TextInput(attrs={'placeholder': 'Tus nombres'})
    )
    last_name = forms.CharField(
        max_length=100, 
        required=True, 
        label="Apellidos",
        widget=forms.TextInput(attrs={'placeholder': 'Tus apellidos'})
    )
    # NUEVO CAMPO: Teléfono capturado en el registro
    telefono = forms.CharField(
        max_length=15, 
        required=True, 
        label="Teléfono de Contacto",
        widget=forms.TextInput(attrs={'placeholder': 'Ej: 0998877665'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            # Aquí podrías guardar el teléfono en un perfil si lo tuvieras, 
            # por ahora se captura para ser usado en el flujo de la app.
        return user

class PerfilForm(forms.ModelForm):
    """Formulario para que el usuario actualice sus datos básicos"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'email': 'Correo Electrónico',
        }