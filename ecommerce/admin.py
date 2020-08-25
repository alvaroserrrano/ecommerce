from django.contrib import admin

from .models import Item, OrderItem, Order, Payment, Coupon, Address,  UserProfile

def accept_refund(modeladmin, request, queryset):
    queryset.update(refund_request=False, refund_granted=True)

accept_refund.short_description = 'Update orders to refund granted'

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                'ordered',
                'being_delivered',
                'received',
                'refund_requested',
                'refund_granted',
                'shipping_address',
                'billing_address',
                'payment',
                'coupon'
                ]
    list_display_links = [
        'user',
        'shipping_address',
        'billing_address',
        'payment',
        'coupon'
    ]
    list_filter = ['ordered',
                   'being_delivered',
                   'received',
                   'refund_requested',
                   'refund_granted']
    search_fields = [
        'user__username',
        'ref_code'
    ]
    actions=[accept_refund]


admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(UserProfile)
