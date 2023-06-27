from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name= 'home'),
    path('about', views.about, name = 'about'),
    path('create', views.create, name='create'),
    path('preview/<int:dataset_id>/', views.preview_dataset, name='preview'),
    path('download_dataset/<int:dataset_id>/', views.download_dataset_view, name='download_dataset'),
    path('preview/<int:dataset_id>/regenerate/', views.regenerate_dataset, name='regenerate'),
    path('help/', views.help, name='help'),
    ]
