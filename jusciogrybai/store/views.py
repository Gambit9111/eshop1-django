from django.shortcuts import render
from .models import Category, Product

# categories view
def all_categories(request):
    categories = Category.get_all_categories()
    return render(request, "store/all_categories.html", {"categories": categories})

def products_by_category(request, slug):
    products = Product.get_all_products_by_category_slug(slug)
    print(products)
    return render(request, "store/products_by_category.html", {"products": products})

def product_detail(request, slug_cat, slug_prod):
    print(slug_cat, slug_prod)
    product = Product.objects.get(slug=slug_prod)
    return render(request, "store/product_detail.html", {"product": product})