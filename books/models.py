from django.db import models
import uuid
from users.models import PersoUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.utils import timezone
from django_countries.fields import CountryField


class Books(models.Model):

    # def get_absolute_url(self):
    #     return reverse("books:detail-books", kwargs={"book_id": self.pk})

    #####     genres   ##########
    # fictionnal genres
    CLASSIC = "cla"
    DRAMA = "dra"
    FABLE = "fab"
    FAIRYTAIL = "ft"
    FANTASY = "fant"
    FICTION = "fic"
    FOLKLORE = "folk"
    HFICTION = "hfic"
    SFICTION = "sfic"
    RFICTION = "rfic"
    HORROR = "hor"
    LEGEND = "leg"
    MYSTERY = "mystery"
    POETRY = "poe"
    MYTHOLOGY = "myth"
    ROMANCE = "romance"
    SATIRE = "sat"
    SHORTSTORY = "shortstory"
    SWASHBUCKLER = "swb"
    THRILLER = "thr"
    TRAVEL = "trv"
    WESTERN = "west"
    HUMOR = "hum"
    NOVEL = "nov"


# Non Fictionnal genres

    BIOGRAPHY = "bio"
    ESSAY = "ess"
    JOURNALISM = "journalism"
    MEMOIR = "memoire"
    NARRATIVENONFICTION = "nnf"
    REFERENCEBOOK = "refbook"
    SELFHELPBOOK = "selfhbook"
    SPEECH = "speech"
    TEXTBOOK = "textbook"

# Image books

    COMICS = "comics"
    MANGAS = "mangas"
    BD = "bd"

# other

    OTHER = "other"
##### GENRE LIST ####

    GENRE_LIST = [


        ('FICTION',

         (
             (CLASSIC, "Classic"),
             (NOVEL, "Novel"),
             (DRAMA, "Drama"),
             (FABLE, "Fable"),
             (FAIRYTAIL, "Fairy Tail"),
             (FANTASY, "Fantasy"),
             (FICTION, "Fiction"),
             (FOLKLORE, "Folkore"),
             (HFICTION, "Historical fiction"),
             (HORROR, "Horror"),
             (LEGEND, "Legend"),
             (MYSTERY, "Mystery"),
             (POETRY, "Poetry"),
             (MYTHOLOGY, "Mythology"),
             (ROMANCE, "Romancd"),
             (SATIRE, "Satire"),
             (SHORTSTORY, "Shortstory"),
             (SWASHBUCKLER, "Swashbuckler"),
             (THRILLER, "Thriller"),
             (TRAVEL, "Travel"),
             (WESTERN, "Western"),
             (SFICTION, "Science Fiction"),
             (RFICTION, "Realistic Fiction"),
             (HUMOR, "Humor")







         )

         ),

        ('NONFICTION',

         (
             (BIOGRAPHY, "Biography"),
             (ESSAY, "Essay"),
             (JOURNALISM, "Journalism"),
             (MEMOIR, "Memoir"),
             (NARRATIVENONFICTION, "Narrative non fiction"),
             (REFERENCEBOOK, "Reference Book"),
             (SELFHELPBOOK, "Self Help Book"),
             (SPEECH, "Speech"),
             (TEXTBOOK, "textbook")
         )
         ),


        ('Image Books',

         (
             (COMICS, "Comics"),
             (BD, "Bd"),
             (MANGAS, "Mangas")


         ),

         ),


        ('OTHER',
         (
             (OTHER, "Other Genre"),

         )
         )



    ]

    genre = models.CharField(
        max_length=50,
        choices=GENRE_LIST,
        default=CLASSIC,

    )

#### language ######
    ENGLISH = "en"
    FRENCH = "fr"
    SPANISH = "sp"
    ARABIC = "ar"
    GERMAN = "ger"
    DEUTCH = "de"
    ITALIAN = "it"
    RUSSIAN = "ru"
    CHINESE = "chi"
    JAPANESE = "jap"
    LANGUAGE_LIST = [
        (ENGLISH, "English"),
        (GERMAN, "German"),
        (ARABIC, "Arabic"),
        (FRENCH, "French"),
        (SPANISH, "Spanish"),
        (JAPANESE, "Japanese"),
        (ITALIAN, "Italian"),
        (RUSSIAN, "Russian"),
        (JAPANESE, "Japanese"),
        (CHINESE, "Chinese"),
    ]

    language = models.CharField(
        max_length=3,
        choices=LANGUAGE_LIST,
        default=ENGLISH,
    )
##########
    ID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, blank=False)
    author = models.CharField(
        verbose_name="Author (if not you)", max_length=200, blank=True, null=True)
    pub_date = models.DateField(null=False, blank=False, default=timezone.now)

    original_poster = models.ManyToManyField(
        PersoUser)

    price = models.DecimalField(default=0,
                                max_digits=6, decimal_places=2, null=False, validators=[
                                    MinValueValidator(0)
                                ])

    cover = models.ImageField(
        default="cover/default_cover.jpg", upload_to="cover")

    pdf = models.FileField(upload_to="pdf_files", null=False)

    summary = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} de {self.author}"

    def is_free(self):
        if self.price > 0:
            return False
        return True


class Reviews(models.Model):
    def get_absolute_url(self):
        return reverse("books:detail-books", kwargs={"book_id": self.book.pk})

    book = models.ForeignKey(Books, to_field="ID", on_delete=models.CASCADE)
    poster = models.ForeignKey(
        PersoUser, to_field="ID", on_delete=models.CASCADE)
    title = models.CharField(max_length=500, blank=True)
    commentary = models.TextField(blank=False)
    date = models.DateField(null=False)

    def __str__(self):
        return f"{self.poster} | {self.book} | {self.title}"


class OrderItem(models.Model):
    user = models.ForeignKey(PersoUser, to_field="ID",
                             on_delete=models.CASCADE)
    item = models.ForeignKey(Books, to_field="ID", on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.item.title


class BillingAddress(models.Model):
    user = models.ForeignKey(PersoUser, to_field="ID",
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=200)
    appartment_address = models.CharField(max_length=200)
    country = CountryField(multiple=True)
    zip = models.CharField(max_length=20)
    auto_complete = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Order(models.Model):
    user = models.ForeignKey(PersoUser, to_field="ID",
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    billing_address = models.ForeignKey(
        BillingAddress, on_delete=models.SET_NULL, blank=True, null=True)
    ordered = models.BooleanField(default=False)
    order_date = models.DateTimeField()

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for ordered_items in self.items.all():
            total += ordered_items.item.price
        return total
