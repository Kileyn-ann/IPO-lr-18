from django import forms  # базовый модуль форм Django

from .models import Category, Manufacturer, Product


class CategoryForm(forms.ModelForm):
    """Форма для добавления категории товара."""

    class Meta:
        model = Category
        fields = ["name", "description"]


class ManufacturerForm(forms.ModelForm):
    """Форма для добавления производителя."""

    class Meta:
        model = Manufacturer
        fields = ["name", "country", "description"]


class ProductForm(forms.ModelForm):
    """Форма для добавления товара."""

    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "product_photo",
            "price",
            "stock_quantity",
            "category",
            "manufacturer",
        ]

