from random import randint, choice
from cap.models import Cap, Category


def add_dummy():
    categories = Category.objects.all()
    img = Cap.objects.first().image
    caps = [Cap(
        image=img,
        name=f"Cap {i}",
        price=randint(2500, 10000),
        category=choice(categories),
        description=f"Cap {i} description",
        is_available=choice([False, True, True, True, True, True, True, True, True, True])
    ) for i in range(1, 501)]

    Cap.objects.bulk_create(caps)