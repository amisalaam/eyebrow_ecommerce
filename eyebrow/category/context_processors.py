from .models import category
from carts.models import CartItem


def menu_links(request):
    links = category.objects.all()
    return dict(links=links) 


    