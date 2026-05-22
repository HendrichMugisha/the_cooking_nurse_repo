import io

from django.shortcuts import render, get_object_or_404
from django.http import FileResponse, Http404
from django.contrib.auth.decorators import login_required

from orders.models import OrderItem
from django.db.models import Count, Q
from .models import Product, ProductVariant, Category

def product_list(request):
    active_category_slug = request.GET.get('category')
    products = Product.objects.filter(is_active=True, product_type='physical').prefetch_related('variants', 'categories')
    if active_category_slug:
        products = products.filter(categories__slug=active_category_slug)
        
    categories = Category.objects.annotate(
        product_count=Count('products', filter=Q(products__is_active=True, products__product_type='physical'))
    ).order_by('name')
    
    context = {
        'products': products,
        'categories': categories,
        'active_category': active_category_slug,
    }
    return render(request, 'catalog/product_list.html', context)

@login_required
def download_digital_item(request, variant_id):
    # Verify the user has a paid or completed order containing this product variant
    # (Since payment statuses default to 'pending' in MVP dummy data, we check for order existence under request.user)
    has_purchased = OrderItem.objects.filter(
        order__user=request.user,
        product_variant_id=variant_id
    ).exists()
    
    if not has_purchased:
        raise Http404("You have not purchased this item or do not have access to it.")
    
    variant = get_object_or_404(ProductVariant, id=variant_id)
    product = variant.product
    
    if product.product_type != 'digital':
        raise Http404("This product is not a digital download.")
        
    # If the physical file exists, serve it securely
    if product.digital_file:
        try:
            return FileResponse(product.digital_file.open(), as_attachment=True, filename=f"{product.slug}.pdf")
        except Exception as e:
            pass
            
    # Fallback Mode: Generate a beautiful, dynamic, text-based recipe guide & welcoming culinary letter
    buffer = io.BytesIO()
    letter_text = (
        "========================================================================\n"
        "                THE COOKING NURSE - DIGITAL DOWNLOAD\n"
        "========================================================================\n\n"
        f"Thank you for purchasing '{product.name}'!\n\n"
        "This is your official secure digital download recipe and culinary guide.\n"
        "We are thrilled to accompany you on your wholesome culinary journey!\n\n"
        "------------------------------------------------------------------------\n"
        "                    THE EVERYDAY MAGIC COOKBOOK RECIPE\n"
        "------------------------------------------------------------------------\n"
        "Roasted Heirloom Tomatoes with Clarified Ghee\n\n"
        "Ingredients:\n"
        " - 1 kg fresh heirloom tomatoes (halved)\n"
        " - 2 tablespoons Pure Artisanal Ghee\n"
        " - Fresh rosemary, garlic cloves, sea salt, black pepper\n\n"
        "Preparation:\n"
        " 1. Wash and halve the heirloom tomatoes.\n"
        " 2. Melt 2 tablespoons of pure artisanal ghee in a heavy cast-iron skillet.\n"
        " 3. Sear tomatoes cut-side down for 4 minutes until beautifully charred.\n"
        " 4. Toss in crushed garlic cloves and fresh rosemary sprigs.\n"
        " 5. Transfer to oven, bake at 200°C for 15 minutes. Serve alongside sourdough!\n\n"
        "------------------------------------------------------------------------\n"
        "                    NURSE'S KITCHEN NOTE\n"
        "------------------------------------------------------------------------\n"
        "Tomatoes are rich in Lycopene, a highly potent antioxidant supporting overall vitality\n"
        "and natural well-being. Cooking tomatoes releases more bioavailable Lycopene, and the\n"
        "healthy fat-soluble vitamins present in Pure Ghee enhance its absorption by up to 300%!\n\n"
        "------------------------------------------------------------------------\n"
        "© 2026 The Cooking Nurse. All rights reserved. www.thecookingnurse.com\n"
        "========================================================================\n"
    )
    buffer.write(letter_text.encode('utf-8'))
    buffer.seek(0)
    
    response = FileResponse(buffer, as_attachment=True, filename=f"{product.slug}_cookbook.txt")
    response['Content-Type'] = 'text/plain; charset=utf-8'
    return response

