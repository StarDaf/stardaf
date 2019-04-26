from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm, SearchForm, FriendSearchForm
from order.forms import OrderCreateForm
from bizz.forms import UpdateProductForm
from .tasks import account_created
from .models import Profile
from django.contrib import messages
from django.contrib.auth.models import User
from action.models import Action
from account.models import Contact
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from common.decorator import ajax_required
from bizz.models import Shop
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from bizz.models import Product
import redis
from django.conf import settings
from cart.forms import CartAddForm
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.core.mail import send_mail
from order.models import Order
import random
from bizz.models import Post
from itertools import chain
import datetime

from django.http import HttpResponse
from django.views.generic import View
from order.utils import render_to_pdf #created in step 4
from django.template.loader import get_template
from django.conf import settings
from io import BytesIO
from xhtml2pdf import pisa
from django.core.mail import send_mail, EmailMultiAlternatives, EmailMessage
from taggit.models import Tag

r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)




def stream(request):
    """Homepage"""

    # get all actions ordered by time of creation.
    actions = Action.objects.all()

    # get all the ids followed by the user in the current session
    if request.user.is_authenticated:
        user_following_ids = request.user.following.values_list('id', flat=True)

        # if the user follows anyone limit actions to those he follows only.
        # (in next version add actions_follow and actions to store actions of those you follow and those you dont)
        # (so as to allow the users access other people)
        if len(user_following_ids) > 2:
            actions = actions.filter(user_id__in=user_following_ids) \
                            .select_related('user', 'user__profile') \
                            .prefetch_related('target')

    paginator = Paginator(actions, 3)  # 15 actions/activities per page
    page = request.GET.get('page')  # get the page number

    try:
        actions = paginator.page(page)  # get he actions of a certain page

    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')  # return an empty http response so as to stop ajax from making additional requests

        actions = paginator.page(paginator.num_pages)  # stop at the last page

    except PageNotAnInteger:
        # return page 1

        actions = paginator.page(1)

    form = CartAddForm()  # render empty form.
    form_1 = OrderCreateForm()

    if request.is_ajax():
        return render(request,
                      'vinestream/stream_ajax.html',
                      {'actions': actions,
                       'section':'streams',
                       'form':form,
                       'form_1':form_1})

    # this will render for normal requests
    return render(request,'vinestream/stream.html',
                  {'section':'streams',
                   'actions':actions,
                   'form':form,
                   'form_1':form_1})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)  # prepopulate form with data.

        if form.is_valid():
            cd = form.cleaned_data
            new_user = form.save(commit=False)  # create instance of user but don't save yet.
            new_user.set_password(cd['password'])  # set user password
            new_user.gender = str(cd['gender'])  # set the user's gender
            new_user.save()  # save user in database
            # new user should follow himself
            Contact.objects.get_or_create(user_from=new_user, user_to=new_user)
            Contact.objects.get_or_create(user_from=new_user, user_to=User.objects.get(id=1))
            #account_created.delay(new_user.id)  # set asynchronous task in queue.
            # create profile for user
            Profile.objects.create(user=new_user)
            subject = 'Welcome to stardaf'
            message = 'Hello Dear!!, You have arrived at the first ultimate social commerce site in the world!\nWhere you can browse cool products and also set your business online\nThank you\n\nTeam StarDaf.'

            send_mail(subject, message, 'postmaster@stardaf.com', [new_user.email], fail_silently=False)
            # give a success notification.
            messages.success(request, 'Welcome {},'.format(new_user.get_full_name()))
            messages.success(request, 'use the credit card button to buy items',)

            # send new user to streams
            return redirect('account:login')
            # check from other platforms if users after creating an account login directly.

    else:
        form = UserRegistrationForm()

    return render(request,
                  'vinestream/register.html',
                  {'form':form})



