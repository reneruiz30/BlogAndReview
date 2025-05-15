from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import SportsSubsectionDetailView

app_name = 'blogapp'

urlpatterns = [
    path('blog/<int:blog_id>/subsection/create/', views.create_subsection, name='create_subsection'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),
    path('comment/<int:pk>/delete/', views.delete_comment, name='delete_comment'),
    path('post/<int:pk>/edit/', views.edit_post, name='edit_post'),
    
   path('subsection/<str:subsection_type>/<int:subsection_id>/post/add/', views.add_post_to_subsection, name='add_post_to_subsection'),
    
    path('blogs/subsection/<int:pk>/', views.subsection_detail, name='subsection_detail'), # Function-based view
    path('post/<int:pk>/like/', views.like_post, name='like_post'),
    path('post/<int:pk>/dislike/', views.dislike_post, name='dislike_post'),
    path('post/<int:pk>/comment/', views.comment_post, name='comment_post'),
    path('subsection/<int:pk>/edit/', views.SubsectionUpdateView.as_view(), name='edit_subsection'),
    path('subsection/<int:pk>/delete/', views.SubsectionDeleteView.as_view(), name='delete_subsection'),
    path('', views.bienvenida, name='bienvenida'),
    path('blogs/', views.BlogListView.as_view(), name='blog_list'),
    path('blog/add/', views.BlogCreateView.as_view(), name='add_blog'),
    path('blog/<int:pk>/', views.BlogDetailView.as_view(), name='blog_detail'),
    path('blog/<int:pk>/review/', views.ReviewCreateView.as_view(), name='add_review'),
    path('register/', views.register, name='register'), # Nueva URL para el registro
    path('blog/<int:blog_pk>/review/<int:review_pk>/comment/add/', views.add_comment, name='add_comment'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('create/', views.BlogCreateView.as_view(), name='blog_create'),
    path('login/', views.login_view, name='login'),   # <-- Add this line
    # path('subsection/<int:pk>/', SportsSubsectionDetailView.as_view(), name='subsection_detail'), # Comment out or remove this line
    path('rate_subsection/<int:subsection_id>/<int:rating>/', views.rate_subsection, name='rate_subsection'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('change-avatar/', views.change_avatar, name='change_avatar'),
    path('change-username/', views.change_username, name='change_username'),
    path('change-email/', views.change_email, name='change_email'),
    path('change-password/', views.change_password, name='change_password'),
    path('change-password/', views.change_password, name='change_password'),

]

