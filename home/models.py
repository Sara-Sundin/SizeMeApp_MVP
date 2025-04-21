from django.db import models

class Plan(models.Model):
    PLAN_TYPE_CHOICES = [
        ('starter', 'Starter'),
        ('growth', 'Growth'),
        ('enterprise', 'Enterprise'),
    ]

    name = models.CharField(max_length=100)
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPE_CHOICES, unique=True)
    monthly_price = models.DecimalField(max_digits=10, decimal_places=2)
    setup_cost = models.DecimalField(max_digits=10, decimal_places=2)
    short_description = models.CharField(max_length=255)
    long_description = models.TextField()
    features = models.TextField(help_text="Separate features with a newline")
    perfect_for = models.TextField(blank=True, null=True)
    icon_class = models.CharField(max_length=100, help_text="Font Awesome icon class", blank=True)
    cta_label = models.CharField(max_length=100, default="Pay Now")
    contact_cta_label = models.CharField(max_length=100, blank=True, null=True)
    order = models.PositiveIntegerField(default=0, help_text="Lower number = higher display priority")

    class Meta:
        ordering = ['order']

    def feature_list(self):
        return self.features.splitlines()

    def __str__(self):
        return f"{self.name} Plan"
