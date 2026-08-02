import pytest

from rest_framework import status
from apps.reviews.services import create_review
from apps.reviews.models import Review
from django.contrib.auth import get_user_model


User = get_user_model()


@pytest.mark.django_db
def test_everyone_can_get_reviews(
        client,
        product,
        user
):
    Review.objects.create(
        review="Very good",
        mark=5,
        product=product,
        user=user
    )

    response = client.get("/api/reviews/")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == 1


@pytest.mark.django_db
def test_everyone_can_get_single_review(
        client,
        product,
        user
):
    review = Review.objects.create(
        review="Very good",
        mark=5,
        product=product,
        user=user
    )

    response = client.get(f"/api/reviews/{review.id}/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == review.id


@pytest.mark.django_db
def test_authenticated_user_can_create_review(
        client,
        user,
        product
):
    client.force_authenticate(user=user)

    data = {
        "review": "Amazing product",
        "mark": 5,
        "product": product.id
    }

    response = client.post(
        "/api/reviews/",
        data,
        format="json"
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert Review.objects.count() == 1


@pytest.mark.django_db
def test_anonymous_user_cannot_create_review(
        client,
        product
):
    data = {
        "review": "Amazing product",
        "mark": 5,
        "product_id": product.id
    }

    response = client.post(
        "/api/reviews/",
        data,
        format="json"
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_owner_can_update_review(
        client,
        user,
        product
):
    review = Review.objects.create(
        review="Old text",
        mark=5,
        product=product,
        user=user
    )

    client.force_authenticate(user=user)

    response = client.patch(
        f"/api/reviews/{review.id}/",
        {
            "review": "New text"
        },
        format="json"
    )

    review.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK
    assert review.review == "New text"


@pytest.mark.django_db
def test_user_cannot_update_another_users_review(
        client,
        user,
        product
):
    owner = User.objects.create_user(
        username="owner",
        password="123456"
    )

    review = Review.objects.create(
        review="Test",
        mark=5,
        product=product,
        user=owner
    )

    client.force_authenticate(user=user)

    response = client.patch(
        f"/api/reviews/{review.id}/",
        {
            "review": "Hacked"
        },
        format="json"
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_owner_can_delete_review(
        client,
        user,
        product
):
    review = Review.objects.create(
        review="Test",
        mark=5,
        product=product,
        user=user
    )

    client.force_authenticate(user=user)

    response = client.delete(
        f"/api/reviews/{review.id}/"
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Review.objects.count() == 0


@pytest.mark.django_db
def test_user_cannot_delete_another_users_review(
        client,
        user,
        product
):
    owner = User.objects.create_user(
        username="owner",
        password="123456"
    )

    review = Review.objects.create(
        review="Test",
        mark=5,
        product=product,
        user=owner
    )

    client.force_authenticate(user=user)

    response = client.delete(
        f"/api/reviews/{review.id}/"
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN