# reviews/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Ticket, Review


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        common = {
            'class': (
                'w-full border border-black px-1 py-2 '
                'text-center placeholder-black'
            ),
        }

        placeholders = {
            'username':       "Nom d'utilisateur",
            'password1':      "Mot de passe",
            'password2':      "Confirmation mot de passe",
        }
        for name, ph in placeholders.items():
            self.fields[name].widget.attrs.update({
                **common,
                'placeholder': ph
            })


class CustomLoginForm(AuthenticationForm):
    class Meta:
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        common = {
            'class': (
                'px-20 py-2 border border-black '
                'placeholder-black text-center'
            )
        }
        # placeholders associés à chaque champ
        placeholders = {
            'username': "Nom d’utilisateur",
            'password': "Mot de passe"
        }
        for name, ph in placeholders.items():
            self.fields[name].widget.attrs.update({
                **common,
                'placeholder': ph
            })


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        common = {
            'class': 'w-full border border-black py-2'
        }

        placeholders = {
            'title': "",
            'description': "",
            'image': ""
        }

        for name, ph in placeholders.items():
            attrs = {**common}
            if name == 'image':
                attrs.update({
                    'class': 'px-31 py-2'
                })
            elif ph:
                attrs['placeholder'] = ph
            self.fields[name].widget.attrs.update(attrs)


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        common = {
            'class': 'w-full border border-black px-8 py-2'
        }

        placeholders = {
            'headline': "",
            'rating': "",
            'body': ""
        }

        for name, ph in placeholders.items():
            attrs = {**common}
            if name == 'rating':
                self.fields[name].widget = forms.RadioSelect(
                    choices=[(i, str(i)) for i in range(6)],
                    attrs={
                        'class': (
                            'flex list-none p-0 items-center space-x-4'
                        )
                    }
                )
            else:
                if ph:
                    attrs['placeholder'] = ph
                if name == 'body':
                    self.fields[name].widget = forms.Textarea(
                        attrs={**attrs, 'rows': 5}
                    )
                else:
                    self.fields[name].widget.attrs.update(attrs)


class FollowUserForm(forms.Form):
    username = forms.CharField(
        label="Nom d'utilisateur à suivre",
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': "Nom d'utilisateur",
            'class': 'w-full border border-black px-3 py-2 text-center'
        })
    )

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        super().__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data['username']
        if username == self.current_user.username:
            raise forms.ValidationError(
                "Vous ne pouvez pas vous suivre vous-même."
            )
        try:
            user_to_follow = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError("Cet utilisateur n'existe pas.")

        if self.current_user.following.filter(
            followed_user=user_to_follow,
            is_blocked=False
        ).exists():
            raise forms.ValidationError("Vous suivez déjà cet utilisateur.")
        # Vérifier si cet utilisateur nous a bloqués
        from .models import UserFollows
        if UserFollows.objects.filter(
            user=self.current_user,
            followed_user=user_to_follow,
            is_blocked=True
        ).exists():
            raise forms.ValidationError(
                "Vous ne pouvez pas suivre cet utilisateur."
            )
        return username
