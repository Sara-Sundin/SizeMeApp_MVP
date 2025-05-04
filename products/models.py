from django.db import models


class Category(models.Model):
    """
    Represents a category for products (e.g., T-Shirts, Sweatshirts).
    Also includes stretch factors used in fit recommendation logic.
    """

    class Meta:
        verbose_name_plural = 'Categories'  # Displayed name in Django admin

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    # Stretch factors for size recommendations based on fit type
    slim_factor = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=1.00,
        help_text="Stretch factor for slim fit"
    )
    regular_factor = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=1.10,
        help_text="Stretch factor for regular fit"
    )
    loose_factor = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=1.20,
        help_text="Stretch factor for loose fit"
    )

    def __str__(self):
        """
        String representation shown in Django admin and elsewhere.
        """
        return self.name

    def get_friendly_name(self):
        """
        Returns the display-friendly version of the category name.
        """
        return self.friendly_name


class Product(models.Model):
    """
    Represents a product in the webshop. Belongs to a category and can have images, sizes, and a price.
    """

    category = models.ForeignKey(
        'Category',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="Category this product belongs to"
    )
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    has_sizes = models.BooleanField(
        default=False,
        null=True,
        blank=True,
        help_text="Indicates if the product has size variants"
    )
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image_url = models.URLField(
        max_length=1024,
        null=True,
        blank=True,
        help_text="Optional image URL if not using upload"
    )
    image = models.ImageField(
        upload_to='products/',
        null=True,
        blank=True,
        help_text="Image uploaded directly to media storage"
    )

    def __str__(self):
        """
        String representation for the product.
        """
        return self.name
