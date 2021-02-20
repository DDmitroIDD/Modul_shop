from datetime import timedelta

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from store.forms import UserForm, ProductForm, PurchaseForm, PurchaseReturnForm
from store.models import CustomUser, Product, Purchase, PurchaseReturns


class UserCreateView(CreateView):
    model = CustomUser
    form_class = UserForm
    success_url = '/login/'
    template_name = 'registration.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.set_password(self.object.password)
        self.object.save()
        return super().form_valid(form)


class ProductCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'is_superuser'
    model = Product
    form_class = ProductForm
    success_url = '/create_product/'
    template_name = 'create_product.html'


class PurchaseCreateView(CreateView):
    model = Purchase
    form_class = PurchaseForm
    template_name = 'create_purchase.html'
    success_url = '/'

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        product = Product.objects.get(id=self.request.POST['product_id'])
        amount_of_money = product.price * object.quantity_of_products
        if amount_of_money > object.user.wallet:
            messages.error(self.request, 'You don\'t have enough funds!')
            return redirect('/')
        elif product.quantity_in_stock < object.quantity_of_products:
            messages.error(self.request, 'Not enough product in stock!')
            return redirect('/')
        product.quantity_in_stock -= object.quantity_of_products
        user = self.request.user
        user.wallet -= amount_of_money
        object.product_id = self.request.POST['product_id']
        user.save()
        object.save()
        product.save()
        return super().form_valid(form=form)


class PurchaseReturnCreateView(CreateView):
    model = PurchaseReturns
    form_class = PurchaseReturnForm
    success_url = '/purchase'
    template_name = 'purchase_return.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        purchase = Purchase.objects.get(id=self.request.POST['purchase_id'])
        returns = PurchaseReturns.objects.filter(purchase=purchase)
        if purchase.time_of_buy + timedelta(minutes=3) < timezone.now():
            messages.error(self.request, 'SORRY, can be returned only 3 minutes after purchase!')
            return redirect('purchase')
        elif returns:
            messages.info(self.request, 'Your return request is already being processed!')
            return redirect('purchase')
        messages.info(self.request, 'Your request in work!')
        self.object.purchase = purchase
        self.object.save()
        return super().form_valid(form=form)


class Login(LoginView):
    template_name = 'login.html'
    success_url = '/'


class Logout(LogoutView):
    next_page = '/'


class ProductPageView(ListView):
    model = Product
    template_name = 'base.html'
    extra_context = {'purchase_form': PurchaseForm, }


class PurchasePageView(ListView):
    model = Purchase
    template_name = 'create_purchase.html'
    extra_context = {'return_form': PurchaseReturnForm, }

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class ReturnPageView(PermissionRequiredMixin, ListView):
    permission_required = 'is_superuser'
    model = PurchaseReturns
    template_name = 'purchase_return.html'


class UpdateProductView(PermissionRequiredMixin, UpdateView):
    permission_required = 'is_superuser'
    success_url = '/'
    model = Product
    fields = '__all__'
    template_name = 'update_product.html'


class PurchaseDeleteView(DeleteView):
    model = Purchase
    template_name = 'delete_purchase.html'
    success_url = '/'

    def post(self, request, *args, **kwargs):
        product_pk = self.request.POST['product_pk']
        product_price = self.request.POST['product_price']
        purchase_quantity = self.request.POST['purchase_quantity']
        purchase_user = self.request.POST['purchase_user']
        product = Product.objects.get(id=product_pk)
        user = CustomUser.objects.get(id=purchase_user)
        product.quantity_in_stock += int(purchase_quantity)
        user.wallet += int(product_price) * int(purchase_quantity)
        user.save()
        product.save()
        return super().post(request, *args, **kwargs)


class ReturnDeleteView(DeleteView):
    model = PurchaseReturns
    template_name = 'delete_return.html'
    success_url = '/'

