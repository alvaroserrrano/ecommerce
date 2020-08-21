from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Item, OrderItem, Order
from django.views.generic import ListView, DetailView
from django.utils import timezone

class HomeView(ListView):
    model = Item
    template_name= 'ecommerce/home-page.html'

class ItemDetailView(DetailView):
    model = Item
    template_name = 'ecommerce/product-page.html'

def checkout(request):
    context={
        'items': Item.objects.all()
    }
    return render(request, 'ecommerce/checkout-page.html', context)

def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, 'Item quantity successfully updated')
            return redirect("ecommerce:product", slug=slug)
        else:
            messages.info(request, 'Item added to the cart')
            order.items.add(order_item)
            return redirect("ecommerce:product", slug=slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered=False, ordered_date =ordered_date)
        order.items.add(order_item)
        return redirect("ecommerce:product", slug=slug)

def remove_from_cart(request, slug):
    item= get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        #order item in order?
        if order.items.filter(item__slug=item.slug).exists():
            order_item=OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, 'Item removed from cart')
            #TODO
            #return redirect('ecommerce:order-summary')
            return redirect("ecommerce:product", slug=slug)
        else:
            #item not in order
            messages.info(request, "Item was not in your cart")
            return redirect('ecommerce:product', slug=slug)
    else:
        #user does not have an order
        messages.info(request, 'No active order was found')
        return redirect("ecommerce:product", slug=slug)


