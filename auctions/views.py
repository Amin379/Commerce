from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Max

from .models import User, Asset, Bid, Comment


def index(request):
    asset = Asset.objects.all
    return render(request, "auctions/index.html",{
        "asset": asset
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url="/login")
def create_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        bid = request.POST["bid"]
        asset = Asset.objects.create(title = title, description = description, user = request.user)
        bid = Bid.objects.create(price = bid, asset = asset, user = request.user)
        return render(request, "auctions/create_listing.html")
    return render(request, "auctions/create_listing.html")

def asset(request, id):
    exist = None
    error = ""
    if request.method == "POST":
        match request.POST['form']:
            case 'bid':
                newBid = request.POST["bid"]
                newBid = int(newBid)
                lastBid = Bid.objects.filter(asset__id = id)
                lastBid = int(lastBid.aggregate(Max('price'))['price__max'] or 0)
                if newBid > lastBid:
                    Bid.objects.create(price = newBid, user = request.user, asset=Asset.objects.get(id = id))
                else:
                    error = "Your offer is less than last one!"
            case 'close':
                asset = Asset.objects.get(id =id)
                asset.open = False
                asset.save()
            case 'comment':
                comment  = request.POST['comment']
                Comment.objects.create(text = comment, user = request.user, asset = Asset.objects.get(id = id))
    if request.user.is_authenticated:
        user = User.objects.get(username = request.user.username)
        exist = user.watchlist.contains(Asset.objects.get(id = id))
    asset = Asset.objects.get(id = id)
    return render(request, "auctions/asset.html", {
                "asset": asset, "id": id, "exist": exist, "error": error
    })

def watchlistAdd(request, id):
    user = User.objects.get(username = request.user.username)
    user.watchlist.add(Asset.objects.get(id = id))
    return HttpResponseRedirect(reverse('asset', args=[id]))

def watchlistRemove(request, id):
    user = User.objects.get(username = request.user.username)
    user.watchlist.remove(Asset.objects.get(id = id))
    return HttpResponseRedirect(reverse('asset', args=[id]))
@login_required(login_url='login')
def watchlist(request):
    user = User.objects.get(username = request.user.username)
    asset = user.watchlist.all
    return render(request, "auctions/watchlist.html", {
        "asset": asset
    })