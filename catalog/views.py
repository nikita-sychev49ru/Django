from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, TemplateView, DetailView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from .forms import ProductForm, ProductModeratorForm
from .models import Product, Category
from .services import get_products_by_category


class ProductUnpublishedView(LoginRequiredMixin, View):
    """Контроллер для отмены публикации продукта"""
    model = Product

    def post(self, request, product_id):
        product = get_object_or_404(Product, product_id)
        if not self.request.user.has_perm('catalog.can_unpublished_product'):
            return HttpResponseForbidden('У вас нет прав для отмены публикации продукта')
        product.is_published = False
        product.save()
        redirect('catalog:product_card', pk=product_id)

class ProductCreateView(LoginRequiredMixin, CreateView):
    """Контроллер для создания продукта"""
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Контроллер для редактирования продукта"""
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


@method_decorator(cache_page(60 * 15), name='dispatch')
class ProductCardDetailView(LoginRequiredMixin, DetailView):
    """Контроллер для просмотра карточки продукта"""
    model = Product
    template_name = 'product_card.html'
    context_object_name = 'product'


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Контроллер для удаления продукта"""
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


class ProductListView(ListView):
    """Контроллер для просмотра списка всех продуктов"""
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = cache.get('products_queryset')
        if not queryset:
            queryset = super().get_queryset()
            cache.set('products_queryset', queryset, 60 * 15)
        return queryset


class ProductByCategoryListView(LoginRequiredMixin, ListView):
    """Контроллер для просмотра списка продуктов одной категории"""
    model = Product
    template_name = 'category.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        products_by_category = get_products_by_category(category_id)
        return products_by_category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs['category_id']
        context['current_category'] = get_object_or_404(Category, id=category_id)
        return context


class ContactsTemplateView(TemplateView):
    """Контроллер для перехода на страницу контактов"""
    template_name = 'contacts.html'