from django import template
from bizz.models import Product, Shop
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Count
import random
from account.models import Profile
from bizz.models import Shop

register = template.Library()

# @register.simple_tag
# def total_users_comment(product_id):
#     # get product
#     product = get_object_or_404(Product, product_id, active=True)
#
#     # return total number of comments
#     return product.comments.count()


@register.inclusion_tag('vinestream/users_comment.html')
def users_comment_all(product_id):
    product = get_object_or_404(Product, id=product_id)
    all_comments = product.comments.all()[:8]

    return {'all_comments':all_comments}


@register.inclusion_tag('vinestream/users_comment_field.html')
def users_comment(product_id):
    product = get_object_or_404(Product, id=product_id)
    all_comments = product.comments.all()[:3]

    return {'all_comments':all_comments}


# @register.inclusion_tag('vinestream/horizontal.html')
# def horizontal_scroll(user_id=None):
#     if user_id:
#         user = User.objects.get(id=user_id)

#     shops = Shop.objects.order_by('?')


    
    

#     return {'shops':shops}

@register.inclusion_tag('vinestream/horizontal.html')
def horizontal_scroll(count=None):
    

    # get ids of shop (list)
    #ids = [i for i in Shop.objects.values_list('id', flat=True)]
    # get a random sample of ids ()
    random_ids = random.sample([i for i in Shop.objects.values_list('id', flat=True)], Shop.objects.count())[:count]  # i will change it to 20 when their is enough shops
    #random_ids = random_ids[:count]
    # filter shops having such ids
    shops = sorted(Shop.objects.all(), key=lambda x: random.random())

    return {'shops':shops}

@register.inclusion_tag('vinestream/popular_products.html')
def popular_products(count):
    products = Product.objects.annotate(like=Count('users_like')).order_by('like')
    products = products[:count]

    return {'products':products}

@register.inclusion_tag('vinestream/new_shops.html')
def new_shops(user):
    #shops = Shop.objects.order_by('-created')[:30]
    friends = user.following.all()
    # users = User.objects.order_by('-created')[:20]
    #return {'shops':shops}
    return {'friends':friends}

@register.inclusion_tag('vinestream/new_users_faisal.html')
def new_users_faisal():
    users = User.objects.order_by('-id')[:20]
    return {'users':users}

@register.inclusion_tag('vinestream/new_users.html')
def new_users():
    profiles = Profile.objects.order_by('-created')[:100]
    return {'profiles':profiles}

@register.inclusion_tag('vinestream/new_user_suggestions.html')
def new_user_suggestions():
    shops = shops = Shop.objects.order_by('-created')[:15]
    return {'shops':shops}