import datetime
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from catalog.models import Category, Product, ProductVariant
from classes.models import Course, ClassSession
from orders.models import Order, OrderItem
from cart.cart import Cart
from portfolio.models import NewsletterSubscriber

User = get_user_model()

class CookingNurseEndToEndTests(TestCase):
    def setUp(self):
        # 1. Clear old data (though Django TestCase isolates the DB)
        Category.objects.all().delete()
        Product.objects.all().delete()
        Course.objects.all().delete()
        User.objects.all().delete()

        # 2. Create Superuser (admin@example.com / adminpassword)
        self.admin_user = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpassword'
        )

        # 3. Create Categories
        self.cat_groceries = Category.objects.create(name="Groceries", description="Fresh and organic supplies.")
        self.cat_digital = Category.objects.create(name="Digital Cookbooks", description="Downloadable recipe books.")

        # 4. Create Products & Variants
        self.p_tomatoes = Product.objects.create(
            category=self.cat_groceries,
            name="Heirloom Tomato Harvest",
            product_type="physical",
            description="Sustainably grown organic tomatoes."
        )
        self.v_tomatoes_1kg = ProductVariant.objects.create(
            product=self.p_tomatoes, name="1 Kg Box", price=12000, stock=50
        )
        self.v_tomatoes_2kg = ProductVariant.objects.create(
            product=self.p_tomatoes, name="2 Kg Box", price=22000, stock=30
        )

        self.p_ghee = Product.objects.create(
            category=self.cat_groceries,
            name="Pure Artisanal Ghee",
            product_type="physical",
            description="Traditional clarified butter."
        )
        self.v_ghee_500ml = ProductVariant.objects.create(
            product=self.p_ghee, name="500ml Jar", price=25000, stock=20
        )

        self.p_cookbook = Product.objects.create(
            category=self.cat_digital,
            name="The Everyday Magic Cookbook",
            product_type="digital",
            description="A complete digital guide."
        )
        self.v_cookbook_download = ProductVariant.objects.create(
            product=self.p_cookbook, name="Digital Download", price=50000, stock=999
        )

        # 5. Create Courses & Sessions
        self.course_breakfast = Course.objects.create(
            title="Breakfast Dishes & Meal Planning",
            course_type="physical",
            description="Learn breakfast dishes.",
            price=150000
        )
        self.session_breakfast = ClassSession.objects.create(
            course=self.course_breakfast,
            date=datetime.date.today() + datetime.timedelta(days=5),
            start_time=datetime.time(9, 0),
            end_time=datetime.time(17, 0),
            capacity=10
        )

        self.course_masterclass = Course.objects.create(
            title="Local Food Masterclass",
            course_type="physical",
            description="Master local foods.",
            price=150000
        )
        self.session_masterclass = ClassSession.objects.create(
            course=self.course_masterclass,
            date=datetime.date.today() + datetime.timedelta(days=12),
            start_time=datetime.time(9, 0),
            end_time=datetime.time(18, 0),
            capacity=12
        )

        self.course_sourdough = Course.objects.create(
            title="Artisanal Sourdough & Gut Health",
            course_type="online",
            description="Online sourdough course.",
            price=85000,
            video_url="https://vimeo.com/placeholder"
        )

        # Clients for testing
        self.client_unauth = Client()
        
        # A standard registered user
        self.client_user = User.objects.create_user(
            email='client@test.com',
            password='clientpassword',
            first_name='Test',
            last_name='Client',
            phone_number='+256700000000'
        )
        self.client_auth = Client()
        self.client_auth.login(email='client@test.com', password='clientpassword')

    # ==========================================
    # GROUP 1: GLOBAL UI & NAVIGATION
    # ==========================================
    
    def test_01_responsive_navbar_assets(self):
        """Test 1: Home page loads successfully with assets and navbar classes."""
        response = self.client_unauth.get(reverse('portfolio:home'))
        self.assertEqual(response.status_code, 200)
        # Verify typography stylesheets exist
        self.assertContains(response, 'fonts.googleapis.com')
        # Verify navigation structure elements (Material icons, desktop, mobile classes)
        self.assertContains(response, 'material-symbols-outlined')
        self.assertContains(response, 'hidden md:block') # Desktop nav container class
        self.assertContains(response, 'md:hidden')       # Mobile top bar container class

    def test_02_active_state_routing(self):
        """Test 2: Routes to shop page load successfully."""
        response = self.client_unauth.get(reverse('catalog:product_list'))
        self.assertEqual(response.status_code, 200)
        # Check active state class condition on menu
        self.assertContains(response, 'Fresh Pickens Market')

    def test_03_global_footer_rendering(self):
        """Test 3: Footer displays consistently."""
        response = self.client_unauth.get(reverse('portfolio:home'))
        self.assertContains(response, 'Sustainability')
        self.assertContains(response, 'Wholesale')
        self.assertContains(response, '© 2026 The Cooking Nurse')

    def test_04_missing_image_fallback(self):
        """Test 4: Product list contains beautiful fallback images."""
        response = self.client_unauth.get(reverse('catalog:product_list'))
        self.assertEqual(response.status_code, 200)
        # Since dummy products don't have real file upload images in test mode,
        # they should use the fallback placeholder image url.
        self.assertContains(response, 'ADBb0uhipnwAI0ENs4U1VZjSckqGn1GFOdTBB6kKkdSot_3Yvkhr5euUwm9fS2OvJvpGc70uzxEKzkFdA4MWiy2tOsP6UsA55HPkSvFVq47ver5uFCGzYNjOFbX42PCW7sY_MoQ63IbCHhliBsyA0hfGSBjnYizl_fy8S8ipgQpR7n8YPBWajxvMNXA_2nYvhbueK8ez7HD-0wlko4YfLEy7LHC090P7ZaCnXQZMihuOIfMKDnw7ZymPK-LPMLDE')

    # ==========================================
    # GROUP 2: THE SHOPPING CART ENGINE
    # ==========================================

    def test_05_add_physical_product_to_cart(self):
        """Test 5: Adding a physical variant redirects to cart and updates cart items."""
        # Add Heirloom Tomato Harvest 1 Kg variant (id=self.v_tomatoes_1kg.id)
        response = self.client_unauth.post(
            reverse('cart:cart_add', args=['variant', self.v_tomatoes_1kg.id]),
            {'quantity': 1}
        )
        self.assertRedirects(response, reverse('cart:cart_detail'))
        
        # Verify item exists in session cart
        session_cart = self.client_unauth.session.get('cart')
        self.assertIsNotNone(session_cart)
        self.assertIn(f"variant_{self.v_tomatoes_1kg.id}", session_cart)
        self.assertEqual(session_cart[f"variant_{self.v_tomatoes_1kg.id}"]['quantity'], 1)

    def test_06_add_digital_product_to_cart(self):
        """Test 6: Adding physical and digital products simultaneously is supported."""
        # Add physical product
        self.client_unauth.post(reverse('cart:cart_add', args=['variant', self.v_tomatoes_1kg.id]), {'quantity': 1})
        # Add digital product
        self.client_unauth.post(reverse('cart:cart_add', args=['variant', self.v_cookbook_download.id]), {'quantity': 1})
        
        session_cart = self.client_unauth.session.get('cart')
        self.assertIn(f"variant_{self.v_tomatoes_1kg.id}", session_cart)
        self.assertIn(f"variant_{self.v_cookbook_download.id}", session_cart)

    def test_07_add_class_booking_to_cart(self):
        """Test 7: Dynamic cart handles physical, digital, and course sessions coexisting."""
        self.client_unauth.post(reverse('cart:cart_add', args=['variant', self.v_tomatoes_1kg.id]), {'quantity': 1})
        self.client_unauth.post(reverse('cart:cart_add', args=['variant', self.v_cookbook_download.id]), {'quantity': 1})
        self.client_unauth.post(reverse('cart:cart_add', args=['session', self.session_masterclass.id]), {'quantity': 1})
        
        session_cart = self.client_unauth.session.get('cart')
        self.assertIn(f"variant_{self.v_tomatoes_1kg.id}", session_cart)
        self.assertIn(f"variant_{self.v_cookbook_download.id}", session_cart)
        self.assertIn(f"session_{self.session_masterclass.id}", session_cart)

    def test_08_dynamic_navigation_badge(self):
        """Test 8: Badge count reflects total items."""
        # Cart starts at 0
        response = self.client_unauth.get(reverse('portfolio:home'))
        self.assertContains(response, '>0<')
        
        # Add 3 items
        self.client_unauth.post(reverse('cart:cart_add', args=['variant', self.v_tomatoes_1kg.id]), {'quantity': 1})
        self.client_unauth.post(reverse('cart:cart_add', args=['variant', self.v_cookbook_download.id]), {'quantity': 1})
        self.client_unauth.post(reverse('cart:cart_add', args=['session', self.session_masterclass.id]), {'quantity': 1})
        
        response = self.client_unauth.get(reverse('portfolio:home'))
        self.assertContains(response, '>3<')

    def test_09_cart_math_and_removal(self):
        """Test 9: Removing item works and recalculates total price correctly."""
        self.client_unauth.post(reverse('cart:cart_add', args=['variant', self.v_tomatoes_1kg.id]), {'quantity': 1}) # 12000 UGX
        self.client_unauth.post(reverse('cart:cart_add', args=['variant', self.v_cookbook_download.id]), {'quantity': 1}) # 50000 UGX
        
        # Remove cookbook variant
        response = self.client_unauth.post(reverse('cart:cart_remove', args=['variant', self.v_cookbook_download.id]))
        self.assertRedirects(response, reverse('cart:cart_detail'))
        
        # Check session cart
        session_cart = self.client_unauth.session.get('cart')
        self.assertNotIn(f"variant_{self.v_cookbook_download.id}", session_cart)
        self.assertIn(f"variant_{self.v_tomatoes_1kg.id}", session_cart)
        
        # Verify dynamic total calculation on cart page
        response = self.client_unauth.get(reverse('cart:cart_detail'))
        self.assertContains(response, '12000 UGX')
        self.assertNotContains(response, '62000 UGX')

    # ==========================================
    # GROUP 3: THE MANDATORY AUTH & CHECKOUT FLOW
    # ==========================================

    def test_10_guest_checkout_guard(self):
        """Test 10: Guest checkout requires credentials."""
        # Add item to cart
        self.client_unauth.post(reverse('cart:cart_add', args=['variant', self.v_tomatoes_1kg.id]), {'quantity': 1})
        
        response = self.client_unauth.get(reverse('orders:checkout'))
        self.assertEqual(response.status_code, 200)
        # Verify credentials form inputs are present in page context for guests
        self.assertContains(response, 'name="email"')
        self.assertContains(response, 'name="password"')

    def test_11_duplicate_email_prevention(self):
        """Test 11: Duplicate guest registration is blocked."""
        self.client_unauth.post(reverse('cart:cart_add', args=['variant', self.v_tomatoes_1kg.id]), {'quantity': 1})
        
        # Try checking out with existing superuser email
        response = self.client_unauth.post(reverse('orders:checkout'), {
            'email': 'admin@example.com',
            'password': 'somepassword',
            'first_name': 'Guest',
            'last_name': 'User',
            'phone_number': '+256701111111',
            'city': 'Kampala',
            'neighborhood': 'Kololo',
            'street_address': 'Plot 4, Acacia Ave'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'An account with this email already exists.')

    def test_12_successful_guest_checkout(self):
        """Test 12: Successful guest checkout provisions account and logs them in."""
        self.client_unauth.post(reverse('cart:cart_add', args=['variant', self.v_tomatoes_1kg.id]), {'quantity': 1})
        
        # Place order
        response = self.client_unauth.post(reverse('orders:checkout'), {
            'email': 'new_guest@test.com',
            'password': 'guestpassword',
            'first_name': 'Guesty',
            'last_name': 'McGuest',
            'phone_number': '+256701222222',
            'city': 'Kampala',
            'neighborhood': 'Bukoto',
            'street_address': 'Plot 10, Bukoto St'
        })
        # Verify it redirects to success page
        new_order = Order.objects.get(user__email='new_guest@test.com')
        self.assertRedirects(response, reverse('orders:success', args=[new_order.id]))
        
        # Check if the guest user was actually saved in DB
        user_exists = User.objects.filter(email='new_guest@test.com').exists()
        self.assertTrue(user_exists)

    def test_13_auto_login_verification(self):
        """Test 13: Order success automatically authenticates the user."""
        self.client_unauth.post(reverse('cart:cart_add', args=['variant', self.v_tomatoes_1kg.id]), {'quantity': 1})
        
        self.client_unauth.post(reverse('orders:checkout'), {
            'email': 'autologin@test.com',
            'password': 'somepassword',
            'first_name': 'Auto',
            'last_name': 'Login',
            'phone_number': '+256701333333',
            'city': 'Kampala',
            'neighborhood': 'Kololo',
            'street_address': 'Acacia'
        })
        
        # Check if client session now contains user ID
        self.assertTrue(self.client_unauth.session.get('_auth_user_id') is not None)
        
        # Verify access to dashboard without login prompt
        response = self.client_unauth.get(reverse('users:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome back, Auto')

    def test_14_logged_in_checkout_behavior(self):
        """Test 14: Logged-in users skip credentials step at checkout."""
        # Add item using authenticated client
        self.client_auth.post(reverse('cart:cart_add', args=['variant', self.v_tomatoes_1kg.id]), {'quantity': 1})
        
        response = self.client_auth.get(reverse('orders:checkout'))
        self.assertEqual(response.status_code, 200)
        # Verify account details credentials inputs are completely omitted
        self.assertNotContains(response, 'name="password"')

    # ==========================================
    # GROUP 4: THE CUSTOMER DASHBOARD
    # ==========================================

    def test_15_order_history_accuracy(self):
        """Test 15: Customer dashboard displays correct order details."""
        # Place order using authenticated user
        order = Order.objects.create(
            user=self.client_user,
            total_amount=12000,
            status='pending',
            city='Kampala',
            neighborhood='Kiswa',
            street_address='Acre Road'
        )
        OrderItem.objects.create(
            order=order,
            product_variant=self.v_tomatoes_1kg,
            quantity=1,
            price_at_time=12000
        )
        
        response = self.client_auth.get(reverse('users:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f"Order #{order.id}")
        self.assertContains(response, "12000 UGX")
        self.assertContains(response, "pending")
        self.assertContains(response, "Heirloom Tomato Harvest")

    def test_16_digital_download_access(self):
        """Test 16: Cookbook purchases provide digital download card access."""
        order = Order.objects.create(user=self.client_user, total_amount=50000)
        OrderItem.objects.create(
            order=order,
            product_variant=self.v_cookbook_download,
            quantity=1,
            price_at_time=50000
        )
        
        response = self.client_auth.get(reverse('users:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'The Everyday Magic Cookbook')
        self.assertContains(response, 'download_for_offline')

    def test_17_online_class_access(self):
        """Test 17: Online course purchases provide video portal access."""
        order = Order.objects.create(user=self.client_user, total_amount=85000)
        OrderItem.objects.create(
            order=order,
            online_course=self.course_sourdough,
            quantity=1,
            price_at_time=85000
        )
        
        response = self.client_auth.get(reverse('users:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Artisanal Sourdough &amp; Gut Health')
        self.assertContains(response, 'open_in_new')

    # ==========================================
    # GROUP 5: THE CLIENT'S STAFF DASHBOARD
    # ==========================================

    def test_18_staff_security_guard(self):
        """Test 18: Non-staff users cannot access staff dashboard."""
        response = self.client_auth.get(reverse('users:staff_dashboard'))
        # Should redirect to login with staff check
        self.assertNotEqual(response.status_code, 200)

    def test_19_inventory_deduction_verification(self):
        """Test 19: Placing an order properly reduces product variant stock."""
        initial_stock = self.v_tomatoes_1kg.stock # 50
        
        # Put in cart
        self.client_unauth.post(reverse('cart:cart_add', args=['variant', self.v_tomatoes_1kg.id]), {'quantity': 2})
        
        # Checkout
        self.client_unauth.post(reverse('orders:checkout'), {
            'email': 'inventory_test@test.com',
            'password': 'somepassword',
            'first_name': 'Inv',
            'last_name': 'Test',
            'phone_number': '+256701555555',
            'city': 'Kampala',
            'neighborhood': 'Nakasero',
            'street_address': 'Plot 12'
        })
        
        # Verify variant stock is deducted
        self.v_tomatoes_1kg.refresh_from_db()
        self.assertEqual(self.v_tomatoes_1kg.stock, initial_stock - 2)

    def test_20_rapid_inventory_update(self):
        """Test 20: Superuser can modify inventory from staff dashboard."""
        # Log in superuser on a client
        admin_client = Client()
        admin_client.login(email='admin@example.com', password='adminpassword')
        
        # Modify stock of tomatoes 1kg via staff POST
        response = admin_client.post(reverse('users:staff_dashboard'), {
            f'variant_{self.v_tomatoes_1kg.id}': 77
        })
        self.assertRedirects(response, reverse('users:staff_dashboard'))
        
        # Verify in DB
        self.v_tomatoes_1kg.refresh_from_db()
        self.assertEqual(self.v_tomatoes_1kg.stock, 77)

    # ==========================================
    # GROUP 6: NEW WORKFLOW INTEGRATION FEATURES
    # ==========================================

    def test_21_newsletter_subscription_flow(self):
        """Test 21: Built-in Newsletter Subscriber signup and validation."""
        # 1. Test subscribing a new email address
        email_addr = "new_subscriber@example.com"
        response = self.client_unauth.post(reverse('portfolio:newsletter_subscribe'), {
            'email': email_addr,
            'next': reverse('portfolio:home')
        })
        # Verify redirect to home
        self.assertRedirects(response, reverse('portfolio:home'))
        # Verify DB entry exists
        self.assertTrue(NewsletterSubscriber.objects.filter(email=email_addr).exists())

        # 2. Test duplicate subscription behavior
        response_dup = self.client_unauth.post(reverse('portfolio:newsletter_subscribe'), {
            'email': email_addr,
            'next': reverse('portfolio:home')
        })
        # Verify redirect to home
        self.assertRedirects(response_dup, reverse('portfolio:home'))
        # Verify it didn't create a new database row (should remain exactly one)
        self.assertEqual(NewsletterSubscriber.objects.filter(email=email_addr).count(), 1)

    def test_22_secure_digital_download_access_control(self):
        """Test 22: Secure digital downloads access gating and fallback file stream."""
        # 1. Unauthenticated users should be redirected to login
        response = self.client_unauth.get(reverse('catalog:download_digital_item', args=[self.v_cookbook_download.id]))
        self.assertEqual(response.status_code, 302)

        # 2. Authenticated user who hasn't purchased the item should receive 404
        response_unpurchased = self.client_auth.get(reverse('catalog:download_digital_item', args=[self.v_cookbook_download.id]))
        self.assertEqual(response_unpurchased.status_code, 404)

        # 3. Authenticated user who HAS purchased the item should successfully download the fallback stream
        order = Order.objects.create(user=self.client_user, total_amount=50000)
        OrderItem.objects.create(
            order=order,
            product_variant=self.v_cookbook_download,
            quantity=1,
            price_at_time=50000
        )
        response_purchased = self.client_auth.get(reverse('catalog:download_digital_item', args=[self.v_cookbook_download.id]))
        self.assertEqual(response_purchased.status_code, 200)
        self.assertEqual(response_purchased['Content-Type'], 'text/plain; charset=utf-8')
        self.assertIn('attachment', response_purchased['Content-Disposition'])
        self.assertIn('THE COOKING NURSE - DIGITAL DOWNLOAD', b"".join(response_purchased.streaming_content).decode('utf-8'))

    def test_23_online_course_video_player_access_control(self):
        """Test 23: E-learning course player access control gating."""
        # 1. Unauthenticated user should be redirected to login
        response = self.client_unauth.get(reverse('classes:online_class_player', args=[self.course_sourdough.slug]))
        self.assertEqual(response.status_code, 302)

        # 2. Authenticated user who has not purchased the course should receive 404
        response_unpurchased = self.client_auth.get(reverse('classes:online_class_player', args=[self.course_sourdough.slug]))
        self.assertEqual(response_unpurchased.status_code, 404)

        # 3. Authenticated user who has purchased the course should successfully access the video player template
        order = Order.objects.create(user=self.client_user, total_amount=85000)
        OrderItem.objects.create(
            order=order,
            online_course=self.course_sourdough,
            quantity=1,
            price_at_time=85000
        )
        response_purchased = self.client_auth.get(reverse('classes:online_class_player', args=[self.course_sourdough.slug]))
        self.assertEqual(response_purchased.status_code, 200)
        self.assertContains(response_purchased, 'Artisanal Sourdough &amp; Gut Health')
        self.assertContains(response_purchased, 'mixkit-cooking-in-a-modern-kitchen')

    def test_24_checkout_map_coordinates_persistence(self):
        """Test 24: Persisting Kampala delivery Leaflet map coordinates during checkout."""
        # 1. Add physical item to client's cart
        self.client_auth.post(reverse('cart:cart_add', args=['variant', self.v_tomatoes_1kg.id]), {'quantity': 1})

        # 2. Complete checkout with custom coordinates
        response = self.client_auth.post(reverse('orders:checkout'), {
            'city': 'Kampala',
            'neighborhood': 'Nakasero',
            'street_address': 'Plot 10, Kyadondo Road',
            'delivery_notes': 'Please drop at security gate.',
            'latitude': '0.319523',
            'longitude': '32.576123'
        })
        
        # Verify checkout redirects to order success page
        new_order = Order.objects.filter(user=self.client_user).latest('id')
        self.assertRedirects(response, reverse('orders:success', args=[new_order.id]))
        
        # Verify coordinates were correctly saved in the database
        self.assertEqual(float(new_order.latitude), 0.319523)
        self.assertEqual(float(new_order.longitude), 32.576123)
