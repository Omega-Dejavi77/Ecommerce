import os
from django.db import models
from django.db.backends.base import features


def get_filename_ext(filename):
    base_name = os.path.basename(filename)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image_path(instance, filename):
    # TODO
    filename, ext = get_filename_ext(filename)
    filename = str(filename).replace(' ', '_')
    final_file_name = '{filename}{ext}'.format(filename=filename, ext=ext)
    return 'products/{filename}/{final_filename}'.format(filename=filename, final_file_name=final_file_name)


class ProductQuerySet(models.query.QuerySet):
    def featured(self):
        return self.get_queryset().filter(featured=True, active=True)
    
    def active(self):
        return self.get_queryset().filter(active=True)


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)
    
    def all(self):
        return self.get_queryset().active()

    def featured(self): # Products.objects.featured()
        return self.get_queryset().featured()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

class Product(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=19, default=39.99)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    objects = ProductManager()

    def __str__(self) -> str:
        return self.title