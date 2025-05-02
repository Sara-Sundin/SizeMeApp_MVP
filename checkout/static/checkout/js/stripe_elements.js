/* global Stripe */
/* jshint esversion: 11 */

/* Stripe payment logic with vanilla JavaScript */

document.addEventListener('DOMContentLoaded', function () {
    // Get Stripe public key and client secret from hidden DOM elements
    const stripePublicKey = document.getElementById('id_stripe_public_key')?.textContent.replace(/['"]+/g, '');
    const clientSecret = document.getElementById('id_client_secret')?.textContent.replace(/['"]+/g, '');

    // Exit if keys are not present (e.g., template not fully loaded)
    if (!stripePublicKey || !clientSecret) return;

    // Initialize Stripe
    const stripe = Stripe(stripePublicKey);
    const elements = stripe.elements();

    // Define styling for Stripe card input
    const style = {
        base: {
            color: '#000',
            fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
            fontSmoothing: 'antialiased',
            fontSize: '16px',
            '::placeholder': {
                color: '#aab7c4'
            }
        },
        invalid: {
            color: '#dc3545',
            iconColor: '#dc3545'
        }
    };

    // Create and mount the card input element
    const card = elements.create('card', { style });
    card.mount('#card-element');

    // Listen for validation changes on card input
    card.on('change', function (event) {
        const errorDiv = document.getElementById('card-errors');
        if (!errorDiv) return;

        if (event.error) {
            // Display error message if validation fails
            errorDiv.innerHTML = `
                <span class="icon" role="alert">
                    <i class="fas fa-times"></i>
                </span>
                <span>${event.error.message}</span>
            `;
        } else {
            // Clear errors when valid
            errorDiv.textContent = '';
        }
    });

    const form = document.getElementById('payment-form');
    const submitBtn = document.getElementById('submit-button');
    const overlay = document.getElementById('loading-overlay');

    // Exit if form or button is missing
    if (!form || !submitBtn) return;

    form.addEventListener('submit', function (ev) {
        ev.preventDefault();

        // Disable card input and button while processing
        card.update({ 'disabled': true });
        submitBtn.disabled = true;

        // Hide form and show loading overlay
        form.classList.add('d-none');
        if (overlay) overlay.classList.remove('d-none');

        // Get save info toggle and CSRF token
        const saveInfo = document.getElementById('id-save-info')?.checked || false;
        const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

        // Build form data to cache before confirmation
        const postData = new FormData();
        postData.append('csrfmiddlewaretoken', csrfToken);
        postData.append('client_secret', clientSecret);
        postData.append('save_info', saveInfo);

        // Cache checkout data in Django before confirming payment
        fetch('/checkout/cache_checkout_data/', {
            method: 'POST',
            body: postData,
        }).then(response => {
            // Confirm the card payment with billing & shipping info
            return stripe.confirmCardPayment(clientSecret, {
                payment_method: {
                    card: card,
                    billing_details: {
                        name: form.full_name.value.trim(),
                        phone: form.phone_number.value.trim(),
                        email: form.email.value.trim(),
                        address: {
                            line1: form.street_address1.value.trim(),
                            line2: form.street_address2.value.trim(),
                            city: form.town_or_city.value.trim(),
                            state: form.county.value.trim(),
                            country: form.country.value.trim(),
                        }
                    }
                },
                shipping: {
                    name: form.full_name.value.trim(),
                    phone: form.phone_number.value.trim(),
                    address: {
                        line1: form.street_address1.value.trim(),
                        line2: form.street_address2.value.trim(),
                        city: form.town_or_city.value.trim(),
                        state: form.county.value.trim(),
                        postal_code: form.postcode.value.trim(),
                        country: form.country.value.trim(),
                    }
                },
            });
        }).then(result => {
            if (result.error) {
                // Display Stripe error and re-enable form
                const errorDiv = document.getElementById('card-errors');
                if (errorDiv) {
                    errorDiv.innerHTML = `
                        <span class="icon" role="alert">
                            <i class="fas fa-times"></i>
                        </span>
                        <span>${result.error.message}</span>
                    `;
                }

                form.classList.remove('d-none');
                if (overlay) overlay.classList.add('d-none');
                card.update({ 'disabled': false });
                submitBtn.disabled = false;
            } else {
                // If payment succeeded, submit the form to complete order
                if (result.paymentIntent.status === 'succeeded') {
                    form.submit();
                }
            }
        }).catch(() => {
            // Reload page on failure to retry cleanly
            location.reload();
        });
    });
});
