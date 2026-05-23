import os
import sys
import traceback

if 'CLOUDINARY_URL' in os.environ:
    from cloudinary_storage.storage import MediaCloudinaryStorage

    class AutoMediaCloudinaryStorage(MediaCloudinaryStorage):
        RESOURCE_TYPE = 'auto'

        def url(self, name):
            url = super().url(name)
            if url and '/auto/upload/' in url:
                ext = os.path.splitext(name)[1].lower()
                if ext in ['.mp4', '.mov', '.avi', '.webm']:
                    url = url.replace('/auto/upload/', '/video/upload/')
                elif ext in ['.pdf', '.zip', '.csv', '.doc', '.docx']:
                    url = url.replace('/auto/upload/', '/raw/upload/')
                else:
                    url = url.replace('/auto/upload/', '/image/upload/')
            return url

        def _save(self, name, content):
            print(f"\n[UPLOAD] ===== Cloudinary Upload Starting =====", file=sys.stderr)
            print(f"[UPLOAD] File name: {name}", file=sys.stderr)
            print(f"[UPLOAD] Content type: {type(content)}", file=sys.stderr)
            print(f"[UPLOAD] Has .size attr: {hasattr(content, 'size')}", file=sys.stderr)
            print(f"[UPLOAD] Has .file attr: {hasattr(content, 'file')}", file=sys.stderr)
            try:
                size = content.size
                print(f"[UPLOAD] File size: {size} bytes", file=sys.stderr)
            except Exception as size_err:
                print(f"[UPLOAD] WARNING: Could not read .size: {size_err}", file=sys.stderr)
            try:
                print(f"[UPLOAD] Calling parent _save()...", file=sys.stderr)
                result = super()._save(name, content)
                print(f"[UPLOAD] SUCCESS: File saved as: {result}", file=sys.stderr)
                print(f"[UPLOAD] ==========================================\n", file=sys.stderr)
                return result
            except Exception as e:
                print(f"\n[UPLOAD] !!!!!!!!!! CLOUDINARY UPLOAD FAILED !!!!!!!!!!", file=sys.stderr)
                print(f"[UPLOAD] Error type: {type(e).__name__}", file=sys.stderr)
                print(f"[UPLOAD] Error message: {str(e)}", file=sys.stderr)
                print(f"[UPLOAD] Full traceback:", file=sys.stderr)
                traceback.print_exc(file=sys.stderr)
                print(f"[UPLOAD] !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n", file=sys.stderr)
                raise
