from re import M
from django.shortcuts import render, redirect
from .models import Category, Product, Order, OrderItem, ShippingDetails

# categories view
def all_categories(request):
    categories = Category.get_all_categories()
    return render(request, "store/all_categories.html", {"categories": categories})

def products_by_category(request, slug):
    products = Product.get_all_products_by_category_slug(slug)
    return render(request, "store/products_by_category.html", {"products": products})

def product_detail(request, slug_cat, slug_prod):
    product = Product.objects.get(slug=slug_prod)
    device = request.COOKIES['device']
    try:
        order_item = OrderItem.objects.get(product=product)
        if request.method == 'POST':
            order, created = Order.objects.get_or_create(device=device, complete=False)
            orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
            orderItem.quantity=request.POST['quantity']
            orderItem.save()
            order_item = OrderItem.objects.get(product=product)
            return redirect('store:cart_view')
        else:
            try:
                order_item = OrderItem.objects.get(product=product)
                context = { 'product': product, 'order_item': order_item }
            except OrderItem.DoesNotExist:
                context = { 'product': product }

    except OrderItem.DoesNotExist:
        if request.method == 'POST':
            order, created = Order.objects.get_or_create(device=device, complete=False)
            orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
            orderItem.quantity=request.POST['quantity']
            orderItem.save()
            order_item = OrderItem.objects.get(product=product)
            return redirect('store:products_by_category', slug=slug_cat)
        else:
            try:
                order_item = OrderItem.objects.get(product=product)
                context = { 'product': product, 'order_item': order_item }
            except OrderItem.DoesNotExist:
                context = { 'product': product }

    return render(request, "store/product_detail.html", context)



def cart_view(request):
    order = Order.objects.get(device=request.COOKIES['device'], complete=False)
    order_items = OrderItem.objects.filter(order=order)

    if request.method == "POST":
        product=request.POST['product_id']
        order_item = OrderItem.objects.get(product=product)
        order_item.delete()
        
    if order_items:
        pass
    else:
        order.delete()
        return redirect('store:all_categories')

    return render(request, "store/cart.html", {"order_items": order_items})

def checkout(request, uuid):
    order = Order.objects.get(uuid=uuid)
    order_items = OrderItem.objects.filter(order=order)

    if request.method == "POST":
        data = request.POST
        print(data)
        shipping_details = ShippingDetails.objects.create(order=order, name=(data['firstName'] + " " + data['lastName']), email=data['email'], phone_number=data['phoneNumber'], address=data['address1'], address2=data['address2'], city=data['city'])
        print(shipping_details)
        return redirect('store:payment', uuid=uuid)
    return render(request, "store/checkout.html", {'order': order, 'order_items': order_items})

def payment(request, uuid):
    order = Order.objects.get(uuid=uuid)
    order_items = OrderItem.objects.filter(order=order)
    shipping_details = ShippingDetails.objects.get(order=order)
    payment_id = str(order.uuid)[0:8]

    if request.method == "POST":
        order.complete = True
        order.save()
        return redirect('store:all_categories')
    return render(request, "store/payment.html", {'order': order, 'order_items': order_items, 'shipping_details': shipping_details, 'payment_id': payment_id})