from django.shortcuts import render, reverse
from .models import DirectMessage
from django.views.generic import ListView, CreateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required


class InboxView(LoginRequiredMixin, ListView):
    model = DirectMessage
    template_name = 'direct_messages/inbox.html'

    def get_queryset(self):
        direct_messages = DirectMessage.objects.filter(receiver=self.request.user)
        direct_messages = direct_messages.order_by('-date_sent')
        return direct_messages


class SentView(LoginRequiredMixin, ListView):
    model = DirectMessage
    template_name = 'direct_messages/sent.html'

    def get_queryset(self):
        direct_messages = DirectMessage.objects.filter(sender=self.request.user)
        direct_messages = direct_messages.order_by('-date_sent')
        return direct_messages


class CreateDirectMessage(LoginRequiredMixin, CreateView):
    model = DirectMessage
    fields = ['receiver', 'content']
    sucess_url = '/messages/sent/'

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

    def get_success_url(self):
        return reverse('direct_messages-inbox')
