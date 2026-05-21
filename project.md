# The Cooking Nurse - Project Architecture & Vision

## 1. Project Vision
"The Cooking Nurse" platform is designed to be a unified, fully owned digital asset. It resolves the client's core problem of fragmented customer data and manual administration across social media platforms. 

By combining her personal culinary portfolio, a booking engine for cooking classes, and a robust e-commerce storefront for her grocery brand ("Fresh Pickens"), the platform creates a seamless user experience. It captures essential CRM data automatically through mandatory account creation at checkout, drastically reducing her administrative burden and enabling scalable future growth.

## 2. End-to-End Architecture

### 2.1. Backend Framework (Django Monolith)
The project uses **Django** in a monolithic architecture, relying on Server-Side Rendering (SSR) via Django Templates. To ensure high maintainability and ease of testing, the project is strictly divided into highly granular **micro-apps**:
*   `users`: Manages authentication, the custom `AbstractBaseUser` model (email as login), the Customer Dashboard, and the bespoke Staff Inventory Dashboard.
*   `portfolio`: Handles static-heavy branding pages (Home, About, Studio Rental).
*   `catalog`: The e-commerce engine for "Fresh Pickens" (Categories, Products, and strict SKUs/Variants with inventory tracking). Handles both physical goods and digital downloads.
*   `classes`: Manages the scheduling and capacity tracking for physical cooking classes (Course -> Sessions), as well as access to pre-recorded online classes.
*   `cart`: A sophisticated, unified session-based shopping cart capable of mixing physical variants, digital courses, and physical class bookings.
*   `orders`: Handles the checkout flow, order generation, address capture, and inventory deduction.

### 2.2. Database Strategy
*   **Dev:** SQLite3 (Currently active).
*   **Prod:** PostgreSQL (Target).
*   **Data Models:** 
    *   Unified `Product` model using a `product_type` flag (physical vs. digital) to keep the cart and order logic clean, avoiding complex polymorphic database relations.
    *   Class scheduling uses a Parent (`Course`) / Child (`ClassSession`) relationship, treating specific class dates as inventory with a strict `capacity`.

### 2.3. Frontend & Styling
*   **HTML:** Django Templates extending from a global `base.html`.
*   **CSS:** **Tailwind CSS** (v3.4) compiled via local Node/npm scripts.
*   **Design Language:** Implements advanced Material Design 3 token concepts (`surface-container`, `tertiary-fixed`) mapped exactly to the brand colors: Forest Green (`#0B5B2E`), Mustard Gold (`#C69C08`), and Rust Red (`#A91B0D`).
*   **UX/UI:** Features a sticky desktop header and an app-style bottom tab bar for mobile users to optimize navigation for social media traffic.

### 2.4. Future Integrations
*   **Payments:** Local API integration (e.g., Pesapal, Flutterwave) to process MTN Momo, Airtel Money, and international Visa/Mastercards.
*   **Video DRM:** Secure video hosting (Mux or Vimeo Pro) for online class delivery.
*   **Email:** AWS SES or SendGrid for transactional receipts and built-in newsletters.

## 3. Current Status (Where We Are Now)
**Phase 1 & 2 (Core Engine & Dashboards) are Complete.**
*   [x] Project Initialized (Django + Virtual Environment).
*   [x] Tailwind CSS configured and integrated into Django.
*   [x] Global UI components (`base.html`) and aesthetic prototypes wired up (`home`, `product_list`, `class_timetable`).
*   [x] Database models written, migrated, and populated with dummy data.
*   [x] Dynamic Session Cart fully functional (handles physical, digital, and booking items simultaneously).
*   [x] Combined Checkout & Registration flow completed (Guest checkout automatically creates an account and logs them in).
*   [x] Customer Dashboard completed (Order history, digital downloads).
*   [x] Staff Dashboard completed (Rapid inventory/capacity management for the client).

**Next Steps:**
1.  Refine remaining frontend pages (About, Studio Rental, Product Details).
2.  Integrate the actual Payment Gateway API.
3.  Implement Video Hosting (DRM) logic for online classes.
4.  Setup Production Environment (VPS/Render, PostgreSQL, Domain mapping).
