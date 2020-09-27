
from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('<int:blog_id>/', views.detail, name="detail"),
    path('new/', views.new, name="new"),
    path('create', views.create, name="create"),
    path('newblog/', views.blogpost, name="blogpost"),
    path('update/<int:blog_id>', views.update, name="update"),
    path('delete/<int:blog_id>', views.BlogDelete.as_view(), name="delete"),
]
