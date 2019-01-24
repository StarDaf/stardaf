from django.shortcuts import render, get_object_or_404, redirect
from bizz.models import Product
from django.contrib.auth.decorators import login_requried
from .forms import CommentForm
from django.contrib import messages

@login_requried
def comment_add(request, product_id):

    # get product
    product = get_object_or_404(Product, id=product_id, available=True)
    if request.method == 'POST':
        form = CommentForm(data=request.POST)

        if form.is_valid():
            cd = form.cleaned_data

            new_comment = form.save(commit=False)
            new_comment.product = product
            new_comment.user = request.user
            new_comment.email = request.user.email  # setting the user's email
            new_comment.save()  # comment added to database.

            # a success message
            messages.success(request, 'Comment added successfully')

            return redirect('bizz:detail')  # return back to products detail page.





