from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('cart/', cart_view, name='cart'),
    path('catalog/', catalog, name='catalog'),
    path('logout/', LogoutView.as_view(next_page='/admin/login/'), name='logout'),
    path('', home, name='home'),
    path('about_author/', about_author, name='about_author'),
    path('about_shop/', about_shop, name='about_shop'),
    path('add_category/', add_category, name='add_category'),
    path('add_manufacturer/', add_manufacturer, name='add_manufacturer'),
    path('add_product/', add_product, name='add_product'),


    path('api/categories/', CategoryListAPIView.as_view()),
    path('api/products/', ProductListAPIView.as_view()),
    path('api/products/<int:pk>/', ProductDetailAPIView.as_view()),
    path('api/products/create/', ProductCreateAPIView.as_view()),
    path('api/products/<int:pk>/update/', ProductUpdateAPIView.as_view()),
    path('api/products/<int:pk>/delete/', ProductDeleteAPIView.as_view()),
]
