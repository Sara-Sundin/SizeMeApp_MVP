### Project 4

# SizeMeApp_MVP

[View project on Heroku](https://sizemeapp-mvp-f444c8498547.herokuapp.com/) 

## Introduction 

### Welcome to SizeMeApp - your smart sizing solution built for businesses.
This website is targeted to businesses with help to offer brands a better shopping experience by recommending the right size for each customer based on their body measurements. This reduces returns, boosts customer satisfaction, and supports a more sustainable future. On this site, brands can explore how the tool works, test it directly in the prototype webshop, and buy a plan that fits their needs. Try it out, experience the technology in action, and see how SizeMeApp can transform the online shopping experience - for your customers and for your brand.

![Screenshot of the website on multi devices](documents/images_readme/multiscreen.jpg)

# CONTENT

[DATABASE OVERVIEW](#database-overview)
- Database ERD Schema

[USER EXPERIENCE (UX)](#user-experience)
- The website across UX planes
- User Stories
- Accessibility

[VISUAL DESIGN IDENTITY](#visual-design-identity)
- Colour Scheme
- Typography
- Imagery
- Wire Frames
- Features
- Admin Dashboard

[TECHNOLOGIES USED](#technologies-used)
- Languages used to create the website
- Frameworks & Libraries
- Software
- Automated Tools
- AI

[DEPLOYMENT](#deployment)
- Heroku with Github Integration

[TESTING.md](TESTING.md)
- Manual vs. Automated Testing
- Manual Testing
- Devices
- Browsers
- User Story Testing
- Testing Grid
- Automated Testing
- Chrome Dev Tools
- Lighthouse
- Validators
- Webhooks
- Testing with Django
- Testing Code Coverage
- Bugs & Fixes

[REFERENCES](#references)

[CREDITS](#credits)

[PERSONAL NOTES](#personal-notes)

[ACKNOWLEDGMENTS](#acknowledgments)

<br>
<br>
<hr>
<hr>

## Database Overview

The database schema for **SizeMeApp** is designed to efficiently manage user data, product information, subscription plans, and personalized garment fit logic. It ensures clear relationships between users, their orders, and the garments they interact with - providing a scalable foundation for accurate size recommendations and seamless order processing.

The database ERD Schema consists of seven main tables:

**CustomUser**  
Stores user details including full name, email, measurements (chest, waist, hips, shoulders), delivery address, and role-related flags like admin status.

**Order**  
Captures all essential order details such as user, contact info, totals, Stripe payment ID, and timestamp.

**OrderLineItem**  
Connects plans to an order, allowing quantity and pricing to be tracked per item.

**Plan**  
Represents the subscription options available in the prototype (e.g., Starter, Growth, Enterprise), each with pricing and descriptions.

**Product**  
Holds details about garments in the webshop, such as name, category, price, size options, and images.

**Category**  
Groups products into categories like t-shirts, shirts, and sweatshirts, supporting filtering and navigation in the shop. Also stores the stretch_factor used to determine the recommendations.

**GarmentFit**  
Links each product to its size measurements (e.g., chest in cm), stretch factor, and size label - essential for generating accurate fit recommendations.

The schema is designed to support both end-user experiences (shopping and fitting) and admin workflows (managing products, plans, and user data). It provides a modular and extendable setup for integrating personalized sizing logic at scale.

## Database ERD Schema

![Database ERD Schema](documents/images_readme/database_erd_schema_4.jpg)

[Back to Content Table](#content)

<hr>
<hr>

# USER EXPERIENCE
- [UX Planes](#the-website-across-ux-planes)
- [User Stories](#user-stories)
- [Accessibility](#accessibility)
- [Aria Labels](#aria-labels-used)

## The Website Across UX Planes

### Strategy Plane
The primary goal of the SizeMeApp website is to introduce businesses to the benefits of implementing personalized size recommendations while allowing users to experience the app in action through a live prototype webshop. 

The target audience includes:

- E-commerce brands and retailers looking to reduce returns and increase conversion rates.
- Business owners seeking innovative sizing solutions.
- Users who want to explore and understand how the SizeMeApp technology works.

The website meets user and business needs by:

- Clearly explaining how SizeMeApp works.
- Demonstrating the app through an interactive webshop prototype.
- Guiding businesses toward making contact for partnership inquiries.
- Offering clear, accessible, and action-driven navigation.

### Scope Plane
The website features are carefully selected to support the project's goals:

- A homepage introducing SizeMeApp’s value proposition for businesses.
- A clear "Plans" section presenting subscription options for companies.
- A user dashboard for managing measurements and profile data.
- A prototype webshop where users can try the sizing recommendation tool.
- Contact form in footer to encourage business leads.

Future improvements include testimonials, client success stories, and additional case studies once the product moves into broader implementation.

### Structure Plane
The structure ensures an intuitive and business-focused flow:

- The homepage introduces the app and invites visitors to try it.
- A prominent link to the prototype webshop encourages exploration.
- The dashboard allows users to input and update their measurements for live sizing demos.
- Plan options are neatly organized, offering pricing tiers for businesses.
- Contact options are clearly placed in the footer throughout the site.

First-time visitors, businesses, and returning users can easily find relevant information with minimal friction.

### Skeleton Plane
The layout focuses on simplicity, clarity, and user engagement:

- A clean, fixed navbar offers easy access to all key areas (Shop, Plans, Dashboard, Contact).
- Strategic CTAs ("View Plans," "Contact Us," "Enter Application") lead users forward.
- Interactive size recommendation features appear naturally within the webshop.
- All forms are straightforward, responsive, and user-friendly.

This skeleton ensures the entire journey feels modern, direct, and efficient.

### Surface Plane
The visual design supports credibility, innovation, and action:

- A neutral background with bright, energetic accent colors draws attention to CTAs.
- Clear, modern typography ensures easy readability.
- Hover effects on buttons and links enhance interactivity without being distracting.
- The SizeMeApp logo, spinning animation at checkout, and subtle transitions maintain a tech-driven but accessible feel.
- Responsive design guarantees an optimal experience on all devices.

Together, these visual elements ensure the website builds trust, engages businesses, and smoothly guides users toward experiencing and partnering with SizeMeApp.

[Back to Content Table](#content)

# USER STORIES

The development of the SizeMeApp website follows a structured user story framework to ensure every feature is built with clear objectives, measurable success criteria, and actionable development steps.

The site adheres to CRUD (Create, Read, Update, Delete) principles to manage user data, measurement updates, plan selections, and interactions within the prototype webshop efficiently.

## Kanban Board
Full user stories and progress tracking are available on the **SizeMeApp-MVP Kanban Board**:  
[View the Kanban Board](https://github.com/users/Sara-Sundin/projects/12). 

I used a Kanban board to organize tasks and prioritize development. By labeling features as Must-Have, Should-Have, Could-Have, and Wont-Have, I ensured a clear focus on essential components like user authentication, the dashboard, and measurement integration, while identifying non-critical elements for future development. This visual management tool helped me break down tasks into To Do, In Progress, and Completed, ensuring a clear overview of each design and development stage. I made sure all tasks required for the project were completed, while leaving some for future enhancements.

![The Kanban Board in progress](documents/images_readme/kanban-board-inprogress-ms4.jpg)

## Example of User Story Implementation

### User Story:
As a registered user, I want to update my measurements, so that I can receive accurate size recommendations as my body changes.

### Acceptance Criteria:
- Users can edit and save new measurements at any time.
- Changes are securely saved and reflected in the sizing recommendations.

### Tasks:
- Build an "Update Measurements" modal on both dashboard and webshop.
- Ensure user data is updated and old values overwritten.
- Provide confirmation modals upon successful update.

By following this approach, the website maintains a user-centered, business-focused experience while ensuring technical clarity and efficiency.

## Visitor Categories

The user stories are structured into three main visitor types:

### New Visitors (Business or Shopper First-Time Users)

New visitors primarily browse to understand the purpose and benefits of SizeMeApp:

- They want to quickly understand what SizeMeApp offers and how it works.
- Clear CTAs ("View Plans," "Try Prototype") guide businesses and shoppers to explore.
- Businesses learn how the solution reduces returns and increases conversion rates.
- A prototype webshop lets visitors experience the size recommendation flow directly.
- The "Plans" section offers tailored subscription options for businesses.

**CRUD in Action:**  
Create (contact forms), Read (plan details, webshop exploration).

### Returning Users (Registered Users)

Returning users can interact more deeply with the application:

- Registered users can manage and update their measurements.
- They receive live size recommendations within the prototype webshop.
- Business users can revisit plan information or request partnership discussions.
- A seamless login process grants access to stored data.

**CRUD in Action:**  
Create (measurements), Read (recommendations), Update and Delete (user profile and measurements).

### Frequent Visitors (Engaged Business Prospects)

Frequent users or businesses continue refining their engagement:

- Shoppers update measurements to maintain accurate size recommendations.
- Businesses monitor updates and review pricing plans for larger scale integration.
- Future: Businesses receive newsletters about updates or added features.

**CRUD in Action:**  
Read (plans, updates), Update and Delete (profile, subscription interests).

## Additional CRUD Features

To ensure full CRUD implementation across the platform:

- Admins can manage (create, read, update, delete) products and subscription plans directly in the admin panel. This includes setting prices, descriptions, images, and display order.
- Registered users can update or delete their profile information, including personal data and body measurements, via the dashboard.
- Orders are created at checkout and can be reviewed by users (if logged in), while admin staff can manage order records through the admin interface.

# ACCESSIBILITY

SizeMeApp has been developed with accessibility as a core priority. Key measures include:

- **Semantic Elements:** Proper use of `<header>`, `<main>`, `<footer>` for clear structure.
- **Descriptive Headings:** Logical use of `<h1>`, `<h2>`, `<h3>` for screen reader navigation.
- **Alt Attributes:** Every important image includes meaningful alt text.
- **Keyboard Navigation:** All menus, buttons, and forms are fully accessible via keyboard.
- **High Contrast Design:** Colors are chosen to meet WCAG contrast guidelines.
- **Responsive Layout:** Ensures usability across desktops, tablets, and smartphones.
- **Viewport Meta Tag:** Optimizes mobile scaling and accessibility.
- **Form Labels and ARIA:** All forms use `<label>` tags and aria-labels where necessary.
- **Readable Fonts:** Fonts such as "Raleway" are chosen for clarity and accessibility.
- **Text Scalability:** Text enlarges properly without loss of structure.
- **Accessibility Testing:** Lighthouse audits and Django accessibility checks were performed regularly.

[Back to Content Table](#content)

<br>
<br>
<hr>
<hr>
<br>
<br>

# VISUAL DESIGN IDENTITY
- [Colour Scheme](#colour-scheme)
- [Typography](#typography)
- [Imagery](#imagery)
- [Wire Frames](#wire-frames)
- [Features](#features)
- [Admin Dashboard](#admin-dashboard)

## Colour Scheme
The color scheme is carefully chosen to create a clean, modern, and user-friendly interface. It consists of five key colors:

#000000 (Black) - Used as a secondary background color as well as navbar and footer. Black gives the site depth and contrast. It helps frame content areas and contributes to a bold, modern aesthetic, especially when paired with bright accent colors.

#FFFFFF (White) - The primary background color, white creates a clean and spacious foundation. It enhances readability and provides a neutral base that allows interactive elements to stand out.

#94E6ED (Soft Aqua) - This fresh, tech-inspired tone is used on CTA buttons to convey lightness and innovation. It's typically assigned to secondary actions or plans and adds a sense of clarity and modernity.

#F8B133 (Warm Orange) - A vibrant and energetic color used on CTAs for primary or featured actions. It draws attention effectively and signals engagement points such as signups or purchasing a plan.

#C3B3D6 (Lavender Grey) - A soft, sophisticated accent that differentiates specific plans or informational CTAs. It introduces a calm, balanced note and helps visually separate alternative options without overpowering the layout.
<br>

![Colour Scheme](documents/images_readme/colorscheme_4.jpg)

<hr>

## Typography
The chosen typography for SizeMeApp consists of Poppins for headings and Raleway for body text. Both are Google Fonts, carefully selected to balance a modern, professional aesthetic with optimal readability. This pairing enhances the user experience by ensuring a structured yet approachable interface that aligns with SizeMeApp’s goal of providing accuracy and ease in online shopping.

![Fonts](documents/images_readme/fonts_4.jpg)

### Poppins 
Poppins brings a clean, contemporary, and professional feel to the site. Its bold yet minimal design ensures clear hierarchy, making key sections such as headings, navigation, and CTAs stand out effectively.

### Raleway 
Raleway is a lightweight, elegant sans-serif font designed for readability. Its subtle letter spacing and refined structure make it ideal for body text, ensuring smooth reading and a user-friendly experience. This complements the bold presence of Poppins, providing a well-balanced visual hierarchy.

<hr>

## Imagery
SizeMeApp uses an AI-generated human body illustration at the home page as a clean and inclusive background. Throughout the site, icons are used as contextual images to support navigation and user actions. The visual style is minimal, functional, and intentionally neutral to keep focus on usability and personal fit. For the avatar in the profile I have used images from vecteezy.com that I stylized using the colorscheme from the site.

<hr>

## Wire Frames
The wireframes were designed in Adobe Illustrator, covering mobile, tablet, and desktop layouts to ensure a fully responsive experience. I developed and applied my own custom wireframing toolkit throughout the process, which helped maintain consistency and efficiency. The final website closely reflects the original wireframe concept, demonstrating a smooth transition from design to implementation.

<details open>
  <summary>Wireframes Home, Plans & Dashboard Page</summary>

  ![Wireframes Home Pages](documents/images_readme/wireframes_home_plans_dashboard.jpg)
</details>

 <details open>
  <summary>Webshop Pages</summary>

  ![Wireframes Webshop Pages](documents/images_readme/wireframes_webshop_pages.jpg)
</details>

[Back to Content Table](#content)

<hr>

## Features

### All pages

#### Favicon
The favicon for SizeMeApp features a minimalist three-ring design, symbolizing balance, precision, and connection - key elements in finding the perfect fit when shopping online. The central, bold ring represents the core function of the app: accurate sizing, while the two smaller rings above and below convey adaptability and seamless user experience.

This clean, geometric icon was designed to be simple yet recognizable, ensuring strong brand identity even at small sizes. The favicon enhances the visual consistency of the platform, aligning with the app’s modern and functional design.

 ![Favicon](documents/images_readme/favicon_rings_32x32.png)

#### Default Navigation Bar
The navigation bar in SizeMeApp is designed for easy access to key features while maintaining a clean and modern look. It provides clear navigation to sections such as Plans, Account, Contact, Cart and Prototype, ensuring users can quickly find what they need.

The navbar also includes a Dashboard link for managing stored measurements, an Order History link and a Logout option for seamless account control.

The design ensures a consistent user experience, adapting for different screen sizes with a responsive mobile-friendly layout with a toggle. 

![Default Navigation Desktop](documents/images_readme/navbar-desktop.jpg)
![Default Navigation Mobile](documents/images_readme/navbar-mobile.jpg)

#### Webshop Navigation Bar
This custom webshop navbar enhances the user experience by blending standard navigation with category filtering. Positioned below the main navbar, the category buttons allow users to instantly filter by T-shirts, Shirts, or Sweatshirts. The top navigation includes dynamic elements like size mode toggle, shopping cart total, account controls, and a plans dropdown, making it both functional and focused on the SizeMeApp journey.

![Webshop Navigation Tablet](documents/images_readme/navbar-webshop-tablet.jpg)
![Webshop Navigation Mobile](documents/images_readme/navbar-webshop-mobile.jpg)

#### Footer
The footer serves as a consistent end point for the site, offering both interaction and contact information. It is divided into a responsive two-column layout, one for the contact form and one for business details and social media. With crisp styling and clear calls to action, it reinforces brand trust and user engagement. At the bottom there is a copyright block, always present if the contact form and details are removed from any page.

![Footer Desktop](documents/images_readme/footer-desktop.jpg)

### Contact Form Section
The contact form in the footer invites users to send messages directly through the site. It uses Django’s crispy forms for clean, accessible styling and includes CSRF protection. The form is simple and intuitive, encouraging outreach without overwhelming the user, making support feel approachable and integrated.

### Contact Details & Social Icons Section
This section provides essential company information including email, phone number, and physical address. Icons enhance scannability, and clickable links ensure easy access. Social media icons link to external platforms in new tabs, allowing users to connect professionally and casually without leaving the site.

![Footer Mobile](documents/images_readme/footer-mobile.jpg)

### Home Page

#### Hero Section
With a clean headline and two clear call-to-action buttons, the hero section guides users to try the tool or explore plans. The layout adapts across screen sizes, ensuring usability and visual impact on all devices. The background features a transparent man overlaid with a measurement grid, symbolizing the core idea behind SizeMeApp: precision. This visual reinforces the app’s purpose-to help users find their perfect fit when shopping online. 

![Hero Section Desktop](documents/images_readme/hero-section-desktop.jpg)
![Hero Section Tablet](documents/images_readme/hero-section-tablet.jpg)
![Hero Section Mobile](documents/images_readme/hero-section-mobile.jpg)

#### Info Section
The info section highlights the core value of SizeMeApp: reducing returns and increasing customer confidence through accurate sizing. It introduces the benefits of profile-based recommendations, emphasizing improved conversion rates and loyalty. With a clear three-step guide - sign up, enter measurements, and explore. Users are encouraged to take immediate action through a bold, centered CTA button.

![Info Section Tablet](documents/images_readme/info-section-tablet.jpg)
![Info Section Mobile](documents/images_readme/info-section-mobile.jpg)

#### Business Plans Section
The Business Plan section presents SizeMeApp’s flexible pricing tailored to different business sizes. It introduces three scalable options - Starter, Growth, and Enterprise, each designed to support user needs from basic to advanced. With clean icons, clear pricing, and feature lists, the section guides brands to choose a plan that aligns with their growth stage, boosting efficiency, fit accuracy, and customer satisfaction.

![Plans Section Desktop](documents/images_readme/plan-section-desktop.jpg)
![Plans Section Mobile](documents/images_readme/plan-section-mobile.jpg)

### Plan Detail Page

### Plan Detail
The Plan Detail section highlights a single business plan based on user focus. It dynamically renders the selected plan type in full width, ensuring maximum visibility. By conditionally including a detailed plan card, the section provides targeted content that adapts to user interest. This clean and focused layout helps businesses easily compare offerings and make informed decisions about the most suitable subscription.

![Plan Detail Desktop](documents/images_readme/plan-detail-desktop.jpg)
![Plan Detail Mobile](documents/images_readme/plan-detail-mobile.jpg)

### CTA button and small Plan Cards
This section encourages user engagement with a clear call-to-action button - guiding users to the webshop. Below, it displays all alternative plans as smaller cards, providing a quick visual comparison of what's available beyond the selected focus.

![Plan Small Card Desktop](documents/images_readme/small-plan-cards-desktop.jpg)
![Plan Small Card Mobile](documents/images_readme/small-plan-cards-mobile.jpg)

### Checkout

#### Shopping Bag
The shopping bag page summarizes selected plans, showing setup fees, monthly costs, and quantities in both mobile and desktop views. Users can update quantities, review totals, and proceed to checkout. It adapts responsively and offers quick access back to the plan selection section.

![Shopping Bag Desktop](documents/images_readme/bag-desktop.jpg)
![Shopping Bag Desktop](documents/images_readme/bag-mobile.jpg)

#### Minicart
The mini cart offers users a quick overview of their selected items without leaving the current page. Triggered when adding a product, it slides in with a smooth animation, showing quantity, price, and a direct link to checkout-streamlining the shopping flow and improving UX.

![Minicart](documents/images_readme/minicart-desktop.jpg)

#### Checkout Details
The checkout details section provides a clear summary of your selected plans, including each item's name, description, setup cost, monthly fee, quantity, and subtotal. A final total is shown at the bottom, along with a note that monthly billing begins after the initial setup payment.

![Checkout Details Desktop](documents/images_readme/checkout-details-desktop.jpg)
![Checkout Details Mobile](documents/images_readme/checkout-details-mobile.jpg)

#### Checkout Form
The checkout form collects customer and delivery details needed to complete the order. It includes fields for name, email, phone number, and address, and offers a toggle for saving the delivery info to the user’s profile if logged in. All fields are styled with Crispy Forms for consistency.

![Checkout Form Desktop](documents/images_readme/checkout-form-desktop.jpg)
![Checkout Form Mobile](documents/images_readme/checkout-form-mobile.jpg)

#### Checkout Payment
This section of the checkout form integrates Stripe for secure payment processing. It displays a styled card input field, handles errors in real-time, and includes the client_secret needed for confirming the payment. A "Back to Bag" link and a “Complete Order” button finalize the user’s purchase.

![Checkout Payment Tablet](documents/images_readme/checkout-payment-tablet.jpg)
![Checkout Payment Mobile](documents/images_readme/checkout-payment-mobile.jpg)

#### Spinner Overlay
The loading overlay displays a custom spinner animation with the SizeMeApp logo while the Stripe payment is processing. It's initially hidden with the d-none class and becomes visible during form submission to indicate to users that their order is being handled securely and smoothly.

![Spinner](documents/images_readme/loading-spinner.jpg)

#### Order Confirmation
The order confirmation page presents a complete summary of the user’s purchase, including the order number, date, itemized product details with costs, and delivery address. It also lists billing information and the grand total. A confirmation email is automatically sent to the customer for reference.

![Order Confirmation](documents/images_readme/order-confirmation-desktop.jpg)

### Account

#### Signup Form
The sign-up form offers a quick and secure registration process, collecting essential details like name, email, and password. There are placeholders with text for guidance and a password toggle for visibility control.  After signing up, users are automatically redirected to the dashboard, ensuring a seamless onboarding experience. 

![Signup Form Desktop](documents/images_readme/signup-desktop.jpg)
![Signup Form Mobile](documents/images_readme/signup-mobile.jpg)

#### Login Form
The login form offers a user-friendly experience with placeholder text for guidance and a password toggle for visibility control. A "Forgot your password?" link provides easy recovery. After logging in, "Logged in as [Username]" text appear in the navigation bar, enhancing personalization and usability. 

![Login Form Desktop](documents/images_readme/login-desktop.jpg)
![Login Form Mobile](documents/images_readme/login-mobile.jpg)

#### Reset Password Form
The reset password form allows users to securely recover their account by entering their email. After submitting, a confirmation message appears, informing them that a reset link has been sent. This ensures a smooth and secure process, allowing users to regain access to their accounts effortlessly. 

![Reset Password Mobile](documents/images_readme/reset-password-mobile.jpg)

![Done Reset Desktop](documents/images_readme/reset-password-done-mobile.jpg)

![Confirm Reset Desktop](documents/images_readme/reset-password-confirm-tablet.jpg)

![Complete Reset Desktop](documents/images_readme/reset-password-complete-desktop.jpg)

### Dashboard
The dashboard offers users a personalized space to manage their profile, measurements, and access the webshop. With a welcoming header, avatar display, and editable user info, it encourages regular updates and engagement. Two clear steps guide users: first to add or update measurements, and second to explore the SizeMeApp prototype. It's a clean, intuitive interface for onboarding and account maintenance.

If the user just signed up or has not entered their measurements when visiting the dashboard it triggers a modal to do so. This acts as a call to enter the measurements to get the full experience of SizeMeApp. The user can either skip to engage for now or close the modal. If skipping or entering the measurements the user gets redirected to a welcome modal where the user can choose between checking out the plan subscriptions or entering the SizeMeApp application.

![Enter Measurements Modal](documents/images_readme/enter-dashboard-modal-mobile.jpg)

Redirects to:

![Welcome Modal](documents/images_readme/welcome-modal-tablet.jpg)

#### Features of the Dashboard
Profile Section:
- Displays avatar (or placeholder) and user info (name, email).
- Includes a link to open the Change Avatar modal.
- Update Profile Button: prominent button for updating user profile details, opens the #profileModal.

Instructional Columns:
Column 1 - Measurements:
- Explains the importance of entering measurements.
- Includes a button to open the #measurementModal.
Column 2 - Webshop Access
- Guides the user to test the application in a live prototype webshop.
- Encourages to try the size mode button in the webshop.

![Dashboard Desktop](documents/images_readme/dashboard-desktop.jpg)
![Dashboard Mobile](documents/images_readme/dashboard-mobile.jpg)

#### Change Avatar Modal
The avatar modal lets users personalize their profile by choosing from pre-designed avatars based on star signs. Each avatar is color-matched to the site's palette, presented in a responsive grid. Selecting one updates the profile instantly, adding a cosmic, user-centered touch.

![Avatar Modal Desktop](documents/images_readme/avatar-desktop.jpg)
![Avatar Modal Mobile](documents/images_readme/avatar-mobile.jpg)

#### Update Profile Modal

![Profile Modal Desktop](documents/images_readme/profile-modal-desktop.jpg)
![Profile Modal Mobile](documents/images_readme/profile-modal-mobile.jpg)

#### Delete Account Modal
If the user decides to delete their account in the profile account modal, a confirmation modal appears to avoid deleting the account by mistake.

![Delete Account Modal Desktop](documents/images_readme/delete-account-modal-desktop.jpg)

#### Delete Account Success Modal
If the user deletes their account a success modal appears with a personal touch and a create new account button in case the user changed their mind.

![Delete Account Success Modal Mobile](documents/images_readme/delete-account-modal-confirm-mobile.jpg)

#### Update Measurements Modal
At the first column the button to update the measurements opens a measurements modal.

![Measurement Modal](documents/images_readme/update-measurements-modal-mobile.jpg)

#### Delete Measurements Modal
If the user decides to delete their measurements a confirmation modal appears to avoid deleting the measurements by mistake.

![Delete Measurement Modal](documents/images_readme/delete-measurements-modal-mobile.jpg)

### Order History
The Order History is accessed via the submenu under the link Accounts in the navbar when user is logged in. The Order History page gives users a clear overview of all past purchases, including order numbers, dates, totals, and access to full details. The table is responsive for all devices, making it easy to track transactions. If no orders have been placed, a friendly message lets users know their history is currently empty.

![Order History Desktop](documents/images_readme/order-history-desktop.jpg)
![Order History Mobile](documents/images_readme/order-history-mobile.jpg)

#### Order Detail
The Order Detail page provides a clear breakdown of a specific purchase, displaying order number, date, total cost, and all included items. Each plan is listed with quantity and, if available, a visual icon to reinforce recognition. The layout is mobile-friendly, with two responsive columns for order info and itemized content.

![Order Detail Desktop](documents/images_readme/order-details-desktop.jpg)
![Order Detail Mobile](documents/images_readme/order-details-mobile.jpg)

#### Logout Confirm Message
The logout link allows users to securely sign out from their account. Clicking it opens a modal with the message "Are you sure you want to sign out?", ensuring intentional logouts. This prevents accidental logouts and provides a seamless user experience. 

![Logout Modal](documents/images_readme/logout-modal-desktop.jpg)

### Prototype Pages - Webshop
The webshop serves as a prototype tool for testing SizeMeApp’s sizing functionality. Users can view products, input body measurements, and receive personalized size recommendations. It simulates a real shopping experience to validate how accurate fit data can reduce returns and improve confidence without completing actual purchases.

#### Entry Page - Webshop
The entry page introduces users to the SizeMeApp prototype webshop. With a clean hero section and welcoming message, it invites visitors to experience the sizing tool in action. The page explains the purpose - trying out real-time fit suggestions-and encourages exploration through a clear call-to-action. It's the starting point for testing how sizing insights can transform online shopping.

![Home Webshop Page Desktop](documents/images_readme/webshop-home-desktop.jpg)
![Home Webshop Page Mobile](documents/images_readme/webshop-home-mobile.jpg)

#### Products Page
The product listing in the prototype webshop blends dynamic functionality with clean design to enhance the sizing experience. Users can filter by category, sort products, and see real-time search results. Each product card features a category badge, image, price, and name, all clickable for more details. Sort and search controls adjust the grid in real time, helping users find the right fit faster with SizeMeApp.

![Products Desktop](documents/images_readme/products-desktop.jpg)
![Products Mobile](documents/images_readme/products-mobile.jpg)

#### Product Detail
This product detail page in the SizeMeApp prototype webshop combines visual clarity with smart sizing. On the left, users see the product image and category badge. On the right, a split layout shows the product description and a form for selecting size and quantity. If size mode is active, personalized fit recommendations appear based on the user’s measurements, with quick access to update them. A modal-based “Add to Cart” button highlights the prototype nature of the tool while preserving real shopping flow.

![Product Detail Desktop](documents/images_readme/product-detail-desktop.jpg)
![Product Detail Tablet](documents/images_readme/product-detail-tablet.jpg)
![Product Detail Mobile](documents/images_readme/product-detail-mobile.jpg)

#### Update Measurement Modal in Product Detail
The Update Measurements modal on the product detail page allows users to enter their body measurements - chest, waist, hips, and shoulders for more accurate size recommendations. It supports the Size Mode feature and enhances the fit-matching experience in the webshop.

![Modal Measurements Product Detail](documents/images_readme/measurements-webshop-mobile.jpg)

#### Checkout Button Modal
The Prototype Info Modal appears when users click the "Add to Cart" button on product pages. It informs them that the webshop is a demo created to showcase the SizeMeApp experience. The modal offers clear next steps: contact us, explore subscription plans, or simply continue browsing.

![Modal Checkout Button](documents/images_readme/modal-checkout-webshop-desktop.jpg)

### Success Modals
Instead of using Django’s default success messages, I chose to implement custom modals for successful actions like updates and submissions. This approach fits the clean and immersive UI/UX of the site better, providing focused, non-intrusive feedback. All modals are designed to auto-dismiss after a timeout-short for minor actions and slightly longer for key user interactions - ensuring clarity without interrupting the flow.

The success modals consists of three different styling options, a basic black and white modal for actions such as changing or deleting measurements and profile, a darker modal for the size mode and a basic white with black text for logging out and contact success modals.

#### Update and Delete Measurements and Profile Success Modals
The measurement and profile update modals provide instant visual feedback when users save new data. Instead of using message banners, these modals confirm actions like adding or editing measurements or profile info. They're styled to match the interface and auto-dismiss after a short delay.

![Profile Success](documents/images_readme/success-modals-desktop.jpg)

#### Size Mode Success Modals
The size mode toggle lets users switch between standard browsing and personalized size recommendations. Entering or exiting triggers a brief success modal, confirming the change. These modals enhance clarity and user feedback while keeping the experience smooth and focused.

![Size Mode Success](documents/images_readme/exit-size-mode-desktop.jpg)

#### Logout and Contact Success Modals
The contact and logout success modals provide brief, friendly confirmation messages after form submission or logging out. They help reassure users that their actions were successful. Both are styled consistently with the app's UI and are set to auto-dismiss after a short delay.

![Logout and Contact Success](documents/images_readme/contact-success-modal.jpg)

### 404 Page
The custom 404 page provides a simple, branded experience for users who land on a broken or incorrect URL. Featuring the SizeMeApp logo and a friendly message, it clearly communicates that the page doesn’t exist and offers a prominent call-to-action to return home, keeping users engaged in the flow.

![404 Page](documents/images_readme/404.jpg)

## Future Features

### Allauth and Social Media Login
In future development, we will implement Django Allauth to enable social media and Google login, allowing users to authenticate seamlessly with existing accounts. This improves user experience by simplifying registration and reducing password fatigue. Allauth also offers robust account management, email verification, and support for multiple authentication providers, making it a scalable and secure solution for future needs.

### Measurement Sync via Camera or 3D Scan
To enhance accuracy and convenience, future versions of SizeMeApp may include integration with smartphone cameras or 3D scanning tools. This would allow users to scan their bodies and generate precise measurements without manual input. Such a feature improves fit accuracy, removes user guesswork, and adds a layer of tech-forward innovation that supports better shopping experiences across devices.

### Subscription Plan Management Dashboard
A dedicated dashboard will allow users to easily manage their SizeMeApp subscription plans. Features may include the ability to upgrade or downgrade plans, pause billing, view usage insights, and receive tailored plan suggestions based on activity. This adds transparency, flexibility, and control for users, improving customer retention and encouraging ongoing engagement with the platform.

### Feedback on Fit Accuracy
After a user receives and tries on a garment, the app will prompt them to provide feedback on how well the suggested size fit. This data helps continuously train and refine the fit algorithm, making future recommendations more precise. It also helps identify inconsistencies in product sizing from different brands, building a smarter and more reliable fit recommendation system over time.

## Admin Dashboard
I customized the Django admin dashboard using Jazzmin to enhance usability and align it with the visual identity of the project. The modern interface makes navigation cleaner and more intuitive, especially for non-technical users. In the product admin, I implemented drag-and-drop sorting using SortableAdminMixin, allowing easy reordering of products directly within the admin panel. This controls the display order in the webshop, giving full flexibility without needing database queries or manual updates. The result is a user-friendly and efficient backend that supports quick content management and a seamless workflow for maintaining the shop.

I customized the admin menu further by adding custom icons to each section using Jazzmin's configuration, along with personalized headings like "SizeMeApp" to reflect the brand and improve navigation clarity.

![Admin Dashboard](documents/images_readme/admin-dashboard.jpg)

[Back to Content Table](#content)

<br>
<br>
<hr>
<hr>
<br>
<br>

# TECHNOLOGIES USED
- [Languages used to create the website](#languages-used-to-create-the-website)
- [Frameworks & Libraries](#frameworks-and-libraries)
- [Software](#software)
- [Automated Tools](#automated-tools)
- [AI](#ai)


## Languages Used to Create the Website
- HTML
- CSS
- JavaScript
- Python

## Frameworks and Libraries
- Django (for development and testing).
- Bootstrap (for responsive design and styling).
- Font Awesome (for icons).
- Google Fonts (for typography).
- Iloveimg.com (to compress images for faster loading).

## Software
- Adobe Illustrator (for wireframes and image creation).
- Adobe Photoshop (for image editing and optimization).
- VS Code (for version control).
- GitHub (to save and store the website's code and files).

## Automated Tools
- Chrome DevTools (for debugging and testing).
- Lighthouse (to analyze performance, accessibility, and SEO).
- W3C HTML & CSS Validator (to validate and check the html and css).
- JSHint (to validate and check the Javascript code).
- Techsini.com (for multidevice image and testing responsiveness).
- CI Python Linter (to validate and check the Python code).
- Coverage (for testing).

## AI
I often use AI tools like ChatGPT and Perplexity and have used them both throughout my work on SizeMeApp. These platforms have supported everything from technical troubleshooting to refining UX and brainstorming product features. AI has accelerated my workflow, offered new perspectives, and helped me make more informed decisions at every stage of the project. For me it's like having an always-available creative and technical partner.

[Back to Content Table](#content)

<br>
<br>
<hr>
<hr>
<br>
<br>

# DEPLOYMENT
The website is deployed on Heroku with GitHub Integration.

## Prerequisites
- GitHub repository containing your project files.
- A Procfile (if needed) specifying the start command for your app.
- A requirements.txt (for Python apps).

## Create a Heroku Account and App
- Go to Heroku and sign up (or log in if you already have an account).
- Click "New" > "Create new app" from the Heroku dashboard.
- Choose a unique App Name and select a region.
- Click "Create App".

![Heroku Deployment Add App](documents/images_readme/deploy_heroku_add-app.jpg)

## Connect GitHub Repository to Heroku
- In the Deploy tab of your Heroku app, go to "Deployment Method".
- Select "GitHub".
- Click "Connect to GitHub" and authorize Heroku to access your repositories.
- Search for your repository name and click "Connect".

![Heroku Deployment Github](documents/images_readme/deploy_heroku_connect-github.jpg)

## Configure Environment Variables
In the Settings tab, click "Reveal Config Vars" to add environment variables like API keys, database URLs, etc.

![Heroku Deployment Config Vars](documents/images_readme/deploy_heroku_add-config_vars.jpg)

## Deploy the App
- Under "Manual Deploy", select the branch you want to deploy (main).
- Click "Deploy Branch".
- Wait for Heroku to build and deploy your app.

## Check Your Deployed Website
- Once the deployment is successful, Heroku will provide a URL (e.g., https://your-app-name.herokuapp.com/).
- Click the URL (VIEW) to access your deployed website.

![Heroku Deployment Add App](documents/images_readme/deploy_heroku_deploy-branch.jpg)

[Back to Content Table](#content)

<br>
<br>
<hr>
<hr>
<br>
<br>

# TESTING

## Detailed Testing Documentation
For detailed documentation on the testing process, refer to [TESTING.md](TESTING.md). This file contains images, test results, and analysis of the testing conducted on the project, providing insights into functionality, UI performance, and overall system behavior. 

[Back to Content Table](#content)

<br>
<br>
<hr>
<hr>
<br>
<br>

# REFERENCES

https://www.djangoproject.com/<br>
https://docs.djangoproject.com/en/dev/topics/testing/<br>
https://peps.python.org/pep-0008/<br>
https://www.iloveimg.com/<br>
https://stackoverflow.com/questions<br>
https://www.vecteezy.com/vector-art/26392255-astrological-sign/<br>
- Free Download Template for website checking from https://www.hubspot.com
- Code Institute Tutorials and Learning Content
- Slack Community and information
- Stand Ups with Kay

# CREDITS
Parts of the webshop were originally based on Code Institute’s Boutique Ado walkthrough, which served as a template and learning tool. While most of the code has been heavily modified to suit the SizeMeApp use case, some structure and snippets may still resemble the original source. Full credit is given.

# PERSONAL NOTES
This project marks the real beginning of SizeMeApp - not just an idea scribbled in a notebook, but a minimum viable product with real logic, real users, and real quirks. The goal was to build something that actually works: a smart dashboard, a custom fit system, and a prototype webshop, all stitched together in Django.

I learned fast that writing code is like tailoring - every detail matters, nothing fits until it actually fits, and the moment you think you’re done, you spot a bug in the hem. Modals didn’t behave, layouts broke like zippers, and yet somehow, I loved every minute of it.

There’s still more to do - camera sync, API integrations, maybe even a little machine learning. But for now, SizeMeApp is a stitched-up dream that fits just right.

<hr>

# ACKNOWLEDGMENTS
I want to thank my mentor Rory Patrick for always being so supporting and engaging in showing me new tips and tricks. Also a big thank you to the Slack community at Code Institute and the peers who are always eager to help out.

[Back to Content Table](#content)

<br>
<br>
<hr>
<hr>
<br>
<br>
