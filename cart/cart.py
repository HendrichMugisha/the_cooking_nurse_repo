from decimal import Decimal
from django.conf import settings
from catalog.models import ProductVariant
from classes.models import Course, ClassSession

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, item, item_type, quantity=1, update_quantity=False):
        # item_id is always string in session dict
        item_id = str(item.id)
        cart_key = f"{item_type}_{item_id}"
        
        # Determine price based on item type
        price = item.course.price if item_type == 'session' else item.price
        
        if cart_key not in self.cart:
            self.cart[cart_key] = {
                'quantity': 0,
                'price': str(price),
                'type': item_type,
                'id': item.id
            }
            
        if update_quantity:
            self.cart[cart_key]['quantity'] = quantity
        else:
            self.cart[cart_key]['quantity'] += quantity
            
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, item_type, item_id):
        cart_key = f"{item_type}_{item_id}"
        if cart_key in self.cart:
            del self.cart[cart_key]
            self.save()

    def __iter__(self):
        cart = self.cart.copy()
        
        # Fetch actual objects from DB to render in the cart page
        variant_ids = [item['id'] for item in cart.values() if item['type'] == 'variant']
        online_ids = [item['id'] for item in cart.values() if item['type'] == 'online']
        session_ids = [item['id'] for item in cart.values() if item['type'] == 'session']
        
        variants = ProductVariant.objects.filter(id__in=variant_ids)
        onlines = Course.objects.filter(id__in=online_ids)
        sessions = ClassSession.objects.filter(id__in=session_ids)
        
        for variant in variants:
            cart[f"variant_{variant.id}"]['item'] = variant
        for online in onlines:
            cart[f"online_{online.id}"]['item'] = online
        for session in sessions:
            cart[f"session_{session.id}"]['item'] = session
            # sessions use the course price
            cart[f"session_{session.id}"]['price'] = str(session.course.price)
            
        for item in cart.values():
            if 'item' in item: # Ensure object was found in DB
                item['price'] = Decimal(item['price'])
                item['total_price'] = item['price'] * item['quantity']
                yield item

    def __len__(self):
        """Count total items in cart."""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
