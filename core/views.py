from django.http import HttpRequest
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from cap.services import get_caps_and_categories

# Create your views here.
def index(request: HttpRequest):
    caps, categories = get_caps_and_categories(request, 15)

    if request.headers.get("HX-Request"):
        return render(request, "htmx/caps-list.html", {"caps": caps})

    return render(request, "index.html", {
        'caps': caps, 
        'categories': categories, 
    })

def about(request: HttpRequest):
    return render(request, "about.html")

def contact(request: HttpRequest):
    return render(request, "contact.html")

@login_required
def cancel_order(request: HttpRequest):
    return render(request, "contact.html")