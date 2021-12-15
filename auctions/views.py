from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import *

# Form classes
class BidForm(forms.Form):
    bid = forms.DecimalField(max_value=9999999999, label="Bid on this item")

# View functions
def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html",{
        "title": "Active Listings",
        "listings": listings
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

@login_required
def create(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        else:
            user = request.user

        title = request.POST["title"]
        description = request.POST["description"]
        price = request.POST["price"]
        image = request.POST["image"]
        category = request.POST["category"]
        category = Category.objects.get(pk=category)
        if not image:
            Listing.objects.create(title=title, description=description, price=price, creator=user, category=category)
        else:
            Listing.objects.create(title=title, description=description, price=price, creator=user, image=image, category=category)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create.html")

def listing_view(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    is_watching = False
    comments = listing.comments.all()
    print(comments)
    if request.user.is_authenticated:
        if Watchlist.objects.filter(watcher=request.user, item=listing_id).exists():
            is_watching = True
    return render(request, "auctions/listing.html", {
      "listing": listing,
      "watching": is_watching,
      "bidForm": BidForm(),
      "comments": comments
    })

@login_required
def watchlist_add(request, listing_id):
    user = User.objects.get(id=request.user.id)
    watched_listing = Listing.objects.get(id=listing_id)

    if Watchlist.objects.filter(watcher=user, item=watched_listing).exists():
        return render(request, "auctions/listing.html", {
          "message": "This listing is already in your watchlist",
          "listing": watched_listing
        })
    else:
        Watchlist.objects.create( watcher=user, item=watched_listing)
        return HttpResponseRedirect(reverse('listings', kwargs={'listing_id': listing_id}))

@login_required
def watchlist_remove(request, listing_id):
    user = User.objects.get(id=request.user.id)
    unwatch_listing = Listing.objects.get(id=listing_id)

    if Watchlist.objects.filter(watcher=user, item=unwatch_listing).exists():
        delete_me = Watchlist.objects.get(watcher=user, item=unwatch_listing)
        delete_me.delete()
        return HttpResponseRedirect(reverse('listings', kwargs={'listing_id': listing_id}))

@login_required
def watchlist_view(request):
    user = User.objects.get(id=request.user.id)
    watches = Watchlist.objects.filter(watcher=user).values_list('item_id', flat=True)
    watchlist = Listing.objects.filter(id__in=watches)
    return render(request, "auctions/watchlist.html",{
        "listings": watchlist
    })

@login_required
def bid(request, listing_id):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        else:
            bid = float(request.POST["bid"])
            user = User.objects.get(id=request.user.id)
            listing = Listing.objects.get(id=listing_id)

            if bid <= float(listing.price):
                return render(request, "auctions/listing.html", {
                  "message": f"The bid must be higher than the current price: ${listing.price}",
                  "listing": listing,
                  "bidForm": BidForm()
                })
            else:
                Listing.objects.filter(pk=listing_id).update(price=bid)
                Bid.objects.create(bidder=user, bid=bid, listing=listing)
                listing = Listing.objects.get(id=listing_id)
                return render(request, "auctions/listing.html", {
                  "message": "Your bid has been accepted",
                  "listing": listing,
                  "bidForm": BidForm()
                })

@login_required
def close(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    if request.method == "POST":
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        elif request.user == listing.creator:
            winner = Bid.objects.filter(listing=listing_id, bid=listing.price).values('bidder')
            Listing.objects.filter(pk=listing_id).update(winner=winner)
            return HttpResponseRedirect(reverse('listings', kwargs={'listing_id': listing_id}))

def comment(request, listing_id):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('listings', kwargs={'listing_id': listing_id}))
        else:
            user = request.user
            comment = request.POST.get('comment_text')
            listing = Listing.objects.get(id=listing_id)
            print(comment)
            Comment.objects.create(author=user, body=comment, listing=listing)
            return HttpResponseRedirect(reverse('listings', kwargs={'listing_id': listing_id}))

def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def category(request, category_id):
    category = Category.objects.get(pk=category_id)
    listings = Listing.objects.filter(category_id=category_id)
    return render(request, "auctions/index.html", {
        "title": category.name,
        "listings": listings
    })