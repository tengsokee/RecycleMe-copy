"""socialMedia urls.py

This script defines the mapping of urls to views for socialMedia page
Author: Desmond, Akshita and Sok Ee 
"""

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import include,path
from .views import PostListView, PostDetailView, PostEditView, PostDeleteView, CommentDeleteView, ProfileView, \
    ProfileEditView, AddLike, AddDislike, BookmarkPost, BookmarkListView

#appName
app_name = 'community'
urlpatterns = [
    #examplepath('whatwedo/',views.pdts_services,name='What we do'),
    #urls for community
    path('', PostListView.as_view(), name='home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/edit/<int:pk>/', PostEditView.as_view(), name='post-edit'),
    path('post/delete/<int:pk>/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:post_pk>/comment/delete/<int:pk>/', CommentDeleteView.as_view(), name='comment-delete'),
    path('profile/<slug>/', ProfileView.as_view(), name='profile'),
    path('profile/edit/<int:pk>/', ProfileEditView.as_view(), name='profile-edit'),
    path('post/<int:pk>/like', AddLike.as_view(), name='like'),
    path('post/<int:pk>/dislike', AddDislike.as_view(), name='dislike'),
    path('post/<int:pk>/bookmark_post', BookmarkPost.as_view(), name='bookmark_post'),
    path('profile/bookmark_list', BookmarkListView.as_view(), name='bookmark_list'),
    #urls for authentication
    path('register/', views.register, name='register'),
    path('registeradmin/', views.registerAdmin, name='registerAdmin'),
    path('login/', views.loginPage, name='loginPage'),
    path('logout/', auth_views.LogoutView.as_view(template_name='socialMedia/logout.html'), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='socialMedia/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetView.as_view(template_name='socialMedia/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='socialMedia/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='socialMedia/password_reset_complete.html'),
         name='password_reset_complete'),
]