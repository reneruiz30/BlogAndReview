from django.urls import path
from . import views

app_name = 'blogapp'

urlpatterns = [
    path('', views.BlogListView.as_view(), name='blog_list'),
    path('blog/add/', views.BlogCreateView.as_view(), name='add_blog'),
    path('blog/<int:pk>/', views.BlogDetailView.as_view(), name='blog_detail'),
    path('blog/<int:pk>/review/', views.ReviewCreateView.as_view(), name='add_review'),
    path('register/', views.register, name='register'), # Nueva URL para el registro
    path('blog/<int:blog_pk>/review/<int:review_pk>/comment/add/', views.add_comment, name='add_comment'),
]