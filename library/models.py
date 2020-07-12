from django.db import models
from users.models import PersoUser
from books.models import Books


class FreeLibrary(models.Model):
    user = models.ForeignKey(PersoUser, to_field="ID",
                             on_delete=models.CASCADE)
    item = models.ForeignKey(Books, to_field="ID", on_delete=models.CASCADE)

    def __str__(self):
        return self.item.title
