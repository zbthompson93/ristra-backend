from django.db import models

class Review(models.Model):
    # User
    # Text
    comment = models.TextField()
    # Ratings
    rating = models.IntegerField()
    # Pictures
    #picture = models.ImageField()

    def __str__(self):
        return self.comment

    class Meta:
        ordering = ('comment',)

class Restaurant(models.Model):
    # Name
    title = models.CharField(max_length=100)
    # Description
    description = models.TextField()
    # Location
    location = models.CharField(max_length=100)
    # Reviews (many to one)
    reviews = models.ManyToManyField(Review)
    # Tags (for filtering)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)
