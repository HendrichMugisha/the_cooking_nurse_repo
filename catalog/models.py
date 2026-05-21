from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):
    PRODUCT_TYPES = (
        ('physical', 'Physical Product (Groceries)'),
        ('digital', 'Digital Product (Cookbook/Recipe)'),
    )

    category = models.ForeignKey(Category, related_name='products', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    product_type = models.CharField(max_length=10, choices=PRODUCT_TYPES, default='physical')
    description = models.TextField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    
    # Only used if product_type is 'digital'
    digital_file = models.FileField(upload_to='digital_products/', blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ProductVariant(models.Model):
    """
    Holds the actual price and stock. 
    Even a simple product gets at least one 'Default' variant.
    """
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, help_text="e.g., '500ml', '1 Kg', or 'Default'")
    sku = models.CharField(max_length=50, unique=True, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=0, help_text="Price in UGX")
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} - {self.name}"

    @property
    def is_in_stock(self):
        return self.stock > 0 or self.product.product_type == 'digital'
