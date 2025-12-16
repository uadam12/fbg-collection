from django.http import HttpRequest
from django.core.paginator import Paginator
from cap.models import Category, Cap
from django.db.models import Q


def get_caps_and_categories(request: HttpRequest, per_page=15):
    # Get query params
    category_ids = request.GET.getlist("category")  # list of categories
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    search = request.GET.get("search")
    page = int(request.GET.get("page", "1"))

    caps = Cap.objects.select_related("category").all()

    # Filter by multiple categories
    if category_ids:
        caps = caps.filter(category_id__in=category_ids)

    # Filter by price
    if min_price:
        caps = caps.filter(price__gte=min_price)
    if max_price:
        caps = caps.filter(price__lte=max_price)

    # Filter by search in name or description
    if search:
        caps = caps.filter(Q(name__icontains=search))

    paginator = Paginator(caps, per_page)
    page_obj = paginator.get_page(page)

    categories = Category.objects.only("name")  # for filtering UI

    return page_obj, categories