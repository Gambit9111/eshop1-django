from django.urls import path
from .views import all_categories, products_by_category, product_detail, cart_view, checkout, payment, orders_admin_area

app_name = "store"
urlpatterns = [
    path("", all_categories, name="all_categories"),
    path("uzsakytigribai/", orders_admin_area, name="orders_admin_area"),
    path("cart/", cart_view, name="cart_view"),
    path('payment/<slug:uuid>/', payment, name="payment"),
    path('checkout/<slug:uuid>/', checkout, name="checkout"),
    path('<slug:slug>/', products_by_category, name="products_by_category"),
    path('<slug:slug_cat>/<slug:slug_prod>/', product_detail, name="product_detail"),
]