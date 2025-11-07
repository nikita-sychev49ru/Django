from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, TemplateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import ProductForm
from .models import Product


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

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

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)