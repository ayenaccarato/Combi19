from django import forms
from combi19app.models import Usuario
#from django.contrib.auth import get_user_model

#Usuario = get_user_model()

class Registro (forms.ModelForm):
    #password = forms.CharField(label='Contraseña', widget= forms.CharField(max_length=10))

    class Meta:
        model = Usuario
        fields = ('usuario',
                   'password',
                   'nombre',
                   'apellido',
                   'dni',
                   'direccion',
                   'email',
                   'telefono',
                   )

    def save(self, commit=True):
        usuario = super().save(commit= False)
        usuario.set_password(self.cleaned_data['password'])
        if commit:
            usuario.save()
        return usuario
