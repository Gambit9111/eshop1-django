from django.db import models
from datetime import date
from django.utils.text import slugify
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator

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

class Order(models.Model):
	device = models.CharField(max_length=100, editable=False)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	uuid = models.UUIDField(default=uuid.uuid4, editable=False)

	def __str__(self):
		return str(self.uuid) + " - " + str(self.date_ordered) + " - " + str(self.complete)
		
	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total 

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total 

class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, editable=False)
	order = models.ForeignKey(Order, on_delete=models.CASCADE, editable=False)
	quantity = models.IntegerField(default=1, null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(5)])
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.order.uuid) + " - " + str(self.product) + " - " + str(self.quantity)

	@property
	def get_total(self):
		total = float(self.product.price) * int(self.quantity)
		return total