from django.contrib import admin
from .models import Books, Reviews
from users.models import PersoUser


class ReviewInLine(admin.TabularInline):
    model = Reviews
    extra = 1


class BooksAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Identification", {"fields": [
            "title",  "genre", "original_poster", "cover", "author"]}),
        ("Ordering", {"fields": ["pub_date", "language"]
                      # , "classes":["collapse"]
                      }),
        ("Price", {"fields": ["price"]}),
        ("Summary", {"fields": ["summary"]}),
        ("File", {"fields": ["pdf"]})

    ]

    list_display = ("title",
                    "pub_date", "price", "genre")
    list_filter = ["pub_date",
                   "original_poster", "language", "price", "genre"]
    search_fields = ["original_poster",
                     "pub_date",  "language", "genre", ]

    inlines = [ReviewInLine]


admin.site.register(Books, BooksAdmin)
