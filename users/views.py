from django.shortcuts import render, redirect, get_object_or_404
from .models import PersoUser
from .forms import PersoUserRegisterForm, PersoUserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.urls import reverse_lazy
from books.models import Books

#############################################################

# register using function view

# def register(request):
#     if request.method == "POST":
#         form = PersoUserRegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get("username")
#             messages.success(
#                 request, f"Thanks for creating an Account,{username}")
#             return redirect("pages:Home")
#     else:
#         form = PersoUserRegisterForm()

#     return render(request, "users/register.html", {"form": form})


# easier registration way through class based view

class SignUpPageView(generic.CreateView):
    form_class = PersoUserRegisterForm
    success_url = reverse_lazy("login")
    template_name = "users/register.html"


######### NO LONGER NEEDED IF USING ALLAUTH ###################

###########################################################


@login_required
def private_profile(request):
    if request.method == "POST":
        u_form = PersoUserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(
                request, "Your informations have been successfully updated")
            return redirect("users:update_profile")

    else:
        u_form = PersoUserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    my_books = Books.objects.filter(original_poster=request.user)

    context = {"u_form": u_form,
               "p_form": p_form,
               "my_books": my_books,

               }

    return render(request, "users/private_profile.html", context)


def PublicProfile(request, user_id):

    perso_user = get_object_or_404(PersoUser, pk=user_id)
    same_author_books = Books.objects.filter(original_poster=perso_user)

    context = {"perso_user": perso_user,
               "same_author_books": same_author_books,
               }

    return render(request, "users/public_profile.html", context)
