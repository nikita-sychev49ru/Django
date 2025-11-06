from dataclasses import fields

from django import forms
from django.core.exceptions import ValidationError
from django.db.models import BooleanField

from config.constants import SPAM_WORDS
from .models import Product


class ProductForm(forms.ModelForm):
    """Форма для создания нового продукта"""
    class Meta:
        model = Product
        fields = ['product_name', 'description', 'image', 'category', 'price', 'is_active']
        exclude = ['created_at', 'updated_at']


    def __init__(self, *args, **kwargs):
        super(ProductForm,self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['product_name'].widget.attrs.update({'placeholder': 'Название продукта',})
        self.fields['description'].widget.attrs.update({'placeholder': 'Добавьте описание продукта'})
        self.fields['price'].widget.attrs.update({'placeholder': 'Укажите цену в формате 00,00',})
        self.fields['is_active'].widget.attrs.update({'class': 'form-check-input'},)

    def clean_price(self):
        """метод валидации цены: цена должна быть больше нуля"""
        price = self.cleaned_data.get('price')
        if not price > 0:
            raise ValidationError('Цена не может быть меньше нуля!')
        return price

    def clean(self):
        """метод валидации данных полей - название продукта и описание:
        поля не должны содержать запрещенных слов"""
        cleaned_data = super().clean()
        product_name = self.cleaned_data.get('product_name')
        description = self.cleaned_data.get('description')
        if not product_name:
            raise ValidationError('Название продукта не может быть пустым!')
        for item in SPAM_WORDS:
            if item.lower() in product_name.lower():
                self.add_error('product_name','Название продукта не может содержать запрещенные слова!')
            elif item.lower() in description.lower():
                self.add_error('description', 'Описание продукта не может содержать запрещенные слова!')