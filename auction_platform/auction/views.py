from django.shortcuts import render, redirect
from .models import Auction, Bid, Review, AdminApproval, Item
from django.contrib.auth.decorators import login_required
from .forms import UserSignupForm
from django.contrib.auth import login


def auction_list(request):
    auctions = Auction.objects.all()
    return render(request, 'auction/auction_list.html', {'auctions': auctions})


@login_required
def place_bid(request, auction_id):
    auction = Auction.objects.get(pk=auction_id)
    if request.method == 'POST':
        bid_amount = request.POST['bid_amount']
        if float(bid_amount) > auction.current_bid:
            Bid.objects.create(auction=auction, bidder=request.user, bid_amount=bid_amount)
            auction.current_bid = bid_amount
            auction.save()
            return redirect('auction_detail', auction_id=auction_id)
    return render(request, 'auction/place_bid.html', {'auction': auction})


def auction_detail(request, auction_id):
    auction = Auction.objects.get(pk=auction_id)
    return render(request, 'auction/auction_detail.html', {'auction': auction})


@login_required
def approve_item(request, item_id):
    if request.user.is_staff:
        item = Item.objects.get(pk=item_id)
        AdminApproval.objects.create(admin=request.user, item=item, is_approved=True)
        return redirect('admin_dashboard')
    return redirect('home')


def user_signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.save()  # Save the updated user with first and last name
            login(request, user)
            return redirect('user_dashboard')  # Redirect to dashboard after signup
    else:
        form = UserSignupForm()
    return render(request, 'auction/signup.html', {'form': form})


def user_dashboard(request):
    user_bids = Bid.objects.filter(bidder=request.user)
    return render(request, 'auction/user_dashboard.html', {'user_bids': user_bids})


def about(request):
    return render(request, 'auction/about.html')


def contact_us(request):
    return render(request, 'auction/contact_us.html')


def home(request):
    return render(request, 'auction/home.html')