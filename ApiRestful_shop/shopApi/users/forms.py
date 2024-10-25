from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser
import products.models as productsModels
from django.utils.translation import gettext_lazy as _


class CustomUserCreationForm (UserCreationForm):
    password1 = forms.CharField(label=_("Mot de passe"), widget=forms.PasswordInput(attrs={'type': 'password'}),max_length=30)
    password2 = forms.CharField(label=_("Confirmer le mot de passe"), widget=forms.PasswordInput(attrs={'type': 'password'}),max_length=30)

    class Meta:
        model = CustomUser
        fields = ['birth_date','first_name','last_name','email','password1','password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            panier = productsModels.Panier(user=user)
            panier.save()
        return user


class CustomAuthenticationForm (forms.Form):

    email = forms.EmailField(max_length=100,required=True,label=_("Email"),widget=forms.EmailInput(attrs={"type":"email","id":"id_email2","autocomplete":"email"}))
    password = forms.CharField(max_length=30,required=True,label=_("Mot de passe"),widget=forms.PasswordInput(attrs={"type":"password"}))