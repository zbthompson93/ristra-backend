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

# Create Input Object Types
class ReviewInput(graphene.InputObjectType):
    id = graphene.ID()
    comment = graphene.String()
    rating = graphene.Int()

class RestaurantInput(graphene.InputObjectType):
    id = graphene.ID()
    title = graphene.String()
    description = graphene.String()
    location = graphene.String()
    reviews = graphene.List(ReviewInput)

# Create mutations for reviews
class CreateReview(graphene.Mutation):
    class Arguments:
        input = ReviewInput(required=True)

    ok = graphene.Boolean()
    review = graphene.Field(ReviewType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        review_instance = Review(comment=input.comment, rating=input.rating)
        review_instance.save()
        return CreateReview(ok=ok, review=review_instance)

class UpdateReview(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = ReviewInput(required=True)

    ok = graphene.Boolean()
    review = graphene.Field(ReviewType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        review_instance = Review.objects.get(pk=id)
        if review_instance:
            ok = True
            review_instance.comment = input.comment
            review_instance.rating = input.rating
            review_instance.save()
            return UpdateReview(ok=ok, review=review_instance)
        return UpdateReview(ok=ok, review=None)

# Create mutations for restaurants
class CreateRestaurant(graphene.Mutation):
    class Arguments:
        input = RestaurantInput(required=True)

    ok = graphene.Boolean()
    restaurant = graphene.Field(RestaurantType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        reviews = []
        for review_input in input.reviews:
          review = Review.objects.get(pk=review_input.id)
          if review is None:
            return CreateRestaurant(ok=False, restaurant=None)
          reviews.append(review)
        restaurant_instance = Restaurant(
          title=input.title,
          description=input.description,
          location=input.location
          )
        restaurant_instance.save()
        restaurant_instance.reviews.set(reviews)
        return CreateRestaurant(ok=ok, restaurant=restaurant_instance)

class UpdateRestaurant(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = RestaurantInput(required=True)

    ok = graphene.Boolean()
    restaurant = graphene.Field(RestaurantType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        restaurant_instance = Restaurant.objects.get(pk=id)
        if restaurant_instance:
            ok = True
            reviews = []
            for review_input in input.reviews:
              review = Review.objects.get(pk=review_input.id)
              if review is None:
                return UpdateRestaurant(ok=False, restaurant=None)
              reviews.append(review)
            restaurant_instance.title=input.title
            restaurant_instance.description=input.description
            restaurant_instance.location=input.location
            restaurant_instance.save()
            restaurant_instance.reviews.set(reviews)
            return UpdateRestaurant(ok=ok, restaurant=restaurant_instance)
        return UpdateRestaurant(ok=ok, morestaurantvie=None)

class Mutation(graphene.ObjectType):
    create_review = CreateReview.Field()
    update_review = UpdateReview.Field()
    create_restaurant = CreateRestaurant.Field()
    update_restaurant = UpdateRestaurant.Field()
