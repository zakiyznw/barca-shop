import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('Jersey', 'Jersey'),
        ('Accessory', 'Aksesori'),
        ('Shoes', 'Sepatu'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    price = models.IntegerField()
    stock = models.IntegerField(default=0)
    description = models.TextField()
    thumbnail = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='jersey')
    is_featured = models.BooleanField(default=False)
    rating = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    total_ratings = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
    
    def add_rating(self, new_rating):
        if 0.0 <= new_rating <= 5.0:  # validasi rating
            total_score = self.rating * self.total_ratings
            total_score += new_rating
            self.total_ratings += 1
            self.rating = total_score / self.total_ratings
            self.save()
        else:
            raise ValueError("Rating harus antara 0.0 sampai 5.0")

    def add_stock(self, amount):
        if amount > 0:
            self.stock += amount
            self.save()
        else:
            raise ValueError("Jumlah penambahan stok harus positif")
    
    def reduce_stock(self, amount):
        if 0 < amount <= self.stock:
            self.stock -= amount
            self.save()
        else:
            raise ValueError("Jumlah pengurangan stok tidak valid")