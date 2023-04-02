from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.ADListView.as_view()),
    path('search/', views.AdSearchView.as_view()),
    path('create/', views.ADCreateView.as_view()),
    path('delete/<int:pk>/', views.ADDelete.as_view()),
    path('detail/<int:pk>/', views.ADDetailView.as_view()),
    path('update/<int:pk>/', views.ADUpdateView.as_view()),

    path('image/update/<int:pk>/', views.ImageUpdateView.as_view()),
    path('image/delete/<int:pk>/', views.ImageDeleteView.as_view()),
]
