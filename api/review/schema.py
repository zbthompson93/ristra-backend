import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from review.models import Review, Restaurant

# Create a GraphQL type for the Review model
class ReviewType(DjangoObjectType):
    class Meta:
        model = Review

# Create a GraphQL type for the Restaurant model
class RestaurantType(DjangoObjectType):
    class Meta:
        model = Restaurant

# Create a Query type
class Query(ObjectType):
    review = graphene.Field(ReviewType, id=graphene.Int())
    restaurant = graphene.Field(RestaurantType, id=graphene.Int())
    reviews = graphene.List(ReviewType)
    restaurants= graphene.List(RestaurantType)

    def resolve_review(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Review.objects.get(pk=id)

        return None

    def resolve_restaurant(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Restaurant.objects.get(pk=id)

        return None

    def resolve_reviews(self, info, **kwargs):
        return Review.objects.all()

    def resolve_restaurants(self, info, **kwargs):
        return Restaurant.objects.all()
