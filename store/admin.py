from django.contrib import admin

from store.models import CustomUser, Product, Purchase, PurchaseReturns

admin.site.register(CustomUser)
admin.site.register(Product)
admin.site.register(Purchase)
admin.site.register(PurchaseReturns)
