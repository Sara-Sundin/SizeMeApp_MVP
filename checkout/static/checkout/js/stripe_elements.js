/*
    Stripe payment logic with vanilla JavaScript
*/

document.addEventListener('DOMContentLoaded', function () {
    const stripePublicKey = document.getElementById('id_stripe_public_key')?.textContent.replace(/['"]+/g, '');
    const clientSecret = document.getElementById('id_client_secret')?.textContent.replace(/['"]+/g, '');

    if (!stripePublicKey || !clientSecret) return;

    const stripe = Stripe(stripePublicKey);
    const elements = stripe.elements();

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

    const card = elements.create('card', { style });
    card.mount('#card-element');

    card.on('change', function (event) {
        const errorDiv = document.getElementById('card-errors');
        if (!errorDiv) return;

        if (event.error) {
            errorDiv.innerHTML = `
                <span class="icon" role="alert">
                    <i class="fas fa-times"></i>
                </span>
                <span>${event.error.message}</span>
            `;
        } else {
            errorDiv.textContent = '';
        }
    });

    const form = document.getElementById('payment-form');
    const submitBtn = document.getElementById('submit-button');
    const overlay = document.getElementById('loading-overlay');

    if (!form || !submitBtn) return;

    form.addEventListener('submit', function (ev) {
        ev.preventDefault();

        card.update({ 'disabled': true });
        submitBtn.disabled = true;
        form.classList.toggle('d-none');
        if (overlay) overlay.classList.toggle('d-none');

        const saveInfo = document.getElementById('id-save-info')?.checked || false;
        const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

        const postData = new FormData();
        postData.append('csrfmiddlewaretoken', csrfToken);
        postData.append('client_secret', clientSecret);
        postData.append('save_info', saveInfo);

        fetch('/checkout/cache_checkout_data/', {
            method: 'POST',
            body: postData,
        }).then(response => {
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
                const errorDiv = document.getElementById('card-errors');
                if (errorDiv) {
                    errorDiv.innerHTML = `
                        <span class="icon" role="alert">
                            <i class="fas fa-times"></i>
                        </span>
                        <span>${result.error.message}</span>
                    `;
                }

                form.classList.toggle('d-none');
                if (overlay) overlay.classList.toggle('d-none');
                card.update({ 'disabled': false });
                submitBtn.disabled = false;
            } else {
                if (result.paymentIntent.status === 'succeeded') {
                    form.submit();
                }
            }
        }).catch(() => {
            location.reload();
        });
    });
});
