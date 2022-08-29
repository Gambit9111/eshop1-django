from .models import Order

def get_order(request):
    try:
        device = request.COOKIES['device']
        my_order = Order.objects.get(device=device, complete=False)
        return {"my_order": my_order}
    except:
        return {"my_order": None}