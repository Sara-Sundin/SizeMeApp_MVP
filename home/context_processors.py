from .forms import ContactForm


def global_context(request):
    """
    Provides global context variables to all templates.

    Includes:
    - Contact form with 'contact' prefix for footer use
    - Flags for triggering modals after form submission or logout
    """

    # Pop session flags (remove after one use)
    show_success_modal = request.session.pop(
        "show_success_modal", False
        )
    show_logged_out_modal = request.session.pop(
        "show_logged_out_modal", False
        )
    show_account_deleted_modal = request.session.pop(
        "show_account_deleted_modal", False
        )

    return {
        "contact_form": ContactForm(prefix='contact'),
        "show_success_modal": show_success_modal,
        "show_logged_out_modal": show_logged_out_modal,
        "show_account_deleted_modal": show_account_deleted_modal,
    }
