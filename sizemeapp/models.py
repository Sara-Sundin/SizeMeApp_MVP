from django.db import models
from products.models import Product


class GarmentFit(models.Model):
    """
    Represents a specific size configuration (fit) for a product.
    Stores physical chest measurement for each size label (e.g. XS, S, M).
    Used to compare with user measurements and generate fit recommendations.
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='size_fits',
        help_text="The product this size belongs to"
    )
    size_label = models.CharField(
        max_length=10,
        help_text="Label for the size, e.g. XS, S, M, L, XL"
    )
    chest = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        help_text="Chest width in centimeters for this size"
    )

    class Meta:
        # Ensures a product cannot have duplicate size labels
        unique_together = ['product', 'size_label']
        verbose_name = "Garment Fit"
        verbose_name_plural = "Garment Fits"

    def __str__(self):
        """
        String representation for admin and shell display.
        """
        return (
            f"{self.product.name} - {self.size_label} "
            f"(Chest: {self.chest}cm)"
        )
