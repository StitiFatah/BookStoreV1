from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import PersoUser, Profile


class PersoUserRegisterForm(forms.ModelForm):

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = PersoUser
        fields = ["username", "email", "first_name",
                  "last_name", "date_of_birth",  "password1", "password2"]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

# Could have benn :

# class CustomUserCreationForm(UserCreationForm):
# class Meta:
# model = get_user_model()
# fields = ('email', 'username',)


class PersoUserUpdateForm(forms.ModelForm):
    # email = forms.EmailField(label="Email Adress", required=True)

    class Meta:
        model = PersoUser
        fields = ["username", "first_name",
                  "last_name"]

    # def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        # return self.initial["password"]

# Could have been

# class CustomUserChangeForm(UserChangeForm):
# class Meta:
# model = get_user_model()
# fields = ('email', 'username',)


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio"]
