from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, TemplateView, DetailView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden

from .forms import ProductForm, ProductModeratorForm
from .models import Product

class ProductUnpublishedView(LoginRequiredMixin, View):
    model = Product

    def post(self, request, product_id):
        product = get_object_or_404(Product, product_id)
        if not self.request.user.has_perm('catalog.can_unpublished_product'):
            return HttpResponseForbidden('У вас нет прав для отмены публикации продукта')
        product.is_published = False
        product.save()
        redirect('catalog:product_card', pk=product_id)

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'product_form.html'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return ProductForm
        if user.has_perm('catalog.can_unpublish_product'):
            return ProductModeratorForm
        else:
            raise PermissionDenied("У вас нет прав для редактирования этого продукта")

class ProductListView(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'

class ContactsTemplateView(TemplateView):
    template_name = 'contacts.html'


class ProductCardDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'product_card.html'
    context_object_name = 'product'


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')

    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=kwargs.get('pk'))
        user = self.request.user
        if user != product.owner:
            if not request.user.has_perm('catalog.delete_product'):
                return HttpResponseForbidden("У вас нет прав для удаления продукта")
        product.delete()
        return redirect('catalog:home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)