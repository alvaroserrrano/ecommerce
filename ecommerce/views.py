from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Item, OrderItem, Order
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from django.contrib.auth.decorators import login_required

class HomeView(ListView):
    model = Item
    paginate_by = 10
    template_name= 'home-page.html'

class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order=Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order-summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, 'You do not have an active order')
            return redirect('/')

class ItemDetailView(DetailView):
    model = Item
    template_name = 'product-page.html'

def checkout(request):
    context={
        'items': Item.objects.all()
    }
    return render(request, 'checkout-page.html', context)

@login_required
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
            return redirect("ecommerce:order-summary")
        else:
            messages.info(request, 'Item added to the cart')
            order.items.add(order_item)
            return redirect("ecommerce:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered=False, ordered_date =ordered_date)
        order.items.add(order_item)
        return redirect("ecommerce:order-summary")

@login_required
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
            return redirect('ecommerce:order-summary')
        else:
            #item not in order
            messages.info(request, "Item was not in your cart")
            return redirect('ecommerce:product', slug=slug)
    else:
        #user does not have an order
        messages.info(request, 'No active order was found')
        return redirect("ecommerce:product", slug=slug)

@login_required
def remove_single_item_from_cart(request,slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        #order item in order?
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, 'This item quantity was updated')
            return redirect('ecommerce:order-summary')
        else:
            messages.info(request, 'Item not found in your cart')
            return redirect('ecommerce:product', slug=slug)
    else:
        messages.info(request, 'You do not have an active order')
        return redirect("ecommerce:product", slug=slug)
