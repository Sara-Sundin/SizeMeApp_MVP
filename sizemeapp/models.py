from django.db import models
from products.models import Product

class GarmentFit(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='size_fits')
    size_label = models.CharField(max_length=10)  # e.g. XS, S, M, L
    chest = models.DecimalField(max_digits=5, decimal_places=1)  # in cm

    class Meta:
        unique_together = ['product', 'size_label']

    def __str__(self):
        return f"{self.product.name} - {self.size_label} (Chest: {self.chest}cm)"
