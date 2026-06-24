from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.conf import settings
from django.core.paginator import Paginator
from django.core.mail import EmailMessage

from rest_framework import generics

import openpyxl

from .models import Product, Category, Manufacturer, CartItem, Cart
from .serializers import *
from .forms import CategoryForm, ManufacturerForm, ProductForm


# 🔹 Главная страница
def home(request):
    products = Product.objects.all().order_by('-id')
    return render(request, "shop/home.html", {'products': products})


# 🔹 Index
def index(request):
    products = Product.objects.all().order_by('-id')[:6]
    categories = Category.objects.all()
    return render(request, 'shop/index.html', {
        'products': products,
        'categories': categories
    })


# 🔹 Каталог с пагинацией
def catalog(request):
    all_products = Product.objects.all().order_by("id")
    paginator = Paginator(all_products, 6)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    return render(request, "shop/catalog.html", {"page_obj": page_obj})


# 🔹 Список товаров с фильтрами
def product_list(request):
    products = Product.objects.all()

    category_id = request.GET.get('category')
    manufacturer_id = request.GET.get('manufacturer')
    search = request.GET.get('search')

    if category_id:
        products = products.filter(category_id=category_id)
    if manufacturer_id:
        products = products.filter(manufacturer_id=manufacturer_id)
    if search:
        products = products.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search)
        )

    categories = Category.objects.all()
    manufacturers = Manufacturer.objects.all()

    return render(request, 'shop/catalog.html', {
        'products': products,
        'categories': categories,
        'manufacturers': manufacturers
    })


# 🔹 Детальная страница товара
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})


# 🔹 О себе / о магазине
def about_author(request):
    return render(request, "shop/about_author.html")


def about_shop(request):
    return render(request, "shop/about_shop.html")


# 🔹 Добавление категории
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Категория успешно добавлена.")
            return redirect("home")
    else:
        form = CategoryForm()
    return render(request, "shop/add_category.html", {"form": form})


# 🔹 Добавление производителя
def add_manufacturer(request):
    if request.method == "POST":
        form = ManufacturerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Производитель успешно добавлен.")
            return redirect("home")
    else:
        form = ManufacturerForm()
    return render(request, "shop/add_manufacturer.html", {"form": form})


# 🔹 Добавление товара
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Товар успешно добавлен.")
            return redirect("home")
    else:
        form = ProductForm()
    return render(request, "shop/add_product.html", {"form": form})


# 🔹 Получение корзины пользователя
def get_user_cart(user):
    cart, created = Cart.objects.get_or_create(user=user)
    return cart


# 🔹 Просмотр корзины
@login_required
def cart_view(request):
    cart = get_user_cart(request.user)
    items = cart.items.all()
    total = sum(item.product.price * item.quantity for item in items)
    return render(request, 'shop/cart.html', {
        'cart': cart,
        'items': items,
        'total': total
    })


# 🔹 Добавить в корзину
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_user_cart(request.user)

    item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        item.quantity += 1

    if item.quantity > product.quantity_in_stock:
        messages.error(request, "Недостаточно товара на складе")
        return redirect('catalog')

    item.save()
    return redirect('cart')


# 🔹 Обновить количество в корзине
@login_required
def update_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    quantity = int(request.POST.get('quantity', 1))

    if quantity > item.product.quantity_in_stock:
        messages.error(request, "Превышено количество на складе")
    else:
        item.quantity = quantity
        item.save()

    return redirect('cart')


# 🔹 Удалить из корзины
@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect('cart')


# 🔹 Оформление заказа
@login_required
def checkout(request):
    cart = get_user_cart(request.user)
    items = cart.items.all()

    if request.method == 'POST':
        address = request.POST.get('address')

        # 📊 Создание Excel-чека
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Чек"
        ws.append(["Товар", "Количество", "Цена"])

        total = 0
        for item in items:
            ws.append([item.product.name, item.quantity, float(item.product.price)])
            total += item.product.price * item.quantity

        ws.append(["", "", ""])
        ws.append(["ИТОГО", "", float(total)])

        file_path = "receipt.xlsx"
        wb.save(file_path)

        # 📧 Отправка email
        email = EmailMessage(
            subject="Ваш заказ",
            body=f"Спасибо за заказ!\nАдрес: {address}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[request.user.email],
        )
        email.attach_file(file_path)
        email.send()

        # 🧹 Очистка корзины
        items.delete()

        messages.success(request, "Заказ оформлен!")
        return redirect('catalog')

    total = sum(item.product.price * item.quantity for item in items)
    return render(request, 'shop/checkout.html', {
        'items': items,
        'total': total
    })


# --- API ---

class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductCreateAPIView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductUpdateAPIView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDeleteAPIView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

