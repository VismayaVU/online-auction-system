from django.shortcuts import render, redirect, get_object_or_404
from .models import Auction, Bid, Review, AdminApproval, Item, AuctionTag
from django.contrib.auth.decorators import login_required
from .forms import UserSignupForm, AuctionItemForm, AuctionForm
from django.contrib.auth import login
from django.utils import timezone
from datetime import timedelta
from django.contrib.admin.views.decorators import staff_member_required


def auction_list(request):
    approved_auctions = Auction.objects.filter(status="Approved")
    return render(request, 'auction/auction_list.html', {'auctions': approved_auctions})


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


@staff_member_required
def approve_auction(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    auction = get_object_or_404(Auction, item=item)

    # Ensure this auction has not already been approved
    approval, created = AdminApproval.objects.get_or_create(item=item)
    if not approval.is_approved:
        approval.is_approved = True
        approval.admin = request.user  # assumes the admin is logged in
        approval.save()

        # Update the auction status to Approved
        auction.status = "Approved"
        auction.save()

    return redirect('pending_auctions')  # Redirect to pending auctions list or admin page


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


@login_required
def create_auction(request):
    if request.method == 'POST':
        item_form = AuctionItemForm(request.POST)
        auction_form = AuctionForm(request.POST)

        if item_form.is_valid() and auction_form.is_valid():
            # Retrieve the starting price from the form
            starting_price = item_form.cleaned_data['starting_price']

            # Save item details
            auction_item = item_form.save(commit=False)
            auction_item.price = starting_price  # Set the price as the starting price
            auction_item.save()

            # Save auction details and link to the item
            auction = auction_form.save(commit=False)
            auction.item = auction_item
            auction.seller = request.user
            auction.starting_bid = starting_price  # Set starting_bid
            auction.current_bid = starting_price - 1
            auction.status = "Pending"
            auction.start_time = auction_form.cleaned_data.get('start_date', timezone.now())
            auction.end_time = auction_form.cleaned_data.get('end_date', auction.start_time + timedelta(days=7))
            auction.save()

            # Save selected tags
            selected_tags = auction_form.cleaned_data['tags']
            for tag in selected_tags:
                AuctionTag.objects.create(
                    auction_id=auction.auction_id,
                    tag_id=tag.tag_id,
                    assigned_on=timezone.now()
                )

            return redirect('auction_list')
    else:
        item_form = AuctionItemForm()
        auction_form = AuctionForm()

    return render(request, 'auction/create_auction.html', {
        'item_form': item_form,
        'auction_form': auction_form,
    })


@staff_member_required
def pending_auctions_admin_view(request):
    pending_auctions = Auction.objects.filter(status="Pending")
    return render(request, "admin/pending_auctions_admin.html", {"pending_auctions": pending_auctions})