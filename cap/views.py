from django.http import HttpRequest
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from app.decorators import staff_required
from cap.models import Cap, Category


@staff_required
def caps(request: HttpRequest):
    category = request.GET.get("category")
    page = int(request.GET.get('page', '1'))
    caps = Cap.objects.select_related('category')

    if category:
        caps = caps.filter(category_id=category)
    
    paginator = Paginator(caps, 15)

    return render(request, 'caps/list.html', {
        'caps': paginator.get_page(page), 
        'categories': Category.objects.only("name")
    })


@staff_required
def create_cap(request: HttpRequest):
    categories = Category.objects.all()

    if request.method == 'POST':
        Cap.objects.create(
            name=request.POST.get('name'),
            category_id=request.POST.get('category'),
            price=request.POST.get('price'),
            image=request.FILES.get('image')
        )
        messages.success(request, "Cap created successfully!!!")
        return redirect('cap:list')

    return render(request, 'caps/form.html', {
        'categories': categories
    })


@staff_required
def update_cap(request: HttpRequest, pk):
    cap = get_object_or_404(Cap, pk=pk)
    categories = Category.objects.all()

    if request.method == 'POST':
        cap.name = request.POST.get('name')
        cap.category_id = request.POST.get('category')
        cap.price = request.POST.get('price')
        if request.FILES.get('image'):
            cap.image = request.FILES.get('image')
        cap.save()
        messages.success(request, "Cap updated successfully!!!")
        return redirect('cap:list')

    return render(request, 'caps/form.html', {
        'cap': cap,
        'categories': categories
    })


@staff_required
def delete_cap(request: HttpRequest, pk):
    cap = get_object_or_404(Cap, pk=pk)

    if request.method == 'POST':
        cap.delete()
        messages.success(request, "Cap deleted successfully!!!")
        return redirect('cap:list')

    return render(request, 'delete.html', {
        'object': cap, 'back_url': 'cap:list'
    })