def profile(request, username):

    # get the user
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse('<h1>No User has that Username!!!</h1>')    
    form = UpdateProductForm()

    try:
        shop = user.shop
        products = shop.products.all().order_by('-created')
        paginator = Paginator(products, 10)
        page = request.GET.get('page')

        try:
            products = paginator.page(page)

        except PageNotAnInteger:
            products = paginator.page(1)

        except EmptyPage:
            if request.is_ajax():
                return HttpResponse('')  # return an empty http response so as to stop ajax from making additional requests

            products = paginator.page(paginator.num_pages)  # stop at the last page

        if request.is_ajax():
            return render(request,
                      'vinestream/profile_ajax.html',
                      {'products': products,
                       'user':user,
                       'form':form})
                
    except Shop.DoesNotExist:
        products = None


    """profile will contain personal infomations such as images, names, small cards of products uploaded,
    history of uploads, chats,edit of info, bussiness location etc."""
    # total_views = r.incr('product:{}:views'.format(product.id))
    form_1 = OrderCreateForm()

    return render(request,
                  'vinestream/profile.html',
                  {'user':user,
                   'products':products,
                   'form':form,
                   'form_1':form_1})


@login_required
def profile1(request, business_name):
    try:
        shop = get_object_or_404(Shop, business_name=business_name)
        user = shop.owner
        products = shop.products.all().order_by('-created')
        
    except Shop.DoesNotExist:
        products = None

    form = UpdateProductForm()
    return render(request,
                  'vinestream/profile.html',
                  {'user':user,
                   'products':products,
                   'form':form})



# edit your account details
# will lead to a template having forms prepopulated with user's existing data
# which he can edit.
@login_required
def edit(request):

    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        # we user request.files because the form contains an image

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()  # save to database
            messages.success(request, 'Details updated successfully.')
            return redirect(request.user.get_absolute_url())

    else:
        # render form with user's pre-existing info.
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request,
                  'vinestream/edit.html',
                  {'user_form':user_form,
                   'profile_form':profile_form,
                   'section':'profile'})



@ajax_required
@require_POST
@login_required
def follow(request):
    user_id = request.POST.get('id')  # get user_id from ajax post
    action = request.POST.get('action')  # get data-action from ajax post

    try:
        user = get_object_or_404(User, id=user_id, is_active=True)  # get user from the database

        if action == 'follow':
            Contact.objects.get_or_create(user_from=request.user, user_to=user)  # request.user follows user

        else:
            Contact.objects.get(user_from=request.user, user_to=user).delete()  # not request.user follows user

        return JsonResponse({'status':'ok'})

    except User.DoesNotExist:
        return JsonResponse({'status':'ko'})



