from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Count, Avg

# Create your models here.

class Movie(models.Model):
    title=models.CharField(max_length=32)
    description=models.TextField(max_length=360)

    def no_of_rating(self):
        rating=Rating.objects.filter(movie=self)
        return len(rating)
    
    def avg_rating(self):
        ratings = Rating.objects.filter(movie=self)
        rating_count = ratings.count()
        if rating_count > 0:
            sum_stars = ratings.aggregate(Avg('star'))['star__avg']  
            return sum_stars
        else:
            return 0

class Rating(models.Model):
    movie=models.ForeignKey(Movie, on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    star=models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        unique_together=(('user','movie'),)
        indexes=[models.Index(fields=['user','movie']),]

