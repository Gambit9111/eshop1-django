from django.db import models
from datetime import date
from django.utils.text import slugify

class Category(models.Model):
    name= models.CharField(max_length=50)
    image= models.ImageField(upload_to='uploads/categories/')
    # create slug field and slugify name
    slug = models.SlugField(max_length=50, unique=True, null=True, blank=True, editable=False)
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    def get_absolute_url(self):
        return f"{self.slug}/"

    def __str__(self):
        return self.name


class Product(models.Model):

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True, editable=False)
    price= models.DecimalField(default=0, decimal_places=2, max_digits=10)
    category= models.ForeignKey(Category,on_delete=models.CASCADE)
    description= models.TextField(max_length=500, default='', blank=True, null= True)
    image= models.ImageField(upload_to='uploads/products/')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/store/{self.category.slug}/{self.slug}/"

    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_all_products_by_category_slug(slug):
        category = Category.objects.get(slug=slug)
        return Product.objects.filter(category=category)
    
    def __str__(self):
        return self.name
