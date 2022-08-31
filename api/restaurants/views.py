from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from restaurants.models import Restaurant
from restaurants.serializers import RestaurantSerializer

@api_view(['GET', 'POST'])
def restaurant_list(request, format=None):
    """
    List all code restaurants, or create a new restaurant.
    """
    if request.method == 'GET':
        restaurants = Restaurant.objects.all()
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = RestaurantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def restaurant_detail(request, pk, format=None):
    """
    Retrieve, update or delete a code restaurant.
    """
    try:
        restaurant = Restaurant.objects.get(pk=pk)
    except Restaurant.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RestaurantSerializer(restaurant)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = RestaurantSerializer(restaurant, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        restaurant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)