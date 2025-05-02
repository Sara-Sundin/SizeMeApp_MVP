from django.db import models

class Plan(models.Model):
    """
    Model representing a subscription plan for SizeMeApp.
    Each plan includes pricing, features, and optional styling data 
    used in the frontend for icon and button customization.
    """

    PLAN_TYPE_CHOICES = [
        ('starter', 'Starter'),
        ('growth', 'Growth'),
        ('enterprise', 'Enterprise'),
    ]

    name = models.CharField(max_length=100)
    plan_type = models.CharField(
        max_length=20,
        choices=PLAN_TYPE_CHOICES,
        unique=True,
        help_text="Type identifier used for internal logic and URL filtering"
    )
    monthly_price = models.DecimalField(
        max_digits=10, decimal_places=2,
        help_text="Monthly subscription price"
    )
    setup_cost = models.DecimalField(
        max_digits=10, decimal_places=2,
        help_text="One-time setup cost"
    )
    short_description = models.CharField(
        max_length=255,
        help_text="Brief description shown on pricing cards"
    )
    long_description = models.TextField(
        help_text="Detailed description shown on the plan detail page"
    )
    features = models.TextField(
        help_text="List of features separated by newlines"
    )
    perfect_for = models.TextField(
        blank=True, null=True,
        help_text="Optional field describing ideal users or businesses"
    )

    icon_class = models.CharField(
        max_length=50,
        help_text="Font Awesome icon class used for the plan icon",
        blank=True
    )
    icon_color_class = models.CharField(
        max_length=50,
        help_text="CSS class for controlling the icon color",
        blank=True
    )
    button_class = models.CharField(
        max_length=50,
        help_text="CSS class for styling the plan's button",
        blank=True
    )

    def feature_list(self):
        """
        Return a list of features by splitting the features string on newlines.
        Useful for rendering as an unordered list in templates.
        """
        return self.features.splitlines()

    def __str__(self):
        """
        String representation of the Plan, shown in admin and shell.
        """
        return self.name
