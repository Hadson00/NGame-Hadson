from django.urls import path
from myapp.views import *

urlpatterns = [
    path("", index, name="index"),
    path("home/", home, name="home"),
    path('like/<int:game_id>/', like_game, name='like_game'),
    path("comment/<int:game_id>/", comment_game, name="comment_game"),
    path("create/", create, name="create_game"),
    path("edit/<int:game_id>", edit, name="edit_game"),
    path("delete/<int:game_id>", delete_game, name="delete_game"),
    path('cart/', view_cart, name='view_cart'),
    path('add_to_cart/<int:game_id>', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:game_id>', remove_from_cart, name='remove_from_cart'),
    path('update_cart/<int:game_id>', update_cart, name='update_cart'),
    path('checkout/', checkout, name='checkout'),
]