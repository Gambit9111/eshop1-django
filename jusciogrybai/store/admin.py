from django.contrib import admin
import django.apps

from .models import Product, Category, Order, OrderItem, ShippingDetails

models = django.apps.apps.get_models()

for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass