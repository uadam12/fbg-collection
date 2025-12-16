import os
from PIL import Image
from io import BytesIO
from typing import Tuple, Union
from django.templatetags.static import static
from django.core.files.base import ContentFile
from django.core.files import File


def compress_image(
    image,
    max_size: Tuple[int, int] = (800, 800),
    quality: int = 75,
    format: str = "JPEG"
) -> ContentFile:
    """
    Compress and resize an image.
    Returns a Django ContentFile suitable for ImageField.
    
    Args:
        image: Uploaded file or ImageField file
        max_size: Maximum (width, height)
        quality: JPEG quality (1-95)
        format: Output format (JPEG, PNG, etc.)
    """
    img = Image.open(image)

    # Convert to RGB if needed
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    # Resize while maintaining aspect ratio
    img.thumbnail(max_size, Image.LANCZOS)

    buffer = BytesIO()
    img.save(buffer, format=format, quality=quality, optimize=True)
    buffer.seek(0)

    return ContentFile(buffer.read(), name=image.name)


def delete_file(file_field) -> None:
    """
    Safely delete a file from storage.
    """
    if not file_field: return

    try:
        if os.path.isfile(file_field.path):
            os.remove(file_field.path)
    except (ValueError, FileNotFoundError):
        # File might not exist or path is invalid
        pass


def delete_old_file(instance, field_name: str, new_file) -> None:
    """
    Deletes the old file from storage if a new file is uploaded.

    Args:
        instance: Model instance
        field_name: Name of the ImageField
        new_file: New uploaded file
    """
    if not instance.pk:
        return

    try:
        old_file = getattr(instance.__class__.objects.get(pk=instance.pk), field_name)
    except instance.__class__.DoesNotExist:
        return

    if old_file and old_file != new_file:
        delete_file(old_file)


def get_file(image: Union[File, None], default_image: str) -> str:
    """
    Returns the URL of the given image if it exists.
    If no image is uploaded or the file is missing, returns the default static image URL.

    Args:
        image: ImageField file or None
        default_image: Filename of the default image in 'static/imgs/'

    Returns:
        URL string
    """
    if image and hasattr(image, 'url'):
        try:
            # Check if file exists on the filesystem
            if hasattr(image, 'path') and os.path.isfile(image.path):
                return image.url
        except (ValueError, OSError):
            pass

    return static(f"imgs/{default_image}")
