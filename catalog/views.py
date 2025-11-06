from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, TemplateView, DetailView, DeleteView

from .forms import ProductForm
from .models import Product


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    success_url = reverse_lazy('catalog:home')

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    success_url = reverse_lazy('catalog:home')

class ProductListView(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'

class ContactsTemplateView(TemplateView):
    template_name = 'contacts.html'


class ProductCardDetailView(DetailView):
    model = Product
    template_name = 'product_card.html'
    context_object_name = 'product'

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')