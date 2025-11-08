from django.db import models

from users.models import CustomUser


class Category(models.Model):
    """Модель для создания категорий продуктов"""
    category_name = models.CharField(max_length=150, verbose_name='Наименование')
    description = models.TextField(max_length=150, verbose_name='Описание')

    def __str__(self):
        return f'{self.category_name}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ['category_name',]
        db_table = 'categories'


class Product(models.Model):
    """Модель для создания продуктов"""
    product_name = models.CharField(max_length=150, verbose_name='Наименование', blank=True)
    description = models.TextField(default='', verbose_name='Описание', blank=True)
    image = models.ImageField(null=True, upload_to='images/', default='images/placeholder.png', verbose_name='Изображение', blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Категория', blank=True)
    owner = models.ForeignKey(
                                CustomUser,
                                on_delete=models.CASCADE,
                                related_name='products',
                                verbose_name='Владелец',
                                blank=True,
                                null=True
                                )
    price = models.FloatField(verbose_name='Цена', blank=True)
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')

    def __str__(self):
        return f'{self.product_name} - {self.price}'

    def save(self, *args, **kwargs):
        if not self.owner:  # Если владелец не указан
            self.owner = CustomUser.objects.get(username='ADMIN')
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ['product_name',]
        db_table = 'products'
        permissions = [
            ('can_unpublish_product', 'Can unpublish product'),
        ]