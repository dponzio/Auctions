from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listings/<int:listing_id>", views.listing_view, name="listings"),
    path("watch/<int:listing_id>", views.watchlist_add, name="watch"),
    path("watchlist", views.watchlist_view, name="watchlist"),
    path("unwatch/<int:listing_id>", views.watchlist_remove, name="unwatch"),
    path("bid/<int:listing_id>", views.bid, name="bid"),
    path("close/<int:listing_id>", views.close, name="close"),
    path("comment/<int:listing_id>", views.comment, name="comment"),
    path("categories", views.categories, name="categories"),
    path("category/<int:category_id>", views.category, name="category")
]
