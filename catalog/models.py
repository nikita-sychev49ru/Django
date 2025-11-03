from django.db import models


class Category(models.Model):
    """Модель для создания категорий продуктов"""

    category_name = models.CharField(max_length=150, verbose_name="Наименование")
    description = models.TextField(max_length=150, verbose_name="Описание")

    def __str__(self):
        return f"{self.category_name}"

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"
        ordering = [
            "category_name",
        ]
        db_table = "categories"


class Product(models.Model):
    """Модель для создания продуктов"""

    product_name = models.CharField(max_length=150, verbose_name="Наименование")
    description = models.TextField(null=True, verbose_name="Описание")
    image = models.ImageField(null=True, upload_to="images/", verbose_name="Изображение")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products", verbose_name="Категория")
    price = models.FloatField(verbose_name="Цена")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата последнего изменения")

    def __str__(self):
        return f"{self.product_name} - {self.price}"

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"
        ordering = [
            "product_name",
        ]
        db_table = "products"
