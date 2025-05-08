document.addEventListener("DOMContentLoaded", function () {
  // === Logout Confirmation ===
  // When "Confirm Logout" button is clicked, submit the hidden logout form
  const confirmLogoutBtn = document.getElementById("confirmLogoutBtn");
  const logoutForm = document.getElementById("logout-form");
  if (confirmLogoutBtn && logoutForm) {
      confirmLogoutBtn.addEventListener("click", function () {
          logoutForm.submit();
      });
  }

  // === Close Mobile Navbar on Outside Click ===
  // Closes the mobile navigation menu if the user clicks outside of it
  const navbarCollapse = document.getElementById("navbarNav");
  const navbarToggler = document.querySelector(".navbar-toggler");
  if (navbarCollapse && navbarToggler) {
      document.addEventListener("click", function (event) {
          const isInside = navbarCollapse.contains(event.target);
          const isToggle = navbarToggler.contains(event.target);
          const isOpen = navbarCollapse.classList.contains("show");

          if (!isInside && !isToggle && isOpen) {
              navbarToggler.click(); // collapse menu
          }
      });
  }

  // === Smooth Scroll and Close Nav on Anchor Click ===
  // Smoothly scrolls to anchor links and closes the mobile nav if open
  const anchorLinks = document.querySelectorAll('.nav-link[href*="#"], .dropdown-item[href*="#"]');
  anchorLinks.forEach(link => {
      link.addEventListener("click", function (e) {
          const href = this.getAttribute("href");
          if (href.includes("#")) {
              const url = new URL(href, window.location.href);
              const samePage = url.pathname === window.location.pathname;
              const anchor = document.getElementById(url.hash.slice(1));

              if (samePage && anchor) {
                  e.preventDefault(); // Prevent default jump
                  anchor.scrollIntoView({ behavior: "smooth", block: "start" });

                  // Close mobile nav if open
                  if (navbarCollapse.classList.contains("show")) {
                      navbarToggler.click();
                  }
              }
          }
      });
  });

  // === Show Contact Success Modal ===
  // If a flag is set in the window object, show the contact confirmation modal
  if (window.showContactModal) {
      const contactModal = new bootstrap.Modal(document.getElementById("contactSuccessModal"));
      contactModal.show();
      setTimeout(() => contactModal.hide(), 2000);
      // Optional: call to server to clear the success flag
      fetch("/clear-success-flag/");
  }

  // === Show Logged Out Modal ===
  // Display a "logged out" confirmation modal for 2 seconds
  if (window.showLogoutModal) {
      const loggedOutModal = new bootstrap.Modal(document.getElementById("loggedOutModal"));
      loggedOutModal.show();
      setTimeout(() => loggedOutModal.hide(), 2000);
  }
});
