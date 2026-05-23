import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()
from portfolio.models import SiteSettings
s = SiteSettings.get_settings()
print("featured_youtube_embed_url:", repr(s.featured_youtube_embed_url))
print("youtube_url:", repr(s.youtube_url))
print("URL length:", len(s.featured_youtube_embed_url))
print("URL truthy:", bool(s.featured_youtube_embed_url))
