from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createListing",views.create_listing, name="create_listing"),
    path("asset/<int:id>", views.asset, name="asset"),
    path("watchlistAdd/<int:id>", views.watchlistAdd, name="watchlistAdd"),
    path("watchlistRemove/<int:id>", views.watchlistRemove, name="watchlistRemove"),
    path("watchlist", views.watchlist, name="watchlist")

]

