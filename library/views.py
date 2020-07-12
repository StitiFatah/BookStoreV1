from django.shortcuts import render, redirect, reverse
from users.models import PersoUser
from books.models import Books, OrderItem
from .models import FreeLibrary
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.contrib import messages


@login_required
def Library(request):

    library = OrderItem.objects.filter(user=request.user, ordered=True)
    free_library = FreeLibrary.objects.filter(user=request.user)

    context = {"library": library,
               "free_library": free_library}

    return render(request, "library/main.html", context)


@login_required
def add_free_book_to_library(request, book_id):
    if not Books.objects.get(pk=book_id).is_free():
        raise PermissionDenied
    elif FreeLibrary.objects.filter(user=request.user, item=Books.objects.get(pk=book_id)).exists():
        messages.info(request, "This book is already in your library")
    else:
        FreeLibrary.objects.create(
            item=Books.objects.get(pk=book_id), user=request.user)
        messages.info(request, "This book was added to your library")

    return redirect(reverse("books:detail-books", kwargs={"book_id": book_id}))


@login_required
def remove_free_book_from_library(request, book_id):

    if FreeLibrary.objects.filter(user=request.user, item=Books.objects.get(pk=book_id)).exists():
        FreeLibrary.objects.filter(
            user=request.user, item=Books.objects.get(pk=book_id)).delete()

    else:
        messages.info(request, "This book isn't in your card")

    return redirect(reverse("library:main-library"))
