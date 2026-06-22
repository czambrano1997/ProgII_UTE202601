from django import forms

from .models import Actor, Obra


class ObraForm(forms.ModelForm):
    class Meta:
        model = Obra
        fields = ['titulo', 'descripcion', 'duracion_min', 'fecha_estreno']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
            'fecha_estreno': forms.DateInput(attrs={'type': 'date'}),
        }


class ActorForm(forms.ModelForm):
    class Meta:
        model = Actor
        fields = ['nombre', 'edad', 'nacionalidad', 'email']
        widgets = {
            'email': forms.EmailInput(),
        }
