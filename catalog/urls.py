from django.urls import path
from  catalog.apps import CatalogConfig
from catalog import views

app_name = CatalogConfig.name

urlpatterns = [
    path('', views.ProductListView.as_view(), name='home'),
    path('category/<int:category_id>', views.ProductByCategoryListView.as_view(), name='products_by_category'),
    path('contacts/', views.ContactsTemplateView.as_view(), name='contacts'),
    path('product/<int:pk>/', views.ProductCardDetailView.as_view(), name='product_card'),
    path('product/create/', views.ProductCreateView.as_view(), name='product_form'),
    path('product/update/<int:pk>/', views.ProductUpdateView.as_view(), name='product_form'),
    path('product/delete/<int:pk>/', views.ProductDeleteView.as_view(), name='product_delete'),
]