from django import forms
from .models import Books, Reviews
from django.urls import reverse
from users.models import PersoUser
from django.core.validators import MinValueValidator, MaxValueValidator


class CreateFreeForm(forms.ModelForm):

    original_poster = forms.ModelMultipleChoiceField(required=True,
                                                     queryset=PersoUser.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:

        model = Books
        fields = ["title", "original_poster", "genre", "author",
                  "pub_date", "cover", "pdf", "summary"]


class CreateNonFreeForm(forms.ModelForm):

    original_poster = forms.ModelMultipleChoiceField(label="co-author",
                                                     queryset=PersoUser.objects.all(), widget=forms.CheckboxSelectMultiple)
    price = forms.DecimalField(
        max_digits=5, decimal_places=2, required=True, validators=[
            MinValueValidator(1)

        ], help_text="Must be higher or equal to 1", widget=forms.TextInput(attrs={"placeholder": "Your price "}))

    class Meta:
        model = Books
        fields = ["title", "original_poster", "genre", "price",
                  "pub_date", "cover", "pdf", "summary"]


class UpdateFreeForm(forms.ModelForm):

    class Meta:

        model = Books
        fields = ["title", "genre", "author",
                  "pub_date", "cover", "pdf", "summary"]


class UpdateNonFreeForm(forms.ModelForm):

    price = forms.DecimalField(
        max_digits=5, decimal_places=2, required=True, validators=[
            MinValueValidator(1)

        ], help_text="Must be higher or equal to 1", widget=forms.TextInput(attrs={"placeholder": "Your price "}))

    class Meta:
        model = Books
        fields = ["title", "genre", "price",
                  "pub_date", "cover", "pdf", "summary"]


class ReviewForm(forms.ModelForm):

    class Meta:

        model = Reviews
        fields = ["title", "commentary"]
