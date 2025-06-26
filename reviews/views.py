from itertools import chain

from django.db.models import CharField, Value
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from .forms import (
    SignupForm,
    ReviewForm,
    TicketForm,
    FollowUserForm,
    CustomLoginForm
)
from .models import Ticket, Review, UserFollows


# Page d'accueil avec formulaire de connexion intégré
def home(request):
    login_error = None
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('feed')
        login_error = "Nom d'utilisateur ou mot de passe invalide."
    else:
        form = CustomLoginForm()

    return render(
        request,
        'reviews/home.html',
        {'login_form': form, 'login_error': login_error},
    )


# Page d'inscription
def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("feed")
    else:
        form = SignupForm()

    return render(request, "reviews/signup.html", {"form": form})


# Page du flux (feed)
@login_required
def feed(request):
    tickets = get_users_viewable_tickets(request.user).annotate(
        content_type=Value('TICKET', CharField()),
    )
    reviews = get_users_viewable_reviews(request.user).annotate(
        content_type=Value('REVIEW', CharField()),
    )

    for ticket in tickets:
        ticket.has_review = ticket.review_set.exists()

    posts = sorted(
        chain(tickets, reviews),
        key=lambda post: post.time_created,
        reverse=True,
    )

    return render(
        request,
        'reviews/feed.html',
        {'posts': posts},
    )


# Créer un nouveau ticket
@login_required
def create_ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect("feed")
    else:
        form = TicketForm()

    return render(request, "reviews/create_ticket.html", {
        "form": form,
        "is_edit": False
    })


# Créer une nouvelle critique pour un ticket spécifique
@login_required
def create_review(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect("feed")
    else:
        form = ReviewForm()

    return render(request, "reviews/create_review.html", {
        "form": form,
        "ticket": ticket,
        "is_edit": False
    })


# Créer une critique avec un ticket
@login_required
def create_review_with_ticket(request):
    if request.method == "POST":
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)

        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()

            return redirect("feed")
    else:
        ticket_form = TicketForm()
        review_form = ReviewForm()

    return render(request, "reviews/create_review_with_ticket.html", {
        "ticket_form": ticket_form,
        "review_form": review_form
    })


User = get_user_model()


def get_users_viewable_tickets(user):
    # Récupère les utilisateurs suivis par l'utilisateur connecté (non bloqués)
    followed_users = UserFollows.objects.filter(
        user=user,
        is_blocked=False
    ).values_list('followed_user', flat=True)

    # Récupère les tickets de l'utilisateur + ceux des suivis
    tickets = Ticket.objects.filter(user__in=list(followed_users) + [user])
    return tickets


# Affiche les critiques que l'utilisateur peut voir
def get_users_viewable_reviews(user):
    # Utilisateurs suivis (non bloqués)
    followed_users = UserFollows.objects.filter(
        user=user,
        is_blocked=False
    ).values_list('followed_user', flat=True)

    # Critiques faites par l'utilisateur ou par les suivis
    reviews_from_network = Review.objects.filter(
        user__in=list(followed_users) + [user]
    )

    # Critiques faites sur les tickets de l'utilisateur (par n'importe qui)
    reviews_on_my_tickets = Review.objects.filter(ticket__user=user)

    reviews = reviews_from_network | reviews_on_my_tickets
    reviews = reviews.distinct()
    return reviews


# Suppression d'un ticket
@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(
        Ticket,
        id=ticket_id,
        user=request.user,
    )

    if request.method == 'POST':
        ticket.delete()
        return redirect('posts')

    return render(
        request,
        'reviews/delete_ticket.html',
        {'ticket': ticket},
    )


# Suppression d'une critique
@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)

    if request.method == "POST":
        review.delete()
        return redirect("posts")

    return render(request, "reviews/delete_review.html", {"review": review})


# Édition d'une critique
@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect("feed")
    else:
        form = ReviewForm(instance=review)

    return render(request, "reviews/create_review.html", {
        "form": form,
        "ticket": review.ticket,
        "is_edit": True
    })


# Edition d'un ticket
@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)

    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect("feed")
    else:
        form = TicketForm(instance=ticket)

    return render(request, "reviews/create_ticket.html", {
        "form": form,
        "is_edit": True
    })


# Page des abonnements et abonnés
@login_required
def follows_view(request):
    form = FollowUserForm(current_user=request.user)
    follows = request.user.following.filter(is_blocked=False)
    followers = UserFollows.objects.filter(
        followed_user=request.user,
        is_blocked=False
    )
    blocked_users = UserFollows.objects.filter(
        followed_user=request.user,
        is_blocked=True
    )
    # Affiche les utilisateurs que l'utilisateur suit
    if request.method == 'POST':
        form = FollowUserForm(request.POST, current_user=request.user)
        if form.is_valid():
            user_to_follow = User.objects.get(
                username=form.cleaned_data['username']
            )
            UserFollows.objects.create(
                user=request.user,
                followed_user=user_to_follow
            )
            return redirect('follows')

    return render(request, 'reviews/follows.html', {
        'form': form,
        'follows': follows,
        'followers': followers,
        'blocked_users': blocked_users
    })


# Désabonnement d'un utilisateur
@login_required
def unfollow_view(request, follow_id):
    follow_instance = get_object_or_404(
        UserFollows, id=follow_id, user=request.user
    )
    follow_instance.delete()
    return redirect('follows')


# Blocage d'un utilisateur
@login_required
def block_user(request, user_id):
    user_to_block = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        # Trouver la relation existante (user_to_block suit request.user)
        follow_relation = get_object_or_404(
            UserFollows,
            user=user_to_block,
            followed_user=request.user
        )
        # Marquer comme bloqué au lieu de supprimer
        follow_relation.is_blocked = True
        follow_relation.save()
        return redirect('follows')
    # Si ce n'est pas un POST, rediriger vers follows
    return redirect('follows')


# Déblocage d'un utilisateur
@login_required
def unblock_user(request, user_id):
    user_to_unblock = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        # Trouver la relation bloquée
        follow_relation = get_object_or_404(
            UserFollows,
            user=user_to_unblock,
            followed_user=request.user,
            is_blocked=True
        )
        # Marquer comme non bloqué (redevient un abonnement normal)
        follow_relation.is_blocked = False
        follow_relation.save()
        return redirect('follows')
    # Si ce n'est pas un POST, rediriger vers follows
    return redirect('follows')


# Page des publications de l'utilisateur
@login_required
def posts(request):
    user_tickets = Ticket.objects.filter(user=request.user).annotate(
        content_type=Value('TICKET', CharField())
    )
    user_reviews = Review.objects.filter(user=request.user).annotate(
        content_type=Value('REVIEW', CharField())
    )

    posts = sorted(
        chain(user_tickets, user_reviews),
        key=lambda post: post.time_created,
        reverse=True
    )

    return render(request, "reviews/posts.html", {
        "posts": posts,
        "is_posts_page": True
    })
