/* jshint esversion: 6 */

// Get CSRF token from cookies (safe for external scripts)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Match cookie by name
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Enable or disable +/- buttons based on input value
function handleEnableDisable(itemId) {
    const qtyInput = document.getElementById(`id_qty_${itemId}`);
    const value = parseInt(qtyInput.value);
    const minus = document.getElementById(`decrement-qty_${itemId}`);
    const plus = document.getElementById(`increment-qty_${itemId}`);
    minus.disabled = value <= 1;
    plus.disabled = value >= 99;
}

// Run after DOM is fully loaded
document.addEventListener("DOMContentLoaded", function () {
    // Set correct button state on load
    const qtyInputs = document.querySelectorAll('.qty_input');
    qtyInputs.forEach(input => {
        const itemId = input.dataset.item_id;
        handleEnableDisable(itemId);
    });

    // Increment quantity
    document.querySelectorAll('.increment-qty').forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            const itemId = this.dataset.item_id;
            const input = document.getElementById(`id_qty_${itemId}`);
            input.value = Math.min(99, parseInt(input.value) + 1);
            handleEnableDisable(itemId);
            input.closest('form').submit(); // Submit the form to update quantity
        });
    });

    // Decrement quantity
    document.querySelectorAll('.decrement-qty').forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            const itemId = this.dataset.item_id;
            const input = document.getElementById(`id_qty_${itemId}`);
            input.value = Math.max(1, parseInt(input.value) - 1);
            handleEnableDisable(itemId);
            input.closest('form').submit(); // Submit the form to update quantity
        });
    });

    // Manual update link (if using a clickable "Update" link)
    document.querySelectorAll('.update-link').forEach(link => {
        link.addEventListener('click', function () {
            const form = this.previousElementSibling;
            if (form.classList.contains('update-form')) {
                form.submit();
            }
        });
    });

    // Remove item from bag
    document.querySelectorAll('.remove-item').forEach(link => {
        link.addEventListener('click', function () {
            const itemId = this.id.split('remove_')[1];
            const csrfToken = getCookie('csrftoken');

            fetch(`/bag/remove/${itemId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json',
                },
            })
            .then(response => {
                if (response.ok) {
                    location.reload(); // Reload page after successful removal
                } else {
                    console.error("Remove failed with status:", response.status);
                }
            })
            .catch(error => console.error("Remove request error:", error));
        });
    });
});
