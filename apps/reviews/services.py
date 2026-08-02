from rest_framework.exceptions import ValidationError
from .models import Review
from django.db import transaction

@transaction.atomic
def can_user_create_review(user, product):

    review_exists = Review.objects.filter(
        user=user,
        product=product
    ).exists()

    if review_exists:
        raise ValidationError(
            "You have already reviewed this product."
        )

    return True

@transaction.atomic
def create_review(data, user):

    product = data["product"]

    can_user_create_review(
        user=user,
        product=product
    )

    review = Review.objects.create(
        user=user,
        product=product,
        mark=data["mark"],
        review=data["review"]
    )

    return review