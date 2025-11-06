from django.urls import path
from blog.apps import BlogConfig
from blog import views

app_name = BlogConfig.name

urlpatterns = [
    path('publication/create/', views.PublicationCreateView.as_view(), name='publication_create'),
    path('publication/<int:pk>/', views.PublicationDetailView.as_view(), name='publication_detail'),
    path('', views.PublicationListView.as_view(), name='publication_list'),
    path('publication/edit/<int:pk>/', views.PublicationUpdateView.as_view(), name='publication_edit'),
    path('publication/delete/<int:pk>/', views.PublicationDeleteView.as_view(), name='publication_delete'),
]