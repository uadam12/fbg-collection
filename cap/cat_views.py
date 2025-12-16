from django.http import HttpRequest
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from app.decorators import staff_required
from cap.models import Category


@staff_required
def categories(request: HttpRequest):
    categories = Category.objects.annotate(
        total_caps=Count('caps')
    )
    return render(request, 'categories/list.html', {
        'categories': categories
    })


@staff_required
def create_category(request: HttpRequest):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Category.objects.create(name=name)
            return redirect('cap:categories')
    return render(request, 'categories/form.html')


@staff_required
def update_category(request: HttpRequest, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            category.name = name
            category.save()
            return redirect('cap:categories')

    return render(request, 'categories/form.html', {
        'category': category
    })


@staff_required
def delete_category(request: HttpRequest, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        category.delete()
        return redirect('cap:categories')

    return render(request, 'delete.html', {
        'object': category, 'back_url': 'categories'
    })
