import os

if 'CLOUDINARY_URL' in os.environ:
    from cloudinary_storage.storage import MediaCloudinaryStorage

    class AutoMediaCloudinaryStorage(MediaCloudinaryStorage):
        # Setting RESOURCE_TYPE to 'auto' tells Cloudinary to automatically detect
        # if the uploaded file is an image, video (.mp4), or raw file (.pdf).
        # This prevents the 500 error when uploading non-image files via FileField.
        RESOURCE_TYPE = 'auto'
