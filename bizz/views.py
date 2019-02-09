from django.shortcuts import render, redirect
from .forms import CreateShopForm, ShopEditForm, AddProductForm, UpdateProductForm
from .tasks import shop_created
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Shop, Product
from cart.forms import CartAddForm
from django.conf import settings
import redis
from Comment.forms import CommentForm
from action.action import create_action
from common.decorator import ajax_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db.models import Count
from action.models import Action


# connect to redis.
r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


@login_required
def create_shop(request, user_id):
    user = get_object_or_404(User, id=user_id, is_active=True)

    if request.method == 'POST':
        form = CreateShopForm(data=request.POST, files=request.FILES)  # prepopulate form with data.
        if form.is_valid():
            new_shop = form.save(commit=False)  # create instance of user but don't save to db yet.
            new_shop.owner = request.user
            new_shop.save()  # save to database
            shop_created.delay(new_shop.id)  # add asynchronous tasks to queue
            messages.success(request, 'Congratulations {}, You can add products to your shop through your profile {}' \
                             .format(new_shop.owner.username, new_shop.owner.get_absolute_url()))

            # return user to his profile where he will now have a add product link
            
            return redirect(new_shop.owner.get_absolute_url())

    else:
        form = CreateShopForm()
        messages.success(request, 'You will be further authenticated by our team. Creating a shop is free')

    return render(request,
                  'add_shop.html',
                  {'form':form,
                   'user':user})

@login_required
def edit(request):
    if request.method == 'POST':
        form = ShopEditForm(instance=request.user.shop, data=request.POST, files=request.FILES)
        if form.is_valid():
            shop = form.save(commit=False)
            shop.owner = request.user
            shop.save()

            messages.success(request, 'You have successfully updated your shop ;-)')
            return redirect(shop.owner.get_absolute_url())

    else:
        form = ShopEditForm(instance=request.user.shop)

    return render(request,
                  'edit_shop.html',
                  {'form':form})


@login_required
def add_product(request, shop_id):
    shop = get_object_or_404(Shop, id=shop_id)

    if request.method == 'POST':
        form = AddProductForm(data=request.POST, files=request.FILES)

        if form.is_valid():
            new_product = form.save(commit=False)

            new_product.shop = shop
            new_product.available = True # make the product available(because we are to filter available products only)
            new_product.save()  # save to database.
            create_action(user=new_product.shop.owner, verb='', target=new_product)

            messages.success(request, 'Product added successfully ;-)')

            # Return to profile of user
            return redirect(shop.owner.get_absolute_url())

    else:
        form = AddProductForm()  # render form

    return render(request,
                  'add_product.html',
                  {'shop':shop,
                   'form':form})


def detail(request, id, slug, username):
    
    
    user = User.objects.get(username=username)
    # get shop
    shop = Shop.objects.get(owner=user)
    # get product
    product = Product.objects.get(id=id, slug=slug, shop=shop)


    # product ranking
    r.zincrby('product_ranking', product.id, 1)  # create a sorted set of keys.

    # total views for a product
    total_views = r.incr('product:{}:views'.format(product.id))
    product.total_views = total_views  # set total views
    product.save()  # re-save product to persist total_views to database.
    comment = False

    # get the user ids that like a product
    users_likes_ids = product.users_like.values_list('id', flat=True)
    # get the five of these users from the database
    users_likes = User.objects.filter(id__in=[users_likes_ids])
    # filter other similar product they also like of same category.
    similar_products = []

    for user in users_likes:
        for pproduct in user.product_liked.filter(category=product.category).exclude(id=product.id):
            similar_products.append(pproduct)

    similar_products = similar_products[:5]

    # product_users_likes = product_users_likes.annotate(taste=Count('product_liked')).order_by('-taste', '-created')[:5]

    form = CartAddForm()
    # if request if post
    if request.method == 'POST':
        
        comment_form = CommentForm(data=request.POST)  # prepopulate data with existing form.

        if comment_form.is_valid():
            if request.user.is_authenticated:
                comment = comment_form.save(commit=False)  # create comment instance but don't save to the database yet.
                comment.product = product
                comment.user = request.user
                comment.email = str(request.user.email)
                comment.save()   # save comment form
            else:
                return redirect('account:login')    

    else:
        # get comment form
        comment_form = CommentForm()
        form = CartAddForm()  # render form

    return render(request,
                  'product_detail.html',
                  {'product':product,
                   'comment':comment,
                   'total_views':total_views,
                   'comment_form':comment_form,
                   'similar_products':similar_products,
                   'form':form})

@login_required
def product_ranking(request):
    product_ranking = r.zrange('product_ranking', 0, -1, desc=True)  # get sorted set.

    product_ranking_ids = [int(id) for id in product_ranking] # get ids of products in sorted set

    most_viewed = list(Product.objects.filter(id__in=product_ranking_ids))  # get the products that are being ranked
    most_viewed.sort(key=lambda x: product_ranking_ids.index(x.id))  # order product according to their ranking.

    return render(request,
                  'ranking.html',
                  {'most_viewed':most_viewed})

@login_required
def delete(request, product_id):
    product = get_object_or_404(Product, id=product_id, shop=request.user.shop)   # get product
    # get action which has this product as it's target
    id =int(product.id)
    actions = Action.objects.filter(target_id=id)
    actions.delete()  # delete action
    Product.objects.filter(name=product.name, id=product.id).delete() # delete the product from the database.



    return redirect(request.user.get_absolute_url())


# @ajax_required
# @require_POST
# @login_required
# def product_like(request):
#     product_id = request.POST.get('id')
#     product_action = request.POST.get('action')
#
#     if product_id and product_action:
#         try:
#             product = get_object_or_404(Product, id=product_id, available=True)
#             if product_action == 'like':
#                 # add request.user as liker of that product
#                 product.users_like.add(request.user)
#
#             else:
#                 # remove request.user as liker of that product
#                 product.users_like.remove(request.user)
#
#             return JsonResponse({'status':'ok'})
#
#         except Product.DoesNotExist:
#             pass
#
#     return JsonResponse({'status':'faisal'})


@ajax_required
@login_required
@require_POST
def like(request):
    """This view will attend to only post requests."""

    # retrieve data that are submitted with post request
    product_id = request.POST.get('id')
    product_action = request.POST.get('action')

    if product_id and product_action:
        try:
            product = Product.objects.get(pk=product_id)  # get the image that is to be liked or unliked
            if product_action == 'like':
                # if user like image add him to users_like attribute of the image
                product.users_like.add(request.user)
                # create_action(request.user, 'likes', image)
            else:
                product.users_like.remove(request.user)
            return JsonResponse({'status':'ok'})
        except:
            pass

    return JsonResponse({'status':'ko'})


@login_required
def recommend(request, user_id, product_id):
    user = get_object_or_404(User, id=user_id, is_active=True)
    product = get_object_or_404(Product, id=product_id, available=True)
    #  create recommendation action
    create_action(user, 'recommended', product)

    # return to the homepage
    return redirect('account:stream')

@login_required
def add_product_stock(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = UpdateProductForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            product.stock = cd['quantity']
            product.save()
            return redirect(product.shop.owner.get_absolute_url())


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



        