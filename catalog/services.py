from django.core.cache import cache
from catalog.models import Product


def get_products_by_category(category_id):
    """сервисная функция, формирующая список продуктов выбранной категории"""
    products_by_category = Product.objects.filter(category_id=category_id, is_published=True).select_related('category')
    return products_by_category


def get_cached_products():
    """сервисная функция, возвращающая закешированный список всех продуктов"""
    cached_products = cache.get('products_queryset')
    if not cached_products:
        cached_products = Product.objects.all()
        cache.set('products_queryset', cached_products, 60 * 15)  # Кешируем на 15 минут
    return cached_products