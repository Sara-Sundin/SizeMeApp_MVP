document.addEventListener("DOMContentLoaded", function () {
    // Logout confirmation
    const confirmLogoutBtn = document.getElementById("confirmLogoutBtn");
    const logoutForm = document.getElementById("logout-form");
    if (confirmLogoutBtn && logoutForm) {
      confirmLogoutBtn.addEventListener("click", function () {
        logoutForm.submit();
      });
    }
  
    // Close mobile nav
    const navbarCollapse = document.getElementById("navbarNav");
    const navbarToggler = document.querySelector(".navbar-toggler");
    if (navbarCollapse && navbarToggler) {
      document.addEventListener("click", function (event) {
        const isInside = navbarCollapse.contains(event.target);
        const isToggle = navbarToggler.contains(event.target);
        if (!isInside && !isToggle && navbarCollapse.classList.contains("show")) {
          navbarToggler.click();
        }
      });
    }
  
    // Scroll to anchor and close nav
    const anchorLinks = document.querySelectorAll('.nav-link[href*="#"], .dropdown-item[href*="#"]');
    anchorLinks.forEach(link => {
      link.addEventListener("click", function (e) {
        const href = this.getAttribute("href");
        if (href.includes("#")) {
          const url = new URL(href, window.location.href);
          if (url.pathname === window.location.pathname) {
            const anchor = document.getElementById(url.hash.slice(1));
            if (anchor) {
              e.preventDefault();
              anchor.scrollIntoView({ behavior: "smooth", block: "start" });
              if (navbarCollapse.classList.contains("show")) {
                navbarToggler.click();
              }
            }
          }
        }
      });
    });
  
    // Show modals
    if (window.showContactModal) {
      const contactModal = new bootstrap.Modal(document.getElementById("contactSuccessModal"));
      contactModal.show();
      fetch("/clear-success-flag/");
    }
  
    if (window.showLogoutModal) {
      const loggedOutModal = new bootstrap.Modal(document.getElementById("loggedOutModal"));
      loggedOutModal.show();
      setTimeout(() => loggedOutModal.hide(), 2000);
    }
  });
  