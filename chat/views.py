from django.shortcuts import render, get_object_or_404, redirect
from .models import Thread
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import ChatForm
from .models import ChatMessage
from bizz.models import Product


@login_required
def thread(request, username):
    user = request.user  # get the current user in the request context.
    #product = get_object_or_404(Product, id=product_id)
    other_user = User.objects.get(username=username)  # get the other user
    thread = Thread.objects.get_or_new(user, other_user)[0]  # get_or_create thread between users.
    # this is returning None.
    form = ChatForm()


    if request.method == 'POST':
        message = request.POST.get('message')

        
        # create chat message instance but don't save to the database yet.
        new_chat = ChatMessage.objects.create(thread=thread, user=user, message=message)
        new_chat.save()  # save to database.
        return render(request,
                'chats/thread.html',
                {'thread':thread,
                'user':user,
                'form':form,
                'other_user':other_user})

    else:
        form = ChatForm()  # send empty chat form to the template.
        
    return render(request,
        'chats/thread.html',
        {'thread':thread,
        'user':user,
        'form':form,
        'other_user':other_user})

      


@login_required
def chats(request):
    user = request.user
    threads = list(Thread.objects.filter(first=user)) + list(Thread.objects.filter(second=user))
    return render(request,
    'chats/mychats.html',
    {'user':user,
    'threads':threads})