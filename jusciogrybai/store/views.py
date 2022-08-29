from django.shortcuts import render
from .models import Category, Product, Order, OrderItem

# categories view
def all_categories(request):
    categories = Category.get_all_categories()
    return render(request, "store/all_categories.html", {"categories": categories})

def products_by_category(request, slug):
    products = Product.get_all_products_by_category_slug(slug)
    return render(request, "store/products_by_category.html", {"products": products})

def product_detail(request, slug_cat, slug_prod):
    product = Product.objects.get(slug=slug_prod)

    if request.method == 'POST':
        product = Product.objects.get(slug=slug_prod)
        device = request.COOKIES['device']
        print(request.POST)
        print(device)
        order, created = Order.objects.get_or_create(device=device, complete=False)
        print(order)
        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
        orderItem.quantity=request.POST['quantity']
        orderItem.save()
        order_item = OrderItem.objects.get(product=product)
        context = { 'product': product, 'order_item': order_item }
    else:
        try:
            order_item = OrderItem.objects.get(product=product)
            context = { 'product': product, 'order_item': order_item }
            print(order_item.quantity)
        except OrderItem.DoesNotExist:
            context = { 'product': product }

    return render(request, "store/product_detail.html", context)