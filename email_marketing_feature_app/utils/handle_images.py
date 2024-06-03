import re
import base64
import uuid
import os
from django.conf import settings

# Constantes para patrones de regex
IMG_PATTERN = re.compile(r'<img src="data:image/(png|jpeg|jpg);base64,([^"]+)"')
IMG_TAG_PATTERN = re.compile(r'<img src="(cid[^"]+)"(.*?)>')

def decode_base64_image(img_str):
    """
    Decodes a base64 encoded image string.
    
    Args:
        img_str (str): The base64 encoded image string.
        
    Returns:
        bytes: The decoded image data.
    """
    return base64.b64decode(img_str)

def save_image(img_data, format):
    """
    Saves the image data to a file in the MEDIA_ROOT directory.
    
    Args:
        img_data (bytes): The image data.
        format (str): The image format (e.g., 'png', 'jpeg', 'jpg').
        
    Returns:
        str: The name of the saved image file.
    """
    img_name = f'{uuid.uuid4()}.{format}'
    img_path = os.path.join(settings.MEDIA_ROOT, 'email_images', img_name)
    os.makedirs(os.path.dirname(img_path), exist_ok=True)
    with open(img_path, 'wb') as img_file:
        img_file.write(img_data)
    return img_name

def replace_image_sources(content, img_name, img_str, format):
    """
    Replaces base64 encoded image sources with actual URLs and content IDs.
    
    Args:
        content (str): The original content containing base64 images.
        img_name (str): The name of the saved image file.
        img_str (str): The base64 encoded image string.
        format (str): The image format.
        
    Returns:
        tuple: Content with URLs replaced and content with CIDs replaced.
    """
    img_url = f'{settings.MEDIA_URL}email_images/{img_name}'
    full_img_url = f'{settings.SITE_URL}{img_url}'
    cid = f'cid:{img_name}'
    
    content_without_cid = content.replace(f'data:image/{format};base64,{img_str}', full_img_url)
    content_with_cid = content.replace(f'data:image/{format};base64,{img_str}', cid)
    
    return content_without_cid, content_with_cid

def add_links_to_images(content_with_cid):
    """
    Adds links to images in the content.
    
    Args:
        content_with_cid (str): The content with image content IDs.
        
    Returns:
        str: The content with images wrapped in links.
    """
    content_with_cid_links = content_with_cid
    for match in IMG_TAG_PATTERN.finditer(content_with_cid):
        img_src = match.group(1)
        img_attrs = match.group(2)
        page_url = 'http://127.0.0.1:5173/'
        replacement_html = f'<a href="{page_url}"><img src="{img_src}" {img_attrs}></a>'
        content_with_cid_links = content_with_cid_links.replace(match.group(0), replacement_html)
    return content_with_cid_links

def handle_images(content):
    """
    Handles embedded images in the content by saving them as files and replacing their sources.
    
    Args:
        content (str): The original content containing base64 images.
        
    Returns:
        tuple: The content without content IDs, the content with image links, and a list of image details.
    """
    matches = IMG_PATTERN.findall(content)
    images = []

    if not matches:
        return content, content, images

    for format, img_str in matches:
        img_data = decode_base64_image(img_str)
        img_name = save_image(img_data, format)
        
        content_without_cid, content_with_cid = replace_image_sources(content, img_name, img_str, format)
        content_with_cid_links = add_links_to_images(content_with_cid)
        
        images.append((img_name, img_data, f'cid:{img_name}'))
    
    return content_without_cid, content_with_cid_links, images
