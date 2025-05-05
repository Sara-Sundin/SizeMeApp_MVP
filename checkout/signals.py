from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import OrderLineItem


@receiver(post_save, sender=OrderLineItem)
def update_on_save(sender, instance, created, **kwargs):
    """
    Signal handler to update the parent Order's total whenever a line item
    is created or updated.

    Args:
        sender (Model): The model class sending the signal.
        instance (OrderLineItem): The instance of the model being saved.
        created (bool): Whether this was a new instance or an update.
        **kwargs: Additional keyword arguments.
    """
    instance.order.update_total()


@receiver(post_delete, sender=OrderLineItem)
def update_on_delete(sender, instance, **kwargs):
    """
    Signal handler to update the parent Order's total when a line
    item is deleted.

    Args:
        sender (Model): The model class sending the signal.
        instance (OrderLineItem): The instance being deleted.
        **kwargs: Additional keyword arguments.
    """
    instance.order.update_total()
