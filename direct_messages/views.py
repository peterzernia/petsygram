from django.shortcuts import render, reverse
from .models import DirectMessage
from django.views.generic import CreateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required


@login_required
def inbox(request):
    direct_messages = DirectMessage.objects.filter(receiver=request.user)
    context ={
        'direct_messages': direct_messages
    }
    return render(request, 'direct_messages/inbox.html', context)


@login_required
def sent(request):
    direct_messages = DirectMessage.objects.filter(sender=request.user)
    context ={
        'direct_messages': direct_messages
    }
    return render(request, 'direct_messages/sent.html', context)


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
