from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('feed/', views.feed, name='feed'),
    path('ticket/<int:ticket_id>/delete/', views.delete_ticket, name='delete_ticket'),
    path('review/<int:review_id>/delete/', views.delete_review, name='delete_review'),
    path('review/<int:review_id>/edit/', views.edit_review, name='edit_review'),
    path('ticket/<int:ticket_id>/edit/', views.edit_ticket, name='edit_ticket'),
    path("review/create/", views.create_review_with_ticket, name="create_review_with_ticket"),
    path('ticket/create/', views.create_ticket, name='create_ticket'),
    path('review/create/<int:ticket_id>/', views.create_review, name='create_review'),
    path('follows/', views.follows_view, name='follows'),
    path('unfollow/<int:follow_id>/', views.unfollow_view, name='unfollow'),
    path('block/<int:user_id>/', views.block_user, name='block_user'),
    path('unblock/<int:user_id>/', views.unblock_user, name='unblock_user'),
    path("posts/", views.posts, name="posts"),
]
