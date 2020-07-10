from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.views import generic
from .models import (Books, Reviews,
                     OrderItem, BillingAddress, Order)
from django.utils import timezone
from .forms import (CreateFreeForm, CreateNonFreeForm,
                    UpdateFreeForm, UpdateNonFreeForm,
                    ReviewForm, CheckoutForm)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied
from users.models import PersoUser


def home_display_books(request):
    main_list = Books.objects.order_by(
        "title").filter(pub_date__lte=timezone.now())
    paginator = Paginator(main_list, 24)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    side_list = Books.objects.order_by(
        "-pub_date").filter(pub_date__lte=timezone.now())[:5]
    context = {"page_obj": page_obj, "side_list": side_list}

    return render(request, "books/first_page.html", context)


def search_nav(request, requested_genre):
    filtered_list = Books.objects.filter(
        genre=requested_genre).filter(pub_date__lte=timezone.now())
    paginator = Paginator(filtered_list, 24)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj, "GENRE": requested_genre}
    return render(request, "books/search_nav.html", context)


class IndexViews_search(generic.ListView):
    model = Books
    template_name = "books/index_search.html"
    context_object_name = "books"

    def get_queryset(self):
        target_query = self.request.GET.get("searchtarget")
        user_query = self.request.GET.get("search").strip()
        author_query = get_user_model().objects.filter(username__icontains=user_query)

        def ids():
            l = []
            for users in author_query:
                l.append(users.ID)
            return l

        if target_query == "title":
            return Books.objects.filter(title__icontains=user_query).filter(pub_date__lte=timezone.now())
        elif target_query == "author":

            return Books.objects.filter(original_poster__in=ids()).filter(pub_date__lte=timezone.now())


class IndexViews_specific_search(generic.ListView):
    model = Books
    template_name = "books/index_specific_search.html"
    context_object_name = "books"

    def get_queryset(self):
        requested_genre = self.kwargs['requested_genre']
        target_query = self.request.GET.get("searchtarget")
        user_query = self.request.GET.get("search").strip()
        author_query = get_user_model().objects.filter(username__icontains=user_query)

        def ids():
            l = []
            for users in author_query:
                l.append(users.ID)
            return l

        if target_query == "title":
            return Books.objects.filter(genre=requested_genre).filter(title__icontains=user_query).filter(pub_date__lte=timezone.now())
        elif target_query == "author":

            return Books.objects.filter(genre=requested_genre).filter(original_poster__in=ids()).filter(pub_date__lte=timezone.now())


def DetailBook(request, book_id):
    book = get_object_or_404(Books, pk=book_id)
    book_original_poster = book.original_poster.all()
    same_author = Books.objects.filter(
        original_poster__in=book_original_poster).filter(pub_date__lte=timezone.now()).exclude(pk=book_id).distinct()
    book_reviews = book.reviews_set.all()
    context = {"book": book,
               "same_author": same_author,
               "book_reviews": book_reviews
               }

    return render(request, "books/detail.html", context)


@login_required
def create_book(request):
    if request.method == "POST":
        form = CreateFreeForm(request.POST, request.FILES)
        if form.is_valid():
            new_book = form.save(commit=False)
            if request.user not in new_book.original_poster.all():
                new_book.save()
                form.save_m2m()
                new_book.original_poster.add(
                    PersoUser.objects.get(pk=request.user.ID))

            return HttpResponseRedirect(reverse("books:detail-books", kwargs={"book_id": new_book.ID}))
    else:
        form = CreateFreeForm()

    return render(request, "books/create_book.html", {"form": form})


@login_required
def create_non_free_book(request):
    if request.method == "POST":
        form = CreateNonFreeForm(request.POST, request.FILES)
        if form.is_valid():
            new_book = form.save(commit=False)
            if request.user not in new_book.original_poster.all():
                new_book.save()
                form.save_m2m()
                new_book.original_poster.add(
                    PersoUser.objects.get(pk=request.user.ID))

            return HttpResponseRedirect(reverse("books:detail-books", kwargs={"book_id": new_book.ID}))
    else:
        form = CreateNonFreeForm(
        )

    return render(request, "books/create_book.html", {"form": form})


@login_required
def update_free_book(request, book_id):

    book = get_object_or_404(Books, pk=book_id)
    if request.user not in book.original_poster.all() and request.user.is_admin is False:
        raise PermissionDenied

    if request.method == "POST":
        form = UpdateFreeForm(request.POST, request.FILES,
                              instance=Books.objects.get(pk=book_id))
        if form.is_valid():
            updated_book = form.save(commit=False)
            updated_book.price = 0

            updated_book.save()
            form.save_m2m()

            return HttpResponseRedirect(reverse("books:detail-books", kwargs={"book_id": updated_book.ID}))
    else:
        form = UpdateFreeForm(instance=Books.objects.get(pk=book_id))

    context = {"form": form, "book": book}

    return render(request, "books/update_book.html", context)


@login_required
def update_non_free_book(request, book_id):
    book = get_object_or_404(Books, pk=book_id)
    if request.user not in book.original_poster.all() and request.user.is_admin is False:
        raise PermissionDenied

    if request.method == "POST":
        form = UpdateNonFreeForm(request.POST, request.FILES,
                                 instance=Books.objects.get(pk=book_id))
        if form.is_valid():
            updated_book = form.save(commit=True)

            return HttpResponseRedirect(reverse("books:detail-books", kwargs={"book_id": updated_book.ID}))
    else:
        form = UpdateNonFreeForm(instance=Books.objects.get(pk=book_id))

    context = {"form": form, "book": book}

    return render(request, "books/update_book.html", context)


