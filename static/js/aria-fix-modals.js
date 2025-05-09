/*
 Fixes accessibility issue where Bootstrap modals retain focus
 while aria-hidden="true" is applied, which violates WAI-ARIA.
 This script removes aria-hidden and inert attributes when modals are shown,
 and restores them on hide. Includes timeout for proper focus handling.
*/

document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".modal").forEach(modal => {
        // Prevent Bootstrap from setting aria-hidden
        new MutationObserver(mutations => {
            mutations.forEach(mutation => {
                if (mutation.attributeName === "aria-hidden" && modal.getAttribute("aria-hidden") === "true") {
                    modal.removeAttribute("aria-hidden");
                    modal.removeAttribute("inert");
                }
            });
        }).observe(modal, {
            attributes: true
        });

        modal.addEventListener("show.bs.modal", function () {
            this.removeAttribute("aria-hidden");
            this.removeAttribute("inert");
            this.setAttribute("aria-modal", "true");
        });

        modal.addEventListener("shown.bs.modal", function () {
            setTimeout(() => {
                (this.querySelector("button, input, textarea, select, a") || this).focus();
            }, 50);
        });

        modal.addEventListener("hide.bs.modal", function () {
            this.setAttribute("aria-hidden", "true");
            this.setAttribute("inert", "");
        });
    });
});