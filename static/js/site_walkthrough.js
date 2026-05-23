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
                    description: 'This is a continuous 30-step interactive walkthrough spanning 3 pages (Home -> Login -> Dashboard). As a Registered Nurse and Culinary Chef, this unified digital platform combines your personal brand, booking engine for classes, and your \'Fresh Pickens\' grocery shop into one powerful workspace. Let\'s begin!',
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
                    title: 'Kitchen Studio Renting 📸',
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
            // local index 0 (Global Step 11)
            {
                popover: {
                    title: 'Welcome to the Staff Dashboard! 👑',
                    description: 'You are logged in! This is the powerful administrative workspace. Here, you can manage every aspect of your business (inventory, classes, bookings, users) with zero technical difficulty. Let\'s review its components!',
                    position: 'center'
                }
            },
            // local index 1 (Global Step 12)
            {
                element: window.innerWidth < 768 ? '.grid > div:nth-child(1)' : '.grid-cols-1.sm\\:grid-cols-2.lg\\:grid-cols-4',
                popover: {
                    title: 'Real-time Operations Analytics 📊',
                    description: 'Summarizes key performance indicators (KPIs) in real-time. Note: Total Revenue generated (in UGX) strictly counts fully completed and paid orders only, explicitly ignoring abandoned carts for accuracy!',
                    side: 'bottom',
                    align: 'center'
                }
            },
            // local index 2 (Global Step 13)
            {
                element: '#btn-tab-analytics',
                popover: {
                    title: 'Transactions & Delivery Hub 💳',
                    description: 'This tab shows details of all physical and digital checkout transactions.',
                    side: 'bottom',
                    align: 'center'
                },
                onHighlighted: () => {
                    const tabBtn = document.getElementById('btn-tab-analytics');
                    if (tabBtn) tabBtn.click();
                }
            },
            // local index 3 (Global Step 14)
            {
                element: window.innerWidth < 768 ? '#tab-analytics' : '#tab-analytics table',
                popover: {
                    title: 'Client Transactions Log 📜',
                    description: 'Every client order is recorded here. Click the "Manage Delivery" button to process an order, update its status from "Pending" to "Shipped" or "Completed", and trigger automated client notification emails!',
                    side: 'top',
                    align: 'center'
                }
            },
            // local index 4 (Global Step 15)
            {
                element: '#btn-tab-inventory',
                popover: {
                    title: 'Bespoke Storefront Inventory 📦',
                    description: 'Clicking here opens the Fresh Pickens Catalog manager.',
                    side: 'bottom',
                    align: 'center'
                },
                onHighlighted: () => {
                    const tabBtn = document.getElementById('btn-tab-inventory');
                    if (tabBtn) tabBtn.click();
                }
            },
            // local index 5 (Global Step 16)
            {
                element: '#tab-inventory .flex.gap-3',
                popover: {
                    title: 'Store Creation Engine 🏗️',
                    description: 'Quickly create new Grocery Categories (like "Organic Spices") or add entirely New Products to your public storefront.',
                    side: 'bottom',
                    align: 'start'
                }
            },
            // local index 6 (Global Step 17)
            {
                element: window.innerWidth < 768 ? '#tab-inventory' : '#tab-inventory table th:nth-child(4)',
                popover: {
                    title: 'Variant & Stock Guardian 🛡️',
                    description: 'This column monitors variants (e.g. 500ml vs 1L). Crucially, stock variants deduct automatically on public checkout to prevent over-selling. Low stock triggers the red alert card above!',
                    side: 'bottom',
                    align: 'center'
                }
            },
            // local index 7 (Global Step 18)
            {
                element: '#btn-tab-classes',
                popover: {
                    title: 'Classes Scheduler 🗓️',
                    description: 'Manage physical and digital cooking class portals.',
                    side: 'bottom',
                    align: 'center'
                },
                onHighlighted: () => {
                    const tabBtn = document.getElementById('btn-tab-classes');
                    if (tabBtn) tabBtn.click();
                }
            },
            // local index 8 (Global Step 19)
            {
                element: '#tab-classes .btn-accent',
                popover: {
                    title: 'Launch a New Masterclass 🎓',
                    description: 'Create a new course payload—upload a vibrant cover image, set the base price in UGX, and configure it as either a Physical Studio Class or a Digital Video Course!',
                    side: 'bottom',
                    align: 'center'
                }
            },
            // local index 9 (Global Step 20)
            {
                element: window.innerWidth < 768 ? '#tab-classes' : '#tab-classes table th:nth-child(3)',
                popover: {
                    title: 'Capacity Overbooking Prevention 🚦',
                    description: 'Physical classes require session dates. The system tracks "Seats Registered" against "Capacity" strictly. If a slot hits capacity, it locks immediately showing a "Full!" badge on the public UI.',
                    side: 'bottom',
                    align: 'center'
                }
            },
            // local index 10 (Global Step 21)
            {
                element: '#btn-tab-rentals',
                popover: {
                    title: 'Studio Rental Requests 📸',
                    description: 'Manage incoming kitchen hiring quotes.',
                    side: 'bottom',
                    align: 'center'
                },
                onHighlighted: () => {
                    const tabBtn = document.getElementById('btn-tab-rentals');
                    if (tabBtn) tabBtn.click();
                }
            },
            // local index 11 (Global Step 22)
            {
                element: window.innerWidth < 768 ? '#tab-rentals' : '#tab-rentals table th:nth-child(6)',
                popover: {
                    title: 'Workflow State Machine 🔄',
                    description: 'Control the booking lifecycle! A pending request can be "Approved", then transition to "Mark Paid". This updates the internal CRM status and locks the studio calendar.',
                    side: 'bottom',
                    align: 'end'
                }
            },
            // local index 12 (Global Step 23)
            {
                element: '#btn-tab-users',
                popover: {
                    title: 'Registered Users CRM 👥',
                    description: 'A secure repository of all registered customers and staff.',
                    side: 'bottom',
                    align: 'center'
                },
                onHighlighted: () => {
                    const tabBtn = document.getElementById('btn-tab-users');
                    if (tabBtn) tabBtn.click();
                }
            },
            // local index 13 (Global Step 24)
            {
                element: window.innerWidth < 768 ? '#tab-users' : '#tab-users table th:nth-child(5)',
                popover: {
                    title: 'Granular Privilege Escalation 🔐',
                    description: 'From here, Ritah can elevate trusted employees to "Staff" so they can access this dashboard, or instantly "Block" abusive or fraudulent customer accounts from accessing the storefront.',
                    side: 'bottom',
                    align: 'end'
                }
            },
            // local index 14 (Global Step 25)
            {
                element: '#btn-tab-newsletter',
                popover: {
                    title: 'Subscribers Mailing List ✉️',
                    description: 'Organic lead aggregation.',
                    side: 'bottom',
                    align: 'center'
                },
                onHighlighted: () => {
                    const tabBtn = document.getElementById('btn-tab-newsletter');
                    if (tabBtn) tabBtn.click();
                }
            },
            // local index 15 (Global Step 26)
            {
                element: '#tab-newsletter button',
                popover: {
                    title: '1-Click CRM Export 📋',
                    description: 'Easily "Copy All Emails" to your clipboard and paste them directly into your preferred bulk emailing tool (Mailchimp, AWS SES, or Brevo) for marketing campaigns!',
                    side: 'bottom',
                    align: 'end'
                }
            },
            // local index 16 (Global Step 27)
            {
                element: '#btn-tab-site',
                popover: {
                    title: 'Global Site Settings ⚙️',
                    description: 'Your no-code frontend editor.',
                    side: 'bottom',
                    align: 'center'
                },
                onHighlighted: () => {
                    const tabBtn = document.getElementById('btn-tab-site');
                    if (tabBtn) tabBtn.click();
                }
            },
            // local index 17 (Global Step 28)
            {
                element: '#tab-site .grid > div:nth-child(1)',
                popover: {
                    title: 'Cinematic Hero Controller 🎬',
                    description: 'Instantly swap the home page background video (.mp4) or the looping typewriter keywords without ever touching a line of code. It injects directly into the production templates!',
                    side: 'top',
                    align: 'start'
                }
            },
            // local index 18 (Global Step 29)
            {
                element: '#tab-site button[type="submit"]',
                popover: {
                    title: 'Save and Deploy! 🚀',
                    description: 'Hitting save instantly updates the frontend for all global traffic! This concludes our deep dive into your powerful new workspace. Enjoy!',
                    side: 'top',
                    align: 'center'
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
            stagePadding: window.innerWidth < 768 ? 5 : 10, // tighter padding on mobile
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
                if (pageContext === 'dashboard' && activeIndex === 18) {
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
            } else if (pageContext === 'dashboard' && savedStep >= 11 && savedStep <= 29) {
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