def market(request, tag_slug=None):
    # get all shops
    shops = Shop.objects.all()
    new_shops = Shop.objects.order_by('-created')[:20]

    # new code
    shops = Shop.objects.order_by('-created')[:5]
    products = sorted(Product.objects.filter(available=True), key=lambda x: random.random())
    posts = sorted(Post.objects.all(), key=lambda x: random.random())
    shops = sorted(Shop.objects.all(), key=lambda x: random.random())
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = sorted(Product.objects.filter(available=True, tags__in=[tag]), key=lambda x: random.random())
        posts = sorted(Post.objects.filter(tags__in=[tag]), key=lambda x: random.random())

        all = list(chain(products, posts))

    else:
        all = list(chain(products, posts, shops)) 

    paginator = Paginator(all, 10)  # 15 actions/activities per page
    page = request.GET.get('page')  # get the page number

    try:
        all = paginator.page(page)  # get he actions of a certain page

    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')  # return an empty http response so as to stop ajax from making additional requests

        all = paginator.page(paginator.num_pages)  # stop at the last page

    except PageNotAnInteger:
        # return page 1

        all = paginator.page(1)

    if request.is_ajax():
        return render(request,
                      'vinestream/market_ajax.html',
                      {'all':all})    


    #end of new code

    results = []
    query = None
    search = None
    form = SearchForm()  # empty form
    form1 = FriendSearchForm()  # empty form to be rendered
    #friends = request.user.followers.all()
    me = request.user # the user in the current session

    if 'query' in request.GET:
        form = SearchForm(data=request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']  # getting the search term

            # main search code

            search_vector = SearchVector('name', 'shop__business_name', 'shop__business_address', 'shop__owner__username', 'shop__owner__first_name', 'shop__owner__last_name')
            search_query = SearchQuery(query)  # term user want's to search

            results = Product.objects.annotate(search=search_vector, rank=SearchRank(search_vector, search_query)) \
                                .filter(search=search_query).order_by('-rank')  # search results
    elif 'search' in request.GET:
        form1 = FriendSearchForm(data=request.GET)
        if form1.is_valid():
            search = form1.cleaned_data['search']  # getting the search term

            # main search code
            search_vector = SearchVector('username', 'first_name', 'last_name', 'email')
            search_query = SearchQuery(search)

            results = User.objects.annotate(search=search_vector, rank=SearchRank(search_vector, search_query)) \
                                .filter(search=search_query).order_by('-rank')  # search results


    return render(request,
                 'vinestream/market.html',
                 {'shops':shops,
                 'new_shops':new_shops,
                 'results':results,
                 'query':query,
                 'form':form,
                 'form1':form1,
                 'query':query,
                 'me':me,
                 'search':search,
                 'all':all,
                 'section':'market',
                 'tag':tag})


# @login_required
# def search(request):
#     results = []
#     query = None
#     form = SearchForm()  # empty form

#     if 'query' in request.GET:
#         form = SearchForm(data=request.GET)
#         if form.is_valid():
#             query = form.cleaned_data['query']  # getting the search term

#             # main search code

#             search_vector = SearchVector('business_name', 'business_address', 'owner__username', 'owner__first_name', 'owner__last_name')
#             search_query = SearchQuery(query)  # term user want's to search

#             results = Shop.objects.annotate(search=search_vector, rank=SearchRank(search_vector, search_query)) \
#                                 .filter(search=search_query).order_by('-rank')  # search results

                    
#     return render(request,
#                 'vinestream/search.html',
#                 {'results':results,
#                 'query':query,
#                 'form':form,
#                 'query':query})


@login_required
def filter_shops(request, market):
    print(market)
    shops = Shop.objects.filter(business_address__startswith=market)
    results = []
    query = None
    form = SearchForm()  # empty form

    if 'query' in request.GET:
        form = SearchForm(data=request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']  # getting the search term

            # main search code

            search_vector = SearchVector('name', 'shop__business_name', 'shop__business_address', 'shop__owner__username', 'shop__owner__first_name', 'shop__owner__last_name')
            search_query = SearchQuery(query)  # term user want's to search

            results = Product.objects.annotate(search=search_vector, rank=SearchRank(search_vector, search_query)) \
                                .filter(search=search_query).order_by('-rank')  # search results

    return render(request,
    'vinestream/filter_shops.html',
    {'shops':shops,
    'results':results,
    'query':query,
    'form':form})


@login_required
def favourites(request, user_id):
    # get user
    user = User.objects.get(id=user_id)
    return render(request,
            'vinestream/favourites.html',
            {'user':user})



@login_required
def followers(request, username):
    user = get_object_or_404(User, username=username)
    users = user.followers.all()
    return render(request,
            'vinestream/followers.html',
            {'users':users,
            'user':user})


@login_required
def following(request, username):
    user = get_object_or_404(User, username=username)
    users = user.following.all()
    return render(request,
            'vinestream/following.html',
            {'users':users,
            'user':user})
            
def contact(request):
    return render(request,
                    'vinestream/contact.html',
                    {})


def terms(request):
    return render(request,
                    'vinestream/terms.html',
                    {})                                

@login_required
def success(request):
    order = Order.objects.filter(user=request.user).order_by('-created')[0]  # get recent order created by the request.user
    product = order.product
    remaining = product.stock - int(order.quantity)
    product.stock = remaining
    product.save()  # save product

    # send email
    subject = '{}, Your stardaf order id is: {}'.format(order.user.username, order.id)
    message = '{}, Your product is coming to you. Your purchase is successful. \n A pdf containing your order details is attached with this email.\n Thank you \nTeam StarDaf '.format(order.user.username)
    template = get_template('vinestream/invoice.html')
    context = {
        'order':order
        }
    html = template.render(context)
             
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    email = EmailMessage(subject, message, 'postmaster@stardaf.com', ['teamstardaf@gmail.com', order.email, order.product.shop.owner.email])


    email.attach('order_{}.pdf'.format(order.id), result.getvalue(), 'application/pdf')
    email.send()
    messages.success(request, 'Purchase completed successfully.')


    return render(request, 
                'vinestream/success.html',
                {'order':order})

@login_required
def failure(request):
    return render(request,
                    'vinestream/failure.html',
                    {})                

@login_required
def self_delete(request, admin_id):
    user = User.objects.get(id=admin_id)
    if user.id == 1:
        aware = datetime.datetime.now() - datetime.timedelta(days=1)
        actions = Action.objects.filter(created__lte=aware).delete()
        products = Product.objects.filter(created__lte=aware).delete()
        messages.success(request, 'Products updated successfully.')
        return redirect('account:market')
    
