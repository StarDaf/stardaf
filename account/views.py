from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm, SearchForm
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
        if user_following_ids:
            actions = actions.filter(user_id__in=user_following_ids) \
                            .select_related('user', 'user__profile') \
                            .prefetch_related('target')

    paginator = Paginator(actions, 15)  # 15 actions/activities per page
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

    if request.is_ajax():
        return render(request,
                      'vinestream/stream_ajax.html',
                      {'actions': actions,
                       'section':'streams',
                       'form':form})

    # this will render for normal requests
    return render(request,'vinestream/stream.html',
                  {'section':'streams',
                   'actions':actions,
                   'form':form})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)  # prepopulate form with data.

        if form.is_valid():
            cd = form.cleaned_data
            new_user = form.save(commit=False)  # create instance of user but don't save yet.
            new_user.set_password(cd['password'])  # set user password
            new_user.gender = str(cd['gender'])  # set the user's gender
            new_user.save()  # save user in database
            #account_created.delay(new_user.id)  # set asynchronous task in queue.
            subject = 'Welcome to stardaf'
            message = 'Hello Dear!!, You have arrived at the first ultimate social commerce site in the world!\nWhere you can browse cool products and also set you business online\nTeam StarDaf.'

            send_mail(subject, message, 'postmaster@stardaf.com', [new_user.email], fail_silently=False)

            # create profile for user
            Profile.objects.create(user=new_user)
            # give a success notification.
            messages.success(request, 'Welcome {},'.format(new_user.get_full_name()))
            messages.success(request, 'Use the plus (+) button to add items to your bag',)

            # send new user to streams
            return redirect('account:login')
            # check from other platforms if users after creating an account login directly.

    else:
        form = UserRegistrationForm()

    return render(request,
                  'vinestream/register.html',
                  {'form':form})


@login_required
def profile(request, user_id, username):

    # get the user
    user = get_object_or_404(User, id=user_id, username=username)

    try:
        shop = user.shop
        products = shop.products.all().order_by('-created')


    except Shop.DoesNotExist:
        products = None


    """profile will contain personal infomations such as images, names, small cards of products uploaded,
    history of uploads, chats,edit of info, bussiness location etc."""
    # total_views = r.incr('product:{}:views'.format(product.id))
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


@login_required
def market(request):
    # get all shops
    shops = Shop.objects.all()
    new_shops = Shop.objects.order_by('-created')[:20]

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
                 'vinestream/market.html',
                 {'shops':shops,
                 'new_shops':new_shops,
                 'results':results,
                 'query':query,
                 'form':form,
                 'query':query})


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