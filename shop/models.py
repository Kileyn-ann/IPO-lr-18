from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')

    def str(self):
        return self.name
class Manufacturer(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    country = models.CharField(max_length=100, verbose_name='Страна')
    description = models.TextField(blank=True, verbose_name='Описание')

    def str(self):
        return self.name 
class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    product_photo = models.ImageField(upload_to='products/', verbose_name='Фото товара')

    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    stock_quantity = models.IntegerField(verbose_name='Количество на складе')

    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, verbose_name='Производитель')

    def clean(self):
        if self.price < 0:
            raise ValidationError("Цена не может быть отрицательной")

        if self.stock_quantity < 0:
            raise ValidationError("Количество на складе не может быть отрицательным")

    def str(self):
        return self.name
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def total_cost(self):
        return sum(item.item_cost() for item in self.items.all())

    def str(self):
        return f"Корзина {self.user.username}"
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(verbose_name='Количество')

    def item_cost(self):
        return self.product.price * self.quantity

    def clean(self):
        if self.quantity > self.product.stock_quantity:
            raise ValidationError("Количество превышает остаток на складе")

    def str(self):
        return f"{self.product.name} ({self.quantity})"
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField(verbose_name="Адрес доставки")

    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"Заказ #{self.id} - {self.user.username}"
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def item_cost(self):
        return self.quantity * self.price

    def str(self):
        return f"{self.product.name} x {self.quantity}"
       
