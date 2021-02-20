from django.urls import path

from store.views import UserCreateView, ProductCreateView, Login, Logout, ProductPageView, PurchaseCreateView, \
    PurchaseReturnCreateView, UpdateProductView, PurchasePageView, ReturnPageView, PurchaseDeleteView, ReturnDeleteView

urlpatterns = [
    path('', ProductPageView.as_view(), name='base'),
    path('registration/', UserCreateView.as_view(), name='registration'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('create_product/', ProductCreateView.as_view(), name='product_create'),
    path('create_purchase/', PurchaseCreateView.as_view(), name='create_purchase'),
    path('purchase/', PurchasePageView.as_view(), name='purchase'),
    path('purchase_return/', PurchaseReturnCreateView.as_view(), name='purchase_return'),
    path('returns/', ReturnPageView.as_view(), name='returns'),
    path('delete_purchase/<int:pk>', PurchaseDeleteView.as_view(), name='delete_purchase'),
    path('delete_return/<int:pk>', ReturnDeleteView.as_view(), name='delete_return'),
    path('update_product/<int:pk>', UpdateProductView.as_view(), name='update_product'),

]
