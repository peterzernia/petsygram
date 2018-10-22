from django.shortcuts import render, reverse, get_object_or_404
from .models import DirectMessage
from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from itertools import chain
from operator import attrgetter


class InboxView(LoginRequiredMixin, ListView):
    model = DirectMessage
    template_name = 'direct_messages/inbox.html'

# Queryset returns one DirectMessage, if it exists, from every user to create
# a link to the message thread with that user.
    def get_queryset(self):
        senders = User.objects.all()
        queryset = []
        for sender in senders:
            if sender != self.request.user:
                direct_messages =  DirectMessage.objects.filter(sender=sender, receiver=self.request.user)
                if direct_messages:
                    queryset.append(direct_messages[0])
        return queryset


class ThreadView(LoginRequiredMixin, ListView):
    model = DirectMessage
    template_name = 'direct_messages/thread.html'

# Queryset combines two querysets between two users, one with user as reciever,
# and one with user as sender, then orders by date to display a message thread
# between two users.
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        dm1 = DirectMessage.objects.filter(receiver=user, sender=self.request.user)
        dm2 = DirectMessage.objects.filter(receiver=self.request.user, sender=user)
        direct_messages = sorted((chain(dm1, dm2)), key=attrgetter('date_sent'))
        return direct_messages


class CreateDirectMessage(LoginRequiredMixin, CreateView):
    model = DirectMessage
    fields = ['receiver', 'content']

    def get_success_url(self, **kwargs):
        return reverse('direct_messages-inbox')

    def form_valid(self, form):
        form.instance.sender = self.request.user
        return super().form_valid(form)


class ViewDirectMessage(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = DirectMessage

    def test_func(self):
        message = self.get_object()
        if self.request.user == message.sender or self.request.user == message.receiver:
            return True
        return False


class DeleteDirectMessage(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = DirectMessage

    def test_func(self):
        message = self.get_object()
        if self.request.user == message.sender or self.request.user == message.receiver:
            return True
        return False

    def get_success_url(self, **kwargs):
        username = self.object.receiver
        return reverse( 'direct_messages-thread', args={username: 'username'})
