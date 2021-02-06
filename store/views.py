from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, ListView, DetailView, UpdateView

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


class ProductCreateView(CreateView):
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
        object.save()
        return super().form_valid(form=form)


class PurchaseReturnCreateView(CreateView):
    model = PurchaseReturns
    form_class = PurchaseReturnForm
    success_url = '/'
    template_name = 'purchase_return.html'


class Login(LoginView):
    template_name = 'login.html'
    success_url = '/'


class Logout(LogoutView):
    next_page = '/'


class ProductPageView(ListView):
    model = Product
    template_name = 'base.html'
    extra_context = {'purchase_form': PurchaseForm, 'product_form': ProductForm}


class PurchasePageView(ListView):
    model = Purchase
    template_name = 'create_purchase.html'


class UpdateProductView(UpdateView):
    success_url = '/'
    model = Product
    fields = '__all__'
    template_name = 'update_product.html'

