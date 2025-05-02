/* jshint esversion: 6 */
/* global bootstrap */

// Enable/disable +/- buttons based on quantity
    function handleEnableDisable(itemId) {
        const qtyInput = document.getElementById(`id_qty_${itemId}`);
        const value = parseInt(qtyInput.value);
        const minus = document.getElementById(`decrement-qty_${itemId}`);
        const plus = document.getElementById(`increment-qty_${itemId}`);
        minus.disabled = value <= 1;
        plus.disabled = value >= 99;
    }

    // Init
    document.addEventListener("DOMContentLoaded", function () {
        const qtyInputs = document.querySelectorAll('.qty_input');
        qtyInputs.forEach(input => {
            const itemId = input.dataset.item_id;
            handleEnableDisable(itemId);
        });

        // Update form on button clicks
        document.querySelectorAll('.increment-qty').forEach(btn => {
            btn.addEventListener('click', function (e) {
                e.preventDefault();
                const itemId = this.dataset.item_id;
                const input = document.getElementById(`id_qty_${itemId}`);
                input.value = Math.min(99, parseInt(input.value) + 1);
                handleEnableDisable(itemId);
                input.closest('form').submit(); // submit form
            });
        });

        document.querySelectorAll('.decrement-qty').forEach(btn => {
            btn.addEventListener('click', function (e) {
                e.preventDefault();
                const itemId = this.dataset.item_id;
                const input = document.getElementById(`id_qty_${itemId}`);
                input.value = Math.max(1, parseInt(input.value) - 1);
                handleEnableDisable(itemId);
                input.closest('form').submit(); // submit form
            });
        });

        // Manual update
        document.querySelectorAll('.update-link').forEach(link => {
            link.addEventListener('click', function () {
                const form = this.previousElementSibling;
                if (form.classList.contains('update-form')) {
                    form.submit();
                }
            });
        });

        // Remove item
        document.querySelectorAll('.remove-item').forEach(link => {
            link.addEventListener('click', function () {
                const itemId = this.id.split('remove_')[1];
                const csrfToken = "{{ csrf_token }}";
                fetch(`/bag/remove/${itemId}/`, {
                    method: 'POST',
                    headers: { 'X-CSRFToken': csrfToken }
                })
                .then(response => response.ok && location.reload())
                .catch(error => console.error("Remove failed:", error));
            });
        });

        // Back to top
        document.querySelectorAll('.btt-link').forEach(link => {
            link.addEventListener('click', e => {
                window.scrollTo({ top: 0, behavior: 'smooth' });
            });
        });
    });