class DeleteBook(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Books

    template_name = "books/delete_book.html"
    success_url = "/"

    def test_func(self):
        book = self.get_object()
        if self.request.user in book.original_poster.all() or self.request.user.is_admin:
            return True
        return False


class CreateReview(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = Reviews
    form_class = ReviewForm
    template_name = "books/create_review.html"

    def form_valid(self, form):
        form.instance.poster = self.request.user
        form.instance.book = Books.objects.get(ID=self.kwargs['book_id'])
        form.instance.date = timezone.now()
        return super().form_valid(form)

    def test_func(self):
        book = Books.objects.get(ID=self.kwargs['book_id'])
        reviews_posted_here = book.reviews_set.filter(poster=self.request.user)
        if len(reviews_posted_here) == 0:
            return True
        return False


class UpdateReview(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Reviews
    form_class = ReviewForm
    template_name = "books/update_review.html"

    def test_func(self):
        review = self.get_object()
        if review.poster == self.request.user or self.request.user.is_admin:
            return True
        return False


class DeleteReview(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Reviews
    template_name = "books/delete_review.html"
    success_url = "/"

    def test_func(self):
        review = self.get_object()
        if review.poster == self.request.user or self.request.user.is_admin:
            return True
        return False


# class search_nav(generic.ListView):
#     model = Books
#     template_name = "books/search_nav.html"
#     context_object_name = "books"

#     def get_queryset(self):
#         Genre = self.kwargs["requested_genre"]
#         return Books.objects.filter(genre=Genre)


@login_required
def Cart_display_view(request):
    user_cart = OrderItem.objects.filter(user=request.user).distinct()

    def get_total_price():
        total = 0
        for i in user_cart:
            total += i.item.price
        return total

    context = {"user_cart": user_cart, "total_price": get_total_price()}

    return render(request, "books/user_cart.html", context)


@login_required
def add_item_to_cart(request, book_id):
    if Books.objects.get(pk=book_id).is_free():
        raise PermissionDenied

    if OrderItem.objects.filter(user=request.user, item=Books.objects.get(pk=book_id)).exists():
        messages.info(request, "This Item is already in your cart")

    else:
        new_item = OrderItem.objects.create(
            item=Books.objects.get(pk=book_id), user=request.user)
        messages.info(request, "The book was added to your cart")

    return redirect(reverse("books:detail-books", kwargs={"book_id": book_id}))


@login_required
def remove_item_from_cart(request, book_id):

    if OrderItem.objects.filter(user=request.user, item=Books.objects.get(pk=book_id)).exists():
        OrderItem.objects.filter(
            user=request.user, item=Books.objects.get(pk=book_id)).delete()

    else:
        messages.info(request, "This book isn't in your card")

    return redirect(reverse("books:user-cart"))


@login_required
def empty_cart(request):
    if OrderItem.objects.filter(user=request.user).exists():

        OrderItem.objects.filter(
            user=request.user).delete()
        messages.info(request, "Your card is now empty")

    else:
        messages.info(request, "Your card is already empty")

    return redirect(reverse("books:user-cart"))


@login_required
def create_order(request):
    if OrderItem.objects.filter(user=request.user, ordered=False).exists():
        print("YES")
        Order.objects.filter(user=request.user, ordered=False).all().delete()
        new_order = Order.objects.create(user=request.user, ordered=False,
                                         order_date=timezone.now())

        for product in OrderItem.objects.filter(user=request.user):
            new_order.items.add(product)
            new_order.save()

    else:
        print("NO")
        messages.info(request, "Your cart is actually empty",
                      )
        return redirect(reverse("books:display-books"))

    return redirect(reverse("books:checkout"))


@login_required
def checkout(request):
    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            STREET = form.cleaned_data["street_address"]
            APPARTMENT = form.cleaned_data["appartment_address"]
            COUNTRY = form.cleaned_data["country"]
            ZIP = form.cleaned_data["zip"]
            PAYMENT_OPTION = form.cleaned_data["payment_options"]
            SAVE = form.cleaned_data["remember"]

            new_address = BillingAddress(user=request.user, street_address=STREET,
                                         appartment_address=APPARTMENT, country=COUNTRY, zip=ZIP)

            if BillingAddress.objects.filter(user=request.user, street_address=STREET,
                                             appartment_address=APPARTMENT, country=COUNTRY, zip=ZIP).exists():
                if SAVE == True:
                    existing_address = BillingAddress.objects.get(user=request.user, street_address=STREET,
                                                                  appartment_address=APPARTMENT, country=COUNTRY, zip=ZIP)
                    existing_address.auto_complete = True

                    existing_address.save()

                pass

            else:
                if SAVE == True:
                    new_address.auto_complete = True
                new_address.save()

            actual_order = Order.objects.filter(
                user=request.user, ordered=False).get()

            actual_order.billing_address = BillingAddress.objects.get(user=request.user, street_address=STREET,
                                                                      appartment_address=APPARTMENT, country=COUNTRY, zip=ZIP)
            actual_order.save()

            return redirect("books:checkout")

    else:
        form = CheckoutForm()

    return render(request, "books/checkout_page.html", {"form": form})
