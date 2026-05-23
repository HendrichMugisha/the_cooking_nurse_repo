import os
from django.core.files.storage import default_storage

if 'CLOUDINARY_URL' in os.environ:
    from cloudinary_storage.storage import MediaCloudinaryStorage, VideoMediaCloudinaryStorage, RawMediaCloudinaryStorage

    class AutoMediaCloudinaryStorage(MediaCloudinaryStorage):
        pass

    def select_video_storage():
        return VideoMediaCloudinaryStorage()

    def select_raw_storage():
        return RawMediaCloudinaryStorage()
else:
    class AutoMediaCloudinaryStorage(default_storage.__class__):
        pass

    def select_video_storage():
        return default_storage

    def select_raw_storage():
        return default_storage
