/**
 * The Cooking Nurse - Interactive Site Walkthrough Engine
 * Built with Driver.js to showcase both public features & advanced staff dashboard CRUD controls.
 * Uses localStorage state persistence to seamlessly reload and resume tours across pages.
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Core State Helpers
    const getTourActive = () => localStorage.getItem('cooking_nurse_tour_active') === 'true';
    const setTourActive = (active) => localStorage.setItem('cooking_nurse_tour_active', active ? 'true' : 'false');
    const getTourStep = () => parseInt(localStorage.getItem('cooking_nurse_tour_step') || '0', 10);
    const setTourStep = (step) => localStorage.setItem('cooking_nurse_tour_step', step.toString());
    const clearTourState = () => {
        localStorage.removeItem('cooking_nurse_tour_active');
        localStorage.removeItem('cooking_nurse_tour_step');
    };

    // Dynamic resolution of paths from global window configs
    const homeUrl = window.homeUrl || '/';
    const loginUrl = window.loginUrl || '/users/login/';
    const dashboardUrl = window.dashboardUrl || '/users/staff-dashboard/';

    const currentPath = window.location.pathname;

    // Check if element is visible
    const isVisible = (selector) => {
        const el = document.querySelector(selector);
        if (!el) return false;
        const style = window.getComputedStyle(el);
        return style.display !== 'none' && style.visibility !== 'hidden' && el.offsetWidth > 0;
    };

    // FAB Button visibility control
    const tourFabContainer = document.getElementById('tour-fab-container');
    const updateFabVisibility = () => {
        if (tourFabContainer) {
            if (getTourActive()) {
                tourFabContainer.style.display = 'none';
            } else {
                tourFabContainer.style.display = 'block';
            }
        }
    };

    // 2. Step Configurations for each Page
    let localSteps = [];
    let pageContext = '';

    if (currentPath === homeUrl || currentPath === '' || currentPath === '/') {
        pageContext = 'home';
        localSteps = [
            // Step 0: Welcome Center Modal
            {
                popover: {
                    title: 'Welcome, Ritah! ✨',
                    description: 'This is a continuous 20-step interactive walkthrough spanning 3 pages (Home -> Login -> Dashboard). As a Registered Nurse and Culinary Chef, this unified digital platform combines your personal brand, booking engine for classes, and your \'Fresh Pickens\' grocery shop into one powerful workspace. Let\'s begin!',
                    position: 'center'
                }
            },
            // Step 1: Cinema Hero Section
            {
                element: '#hero-section',
                popover: {
                    title: 'Stunning Cinematic Hero 🎬',
                    description: 'Marketing Science: Background videos retain social media traffic significantly longer. The dynamic text-loop (e.g. katogo preparation) drives immediate engagement. The "Next Live Class" alert badge dynamically fetches the next available slot from your scheduling database!',
                    side: 'bottom',
                    align: 'center'
                }
            },
            // Step 2: Fresh Pickens Bento Grid Card
            {
                element: '#bento-fresh-pickens',
                popover: {
                    title: 'Fresh Pickens Storefront 🛒',
                    description: 'This is the groceries hub. Here, your clients can easily browse and buy fresh organic produce and pure artisanal grass-fed ghee directly from the live catalog.',
                    side: 'top',
                    align: 'center'
                }
            },
            // Step 3: Cooking Classes Bento Card
            {
                element: '#bento-cooking-classes',
                popover: {
                    title: 'Hands-on Cooking Timetable 🍳',
                    description: 'Your live capacity-tracked scheduling engine! Physical class slots act like strict inventory: they automatically lock when full to prevent overbooking. Digital classes (like pre-recorded videos) have infinite streaming slots.',
                    side: 'top',
                    align: 'center'
                }
            },
            // Step 4: Digital Cookbooks Bento Card
            {
                element: '#bento-digital-library',
                popover: {
                    title: 'Digital Cookbooks Library 📚',
                    description: 'Showcases your premium digital publications. Upon order checkout, these PDF cookbooks and nutritional manuals become instantly downloadable via the customer\'s dashboard.',
                    side: 'top',
                    align: 'center'
                }
            },
            // Step 5: Studio Rental Bento Card
            {
                element: '#bento-studio-rental',
                popover: {
                    title: 'Kitchen Studio Hiring 📸',
                    description: 'Allows clients to calculate provisional hourly quotes and book the sensory kitchen studio for food photography, masterclasses, pro video shoots, or private dining.',
                    side: 'top',
                    align: 'center'
                }
            },
            // Step 6: Navigation Bars
            {
                element: window.innerWidth < 768 ? 'header' : '#desktop-navbar',
                popover: {
                    title: 'Fluid Desktop & Mobile Navigation 🧭',
                    description: 'Features a sticky glassmorphic desktop header and an app-style bottom tab bar for mobile users, keeping navigation extremely fast, smooth, and natural for social media traffic.',
                    side: 'bottom',
                    align: 'center'
                }
            },
            // Step 7: Newsletter lead capture
            {
                element: '#footer-newsletter',
                popover: {
                    title: 'Newsletter CRM Lead Capture ✉️',
                    description: 'Captures and stores organic traffic leads with a subscription box offering a free recipe guide download. Clicking \'Next\' will redirect us to the Administrative Login page!',
                    side: 'top',
                    align: 'center'
                }
            }
        ];
    } else if (currentPath.includes(loginUrl)) {
        pageContext = 'login';
        localSteps = [
            // Step 8: Email Input
            {
                element: '#login-email',
                popover: {
                    title: 'Admin Credentials Showcase 🔑',
                    description: 'To show you the staff management dashboard, we will log in using our demo administrator account. The email is **admin@example.com** (automatically filled in!). Notice that this login is strictly separated from normal customer logins for security purposes.',
                    side: 'bottom',
                    align: 'start'
                },
                onHighlighted: () => {
                    const emailInput = document.getElementById('login-email');
                    if (emailInput) {
                        emailInput.focus();
                        emailInput.value = 'admin@example.com';
                        // Trigger input event to let any framework listeners know it changed
                        emailInput.dispatchEvent(new Event('input', { bubbles: true }));
                    }
                }
            },
            // Step 9: Password Input
            {
                element: '#login-password',
                popover: {
                    title: 'Secure Access Control 🔒',
                    description: 'The administrative password is **adminpassword** (automatically pre-filled for you here too!). Only authenticated Staff Administrators can access the dashboard. Feel free to toggle the eye icon to view it.',
                    side: 'bottom',
                    align: 'start'
                },
                onHighlighted: () => {
                    const passInput = document.getElementById('login-password');
                    if (passInput) {
                        passInput.focus();
                        passInput.value = 'adminpassword';
                        passInput.dispatchEvent(new Event('input', { bubbles: true }));
                    }
                }
            },
            // Step 10: Submit Button
            {
                element: '#login-submit',
                popover: {
                    title: 'Enter the Staff Workspace 🚀',
                    description: 'Click \'Log In\' now to authenticate. The page will reload and instantly launch the Admin Tour!',
                    side: 'top',
                    align: 'center'
                }
            }
        ];
    } else if (currentPath.includes(dashboardUrl)) {
        pageContext = 'dashboard';
        localSteps = [
            // Step 11: Welcome Admin
            {
                popover: {
                    title: 'Welcome to the Staff Dashboard! 👑',
                    description: 'You are logged in! This is the powerful administrative workspace. Here, you can manage every aspect of your business (inventory, classes, bookings, users) with zero technical difficulty. Let\'s review its components!',
                    position: 'center'
                }
            },
            // Step 12: Analytics Summary Card Grid
            {
                element: '.grid-cols-1.sm\\:grid-cols-2.lg\\:grid-cols-4',
                popover: {
                    title: 'Real-time Operations Analytics 📊',
                    description: 'Summarizes key performance indicators (KPIs) in real-time. Note: Total Revenue generated (in UGX) strictly counts fully completed and paid orders only, explicitly ignoring abandoned carts for accuracy!',
                    side: 'bottom',
                    align: 'center'
                }
            },
            // Step 13: Analytics & Orders Tab Content
            {
                element: '#tab-analytics',
                popover: {
                    title: 'Transactions & Delivery Hub 💳',
                    description: 'Shows details of all physical and digital checkout transactions. Administrators can inspect client invoices, billing info, and manage order fulfillment statuses.',
                    side: 'top',
                    align: 'center'
                },
                onHighlighted: () => {
                    const tabBtn = document.getElementById('btn-tab-analytics');
                    if (tabBtn) tabBtn.click();
                }
            },
            // Step 14: Inventory Tab
            {
                element: '#btn-tab-inventory',
                popover: {
                    title: 'Bespoke Storefront Inventory 📦',
                    description: 'Clicking here opens the Fresh Pickens Catalog. You can add new products and manage variant SKUs (e.g., 500ml vs 1L Jar). Stock variants automatically deduct upon checkout to prevent over-selling!',
                    side: 'bottom',
                    align: 'center'
                },
                onHighlighted: () => {
                    const tabBtn = document.getElementById('btn-tab-inventory');
                    if (tabBtn) tabBtn.click();
                }
            },
            // Step 15: Classes Timetable Tab
            {
                element: '#btn-tab-classes',
                popover: {
                    title: 'Classes Scheduler & Slots 🗓️',
                    description: 'Allows rapid scheduling of hands-on physical classes, defining date, start/end times, and setting custom attendee capacity thresholds. Also handles links to online video lessons.',
                    side: 'bottom',
                    align: 'center'
                },
                onHighlighted: () => {
                    const tabBtn = document.getElementById('btn-tab-classes');
                    if (tabBtn) tabBtn.click();
                }
            },
            // Step 16: Studio Rentals Tab
            {
                element: '#btn-tab-rentals',
                popover: {
                    title: 'Studio Rental Requests 📸',
                    description: 'Lists all provisional bookings submitted from the home page. Admins can review requested dates, purpose, hourly quotes, approve slots, and mark them as fully paid.',
                    side: 'bottom',
                    align: 'center'
                },
                onHighlighted: () => {
                    const tabBtn = document.getElementById('btn-tab-rentals');
                    if (tabBtn) tabBtn.click();
                }
            },
            // Step 17: User Access Roles Tab
            {
                element: '#btn-tab-users',
                popover: {
                    title: 'Registered Users Directory 👥',
                    description: 'A secure CRM repository of all registered customers. Ritah can inspect join dates, search contacts, assign admin privileges, or block fraudulent customer accounts.',
                    side: 'bottom',
                    align: 'center'
                },
                onHighlighted: () => {
                    const tabBtn = document.getElementById('btn-tab-users');
                    if (tabBtn) tabBtn.click();
                }
            },
            // Step 18: Newsletter Tab
            {
                element: '#btn-tab-newsletter',
                popover: {
                    title: 'Subscribers Mailing List ✉️',
                    description: 'Shows all organic newsletter subscriptions. Click the \'Copy All Emails\' button to easily copy emails to your clipboard and instantly paste them directly into Mailchimp or AWS SES!',
                    side: 'bottom',
                    align: 'center'
                },
                onHighlighted: () => {
                    const tabBtn = document.getElementById('btn-tab-newsletter');
                    if (tabBtn) tabBtn.click();
                }
            },
            // Step 19: Site Settings Tab
            {
                element: '#btn-tab-site',
                popover: {
                    title: 'Global Site Settings ⚙️',
                    description: 'Your site global content editor. From here, you can easily manage the settings, tags, images, and other general parameters across the entire platform with no coding required.',
                    side: 'bottom',
                    align: 'center'
                },
                onHighlighted: () => {
                    const tabBtn = document.getElementById('btn-tab-site');
                    if (tabBtn) tabBtn.click();
                }
            },
            // Step 20: Concluding Modal
            {
                popover: {
                    title: 'Walkthrough Complete! 🎉',
                    description: 'You\'ve successfully explored every single feature of the Cooking Nurse web asset! From direct public reservations, e-commerce storefront, to unified admin dashboard CRUD controllers. Click \'Finish\' to complete the tour!',
                    position: 'center'
                }
            }
        ];
    }

    // 3. Tour Engine Initialization
    if (localSteps.length > 0) {
        const driverObj = window.driver.js.driver({
            showProgress: true,
            allowClose: true,
            animate: true,
            overlayColor: 'rgba(15, 23, 42, 0.7)', // rich dark backdrop overlay
            steps: localSteps,
            onDestroyed: () => {
                // If closed/exited, reset active states
                clearTourState();
                updateFabVisibility();
            },
            onNextClick: (element, step, options) => {
                const activeIndex = driverObj.getActiveIndex();

                // Page 1 transitions:
                if (pageContext === 'home' && activeIndex === 7) {
                    setTourActive(true);
                    setTourStep(8); // next is login page first step
                    window.location.href = loginUrl;
                    return;
                }

                // Page 2 transitions:
                if (pageContext === 'login' && activeIndex === 2) {
                    // pre-fill and trigger submit click!
                    const emailInput = document.getElementById('login-email');
                    const passInput = document.getElementById('login-password');
                    if (emailInput && passInput) {
                        emailInput.value = 'admin@example.com';
                        passInput.value = 'adminpassword';
                    }
                    // Keep tour active, let dashboard pick it up at Step 11
                    setTourActive(true);
                    setTourStep(11);
                    document.getElementById('login-submit').click();
                    return;
                }

                // Page 3 transitions (dashboard completes):
                if (pageContext === 'dashboard' && activeIndex === 9) {
                    clearTourState();
                    driverObj.destroy();
                    updateFabVisibility();
                    return;
                }

                // Advance standard step
                const currentGlobalStep = getTourStep();
                setTourStep(currentGlobalStep + 1);
                driverObj.moveNext();
            },
            onPrevClick: (element, step, options) => {
                const activeIndex = driverObj.getActiveIndex();

                // Page 2 going back to Page 1:
                if (pageContext === 'login' && activeIndex === 0) {
                    setTourActive(true);
                    setTourStep(7); // go back to last homepage step
                    window.location.href = homeUrl;
                    return;
                }

                // Page 3 going back to Page 2:
                if (pageContext === 'dashboard' && activeIndex === 0) {
                    setTourActive(true);
                    setTourStep(10); // go back to login submit step
                    window.location.href = loginUrl;
                    return;
                }

                // Move backward standard step
                const currentGlobalStep = getTourStep();
                setTourStep(Math.max(0, currentGlobalStep - 1));
                driverObj.movePrevious();
            }
        });

        // 4. Resume logic on page load
        if (getTourActive()) {
            const savedStep = getTourStep();
            let localTargetIndex = 0;

            if (pageContext === 'home' && savedStep >= 0 && savedStep <= 7) {
                localTargetIndex = savedStep;
                updateFabVisibility();
                driverObj.drive(localTargetIndex);
            } else if (pageContext === 'login' && savedStep >= 8 && savedStep <= 10) {
                localTargetIndex = savedStep - 8;
                updateFabVisibility();
                driverObj.drive(localTargetIndex);
            } else if (pageContext === 'dashboard' && savedStep >= 11 && savedStep <= 20) {
                localTargetIndex = savedStep - 11;
                updateFabVisibility();
                // Ensure initial analytics tab is loaded
                const tabBtn = document.getElementById('btn-tab-analytics');
                if (tabBtn) tabBtn.click();
                
                driverObj.drive(localTargetIndex);
            } else {
                // Out of range for current page context, clear tour active
                clearTourState();
                updateFabVisibility();
            }
        }
    }

    // 5. Click listener on Floating tour button
    const startTourBtn = document.getElementById('start-tour-btn');
    if (startTourBtn) {
        startTourBtn.addEventListener('click', () => {
            // Trigger or restart tour
            clearTourState();
            setTourActive(true);
            setTourStep(0);

            // Force a clean slate: If logged in, logout first. The backend redirects to home automatically!
            if (window.userIsAuthenticated && window.logoutUrl) {
                window.location.href = window.logoutUrl;
                return;
            }

            if (currentPath === homeUrl || currentPath === '/' || currentPath === '') {
                // Start immediately
                updateFabVisibility();
                window.location.reload();
            } else {
                // Redirect to homepage to start from beginning
                window.location.href = homeUrl;
            }
        });
    }

    // Initially sync floating button visibility
    updateFabVisibility();
});
