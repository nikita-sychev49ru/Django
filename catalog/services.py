from catalog.models import Product


def get_products_by_category(category_id):
    """сервисная функция, формирующая список продуктов выбранной категории"""
    products_by_category = Product.objects.filter(category_id=category_id, is_published=True).select_related('category')
    return products_by_category