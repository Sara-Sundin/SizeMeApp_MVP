# TESTING
- [User Story Testing](#user-story-testing)
- [Lighthouse](#lighthouse)
- [Validation](#validation)
- [Bugs and Fixes](#bugs-and-fixes)

## User Story Testing

### User Story - Simple and Secure Login Process.
As a user, I want a simple and secure login process,
so that I can access my stored measurements and comment on blog posts.

To ensure that the login system is both user-friendly and secure,
the following tests were conducted:

#### Browser used - Google Chrome, Safari, Samsung Internet
- Login Page Accessibility – Verified that the login page is easily accessible from the navigation menu and redirects correctly after authentication.
- Successful Login – Entered valid email and password combinations to confirm users can log in successfully.
- Failed Login Attempts – Tested incorrect credentials to ensure appropriate error messages are displayed.
- Password Reset Functionality – Verified that users can request a password reset, receive an email, and successfully reset their password.
- Session Management – Ensured users remain logged in across different pages and are logged out correctly when requested.
- Keyboard Navigation – Ensured that all form fields, buttons, and links are fully accessible via keyboard.
- User Feedback - Gathered informal feedback from testers to determine if the information provided was clear and sufficient for a smooth onboarding experience.

The feature successfully meets the user story criteria, providing users with a simple, secure, and accessible login experience. 

![Test User Story 1 Desktop](#)
 ![Test User Story 1 Mobile](#)

## Lighthouse
I have recorded the first and final run with Lighthouse for all pages with images and warning messages below. 

### Home Page

#### First run with Lighthouse - Home page

![Lighthouse Home 1st run](documents/images_readme/lighthouse_home_first.jpg)

### Plan Page

#### First run with Lighthouse - Plan page

![Lighthouse Plan 1st run](documents/images_readme/lighthouse_plans_first.jpg)

### Bag Page

#### First run with Lighthouse (Bag page)

![Lighthouse Bag 1st run](documents/images_readme/lighthouse_bag_first.jpg)

Improvement messages: 
- Buttons do not have accessible names.
- Form element do not have associated label.
- Heading elements are not in order.
  
#### Second run with Lighthouse (Bag page) - after fixing the issues.

![Lighthouse Bag 2nd run](documents/images_readme/lighthouse_bag_final.jpg)

### Checkout Page

#### First run with Lighthouse (Checkout page)
Overall Stripe gave me warnings and third party cookies I could not remove so I included one run with Lighthouse where Stripe is disabled.

![Lighthouse Checkout 1st run](documents/images_readme/lighthouse_checkout_first.jpg)

Improvement messages: 
- Stripe inserts aria-hidden = true on card field.
- 14 third party cookies with stripe.
- Country select field missing label.
- Headings not in order.
  
#### Second run with Lighthouse (Checkout page) - after fixing the issues.

![Lighthouse Checkout 2nd run -no stripe](documents/images_readme/lighthouse_checkout_final_no-stripe.jpg)

### Signup Page

#### First run with Lighthouse - Signup page

![Lighthouse Signup 1st run](documents/images_readme/lighthouse_signup_first.jpg)

### Login Page

#### First run with Lighthouse - Login page

![Lighthouse Login 1st run](documents/images_readme/lighthouse_login_first.jpg)

### Dashboard Page

#### First run with Lighthouse - Dashboard page

![Lighthouse Dashboard 1st run](documents/images_readme/lighthouse_dashboard_first.jpg)

### Shop Page

#### First run with Lighthouse - Shop page

![Lighthouse Shop 1st run](documents/images_readme/lighthouse_shop_first.jpg)

### Products Page

#### First run with Lighthouse (Products page)

![Lighthouse Products 1st run](documents/images_readme/lighthouse_shop_products_first.jpg)

Improvement messages: 
- Select sorting field missing label.
  
#### Second run with Lighthouse (Products page) - after fixing the issues.

![Lighthouse Products 2nd run](documents/images_readme/lighthouse_shop_products_final.jpg)

### Product Detail Page

#### First run with Lighthouse (Product Detail page)

![Lighthouse Product Detail 1st run](documents/images_readme/lighthouse_product_detail_first.jpg)

Improvement messages: 
- Buttons do not have accessible names.
- Form element do not have associated label.
- Select element do not have associated label.
- Size mode button in navbar not a list element.
  
#### Second run with Lighthouse (Product Detail page) - after fixing the issues.

![Lighthouse Product Detail 2nd run](documents/images_readme/lighthouse_product_detail_final.jpg)

## Validation

### W3C HTML Validator
I have included screenprints of the first and final validation of the HTML with W3C validation.
<br>

#### Home Page HTML- Initial Check

  ![Validation HTML Home 1st](documents/images_readme/home_html_check_first.jpg)
  
#### Home Page HTML- Final Check

  ![Validation HTML Home Final](documents/images_readme/home_html_check_final.jpg)


#### Plans Page HTML- Initial Check

  ![Validation HTML Plans 1st](documents/images_readme/plans_html_check_first.jpg)

#### Signup Page HTML- Initial Check

  ![Validation HTML Signup 1st](documents/images_readme/signup_html_check_first.jpg)
  
#### Signup Page HTML- Final Check

  ![Validation HTML Signup Final](documents/images_readme/signup_html_check_final.jpg)

#### Login Page HTML- Initial Check

  ![Validation HTML Login 1st](documents/images_readme/login_html_check_first.jpg)

#### Dashboard Page HTML- Initial Check

  ![Validation HTML Dashboard 1st](documents/images_readme/dashboard_html_check_first.jpg)

#### Shop Page HTML- Initial Check

  ![Validation HTML Shop 1st](documents/images_readme/shop_html_check_first.jpg)
  
#### Shop Page HTML- Final Check

  ![Validation HTML Shop Final](documents/images_readme/shop_html_check_final.jpg)

#### Products Page HTML- Initial Check

  ![Validation HTML Products 1st](documents/images_readme/products_html_check_first.jpg)


#### Product Detail Page HTML- Initial Check

  ![Validation HTML Detail 1st](documents/images_readme/product-detail_html_check_first.jpg)
  
#### Product Detail Page HTML- Final Check

  ![Validation HTML Detail Final](documents/images_readme/product-detail_html_check_final.jpg)

### W3C CSS Validator
The CSS was succesfully validated for all pages.

![Screenshot of the CSS Validation](documents/images_readme/w3c-css.jpg)

### JSHint Validator
I have included screenprints of all final validation for each script validated with JSHint.

#### Base.js - JSHint Check

![Base JSHint Final Check](documents/images_readme/base_js_check_JSHint_final.jpg)

#### Accounts - JSHint Check

![Accounts JSHint Final Check](documents/images_readme/accounts_dashboard_js_check_JSHint_final.jpg)

#### Delete Account - JSHint Check

![Delete Account JSHint Final Check](documents/images_readme/delete_account_js_check_JSHint_final.jpg)

#### Mini Cart - JSHint Check

![Mini Cart JSHint Final Check](documents/images_readme/minicart_js_check_JSHint_final.jpg)

#### Products - JSHint Check

![Products JSHint Final Check](documents/images_readme/products_js_check_JSHint_final.jpg)

#### Shopping Bag - JSHint Check

![Bag JSHint Final Check](documents/images_readme/scripts_bag_js_check_JSHint_final.jpg)

#### Checkout Stripe - JSHint Check

![Stripe JSHint Final Check](documents/images_readme/stripe_elements_js_check_JSHint_final.jpg)

#### Toggle Password - JSHint Check

![Toggle JSHint Final Check](documents/images_readme/toggle_password_js_check_JSHint_final.jpg)

### CI Python Linter
The CI Python Linter helps ensure that our code is clean, maintainable, and error-free, improving the overall development workflow and reducing potential bugs before deployment.

It implements:
- Automatic Code Checks – The linter runs automatically when code is pushed to the repository.
- PEP 8 Compliance – Ensures that the code follows Python’s official style guide.
- Error & Warning Detection – Identifies syntax errors, unused imports, and other common issues.
- Consistent Formatting – Helps enforce standard formatting, reducing unnecessary code style variations.

Tools used:
- Flake8 – Checks for syntax errors, style violations, and undefined variables.
- Black – Automatically formats code to follow best practices.
- Pylint – Provides detailed code analysis and improvement suggestions.

I ran all my Python code through the Python Linter with the following results. The final check for all code files were without errors. For more images tested on all apps see the [Read Me Images](documents/images_readme) folder.

### Account App
#### Account forms.py- Initial Check
![Validation CI Python Linter First Check](documents/images_readme/accounts_forms_linting_test_first.jpg)

#### Account forms.py- Final Check
![Validation CI Python Linter Final Check](documents/images_readme/accounts_forms_linting_test_final.jpg)

## Bugs and Fixes
Here I have recorded some issues that I spent excessive time solving with the solutions indicated below.

### Bug: Multiple Modals Opened Simultaneously on ***product_detail*** Page

![Bug Modals](documents/images_readme/bug-modals.jpg)

#### Description
When visiting the ***product_detail*** page, multiple Bootstrap modals (update size mode modal and prototype info modal) were opening at the same time when opening one or the other.

#### Root Cause
The bug was caused by multiple window.onload assignments in the postloadjs block of the template. Each modal trigger script defined its own window.onload function, which overwrote the others and led to unpredictable behavior where more than one modal could appear.

#### Resolution
The solution involved consolidating modal logic into a single window.onload function and using {% if %} / {% elif %}` logic to ensure only one modal is triggered based on context flags passed from the view.

### Bug: AWS Storage Misconfigured

#### Description  
During setup of image uploads to Amazon S3, images were not being uploading at all, just the link to the bucket was cofigured.

#### Root Cause  
The problem was caused by the deprecation of the DEFAULT_FILE_STORAGE settings in versions Django 4.2 and newer. After this Django introduced the STORAGES setting for configuring storage backends. Continuing to use the old format led to Django falling back to default file storage or silently failing to connect to the S3 bucket.

#### Resolution  
The settings were updated to the new STORAGES format as recommended in the Django documentation:

![Bug AWS Storage](documents/images_readme/bug-storages.jpg)

### Bug: Checkout Fields Not Saving to CustomUser When "Save Info" Box Was Checked

![Bug Save Info](documents/images_readme/bug-save_info.jpg)

#### Description  
After adding new fields (e.g. phone_number, address, city, postcode, country) to the CustomUser model, the checkout form did not save the details when the user checked the “Save this information for next time” box. The form submitted successfully, but the saved values were not persisted to the user profile.

#### Root Cause  
The checkout logic was originally designed for a default OrderProfile model. After extending CustomUser, the code handling the "save_info" flag was not updated to write to the corresponding fields in the custom user model. As a result, the posted data was ignored.

#### Resolution  
Updated the checkout view logic in checkout/views.py to correctly reference and save the new fields to the request.user instance when save_info is set to True.

### Bug: `RecursionError` When Adding a Plan to the Bag

![Bug Recursion](documents/images_readme/bug-error.jpg)

#### Description  
When a user attempted to add a Plan to the shopping bag, the app crashed with a RecursionError: maximum recursion depth exceeded. This occurred during rendering of the plan_detail page after the item was added to the bag.

#### Root Cause  
The error was caused by circular logic between the plan_detail view, the bag system, and the page rendering. A template tag {% url 'plan_detail' plan.id %} was triggering the view recursively during template evaluation.

#### Resolution  
The bug was resolved by identifying and removing the recursive call chain. This involved:
- Reviewing all template tags and context variables that pointed to plan_detail.
- Ensuring that redirects, reverse(), or includes did not re-invoke the view.
- Refactoring plan_detail to avoid loading templates or partials that included self-referential links.

[Back to Content Table](#content)