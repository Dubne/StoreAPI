from rest_framework.exceptions import ValidationError
from reviews.models import Review

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

def create_review(data, user):

    product = data["product"]

    can_user_create_review(
        user=user,
        product=product
    )

    review = Review.objects.create(
        user=user,
        product=product,
        rating=data["rating"],
        description=data["description"]
    )

    return review