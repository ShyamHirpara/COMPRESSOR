import os
import shutil
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.core.files.base import ContentFile
from django.core.files import File
from PIL import Image

# Disable DecompressionBombWarning for large images
Image.MAX_IMAGE_PIXELS = None

from .models import CompressedImage

def compress_image_logic(input_path, output_path, level='normal', output_format='JPEG'):
    """
    Compresses an image based on the selected level and output format.
    """
    try:
        img = Image.open(input_path)
        
        # Define settings based on level
        if level == 'ultra':
            target_size_mb = 0.2  # 200KB
            max_dimension = 1200
            quality_range = (30, 60)
            best_quality = 40
        elif level == 'super':
            target_size_mb = 0.5  # 500KB
            max_dimension = 2000
            quality_range = (50, 80)
            best_quality = 65
        else: # normal
            target_size_mb = 2.0  # 2MB
            max_dimension = 4000
            quality_range = (75, 95)
            best_quality = 85

        # Resize if too large
        if max(img.size) > max_dimension:
            scale = max_dimension / max(img.size)
            new_size = (int(img.size[0] * scale), int(img.size[1] * scale))
            img = img.resize(new_size, Image.Resampling.LANCZOS)

        # Handle format specific conversions
        if output_format.upper() == 'JPEG':
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            save_format = 'JPEG'
        elif output_format.upper() == 'PNG':
            save_format = 'PNG'
        elif output_format.upper() == 'WEBP':
            save_format = 'WEBP'
        else:
            save_format = 'JPEG'
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

        # Binary search for quality (Mainly for JPEG/WEBP)
        if save_format in ['JPEG', 'WEBP']:
            low, high = quality_range
            target_bytes = target_size_mb * 1024 * 1024
            
            # Initial attempt
            img.save(output_path, save_format, quality=best_quality, optimize=True)
            
            if os.path.getsize(output_path) > target_bytes:
                 for _ in range(3): 
                    quality = (low + high) // 2
                    img.save(output_path, save_format, quality=quality, optimize=True)
                    if os.path.getsize(output_path) < target_bytes:
                        best_quality = quality
                        low = quality + 1
                    else:
                        high = quality - 1
                 # Final save
                 img.save(output_path, save_format, quality=best_quality, optimize=True)
        else:
            # PNG
            img.save(output_path, save_format, optimize=True)
            
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def index(request):
    context = {}
    
    # 1. Handle POST (Upload)
    if request.method == 'POST' and request.FILES.get('image'):
        try:
            uploaded_file = request.FILES['image']
            level = request.POST.get('level', 'normal')
            output_format = request.POST.get('format', 'JPEG').upper() 
            
            # Only accept JPG/JPEG input
            name, ext = os.path.splitext(uploaded_file.name)
            if ext.lower() not in ['.jpg', '.jpeg']:
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                     return JsonResponse({'error': "Only JPEG/JPG input is supported."}, status=400)
                context['error'] = "Only JPEG/JPG input is supported."
                return render(request, 'web_compressor/index.html', context)

            # Ensure MEDIA_ROOT is str and temp dir exists
            media_root_str = str(settings.MEDIA_ROOT)
            temp_dir = os.path.join(media_root_str, 'temp')
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)

            fs = FileSystemStorage(location=temp_dir, base_url='/media/temp/')
            filename = fs.save(uploaded_file.name, uploaded_file)
            uploaded_file_path = fs.path(filename)
            uploaded_file_url = fs.url(filename)

            results = []
            
            format_map = {
                'JPEG': {'ext': '.jpg', 'label': 'JPG'},
                'PNG': {'ext': '.png', 'label': 'PNG'},
                'WEBP': {'ext': '.webp', 'label': 'WEBP'}
            }
            
            target_fmt = format_map.get(output_format, format_map['JPEG'])

            out_filename = f"{name}_{level}_compressed{target_fmt['ext']}"
            out_path = os.path.join(temp_dir, out_filename)
            
            success = compress_image_logic(uploaded_file_path, out_path, level=level, output_format=output_format)
            
            if success:
                file_size_bytes = os.path.getsize(out_path)
                file_size_mb = file_size_bytes / (1024*1024)
                file_size_text = f"{file_size_mb:.2f} MB"
                
                final_url = fs.url(out_filename)
                
                # If User is logged in, save to DB
                if request.user.is_authenticated:
                    # Delete ALL previous images for this user
                    previous_images = CompressedImage.objects.filter(user=request.user)
                    for img in previous_images:
                        img.delete()

                    with open(out_path, 'rb') as f:
                        compressed_obj = CompressedImage(
                            user=request.user,
                            original_filename=out_filename,
                            size_text=file_size_text,
                            format=target_fmt['label']
                        )
                        compressed_obj.image.save(out_filename, File(f), save=True)
                        final_url = compressed_obj.image.url
                    
                    if os.path.exists(out_path):
                        os.remove(out_path)

                results.append({
                    'format': target_fmt['label'],
                    'url': final_url,
                    'size': file_size_text,
                    'filename': out_filename
                })

            # Cleanup input file
            if os.path.exists(uploaded_file_path):
                os.remove(uploaded_file_path)
                
            response_data = {
                'original_url': uploaded_file_url,
                'original_size': f"{uploaded_file.size / (1024*1024):.2f} MB",
                'level': level.capitalize(),
                'results': results
            }
            
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse(response_data)
            
            context.update(response_data)

        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"Server Error: {e}")
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                 return JsonResponse({'error': f"Server Error: {str(e)}"}, status=500)
            context['error'] = "An error occurred during compression."

    return render(request, 'web_compressor/index.html', context)

def upload_temp_image_view(request):
    if request.method == 'POST' and request.FILES.get('image'):
        try:
            media_root_str = str(settings.MEDIA_ROOT)
            temp_dir = os.path.join(media_root_str, 'temp')
            
            # 1. Clear previous uploaded image for this session
            previous_filename = request.session.get('uploaded_filename')
            if previous_filename:
                prev_path = os.path.join(temp_dir, previous_filename)
                if os.path.exists(prev_path):
                     try:
                        os.remove(prev_path)
                     except Exception as e:
                        print(f"Error deleting previous file: {e}")

            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)

            # 2. General Cleanup: Remove temp files older than 1 hour (3600 seconds)
            try:
                import time
                current_time = time.time()
                one_hour_ago = current_time - 3600
                
                if os.path.exists(temp_dir):
                    for f in os.listdir(temp_dir):
                        f_path = os.path.join(temp_dir, f)
                        if os.path.isfile(f_path):
                            creation_time = os.path.getctime(f_path)
                            if creation_time < one_hour_ago:
                                try:
                                    os.remove(f_path)
                                except OSError:
                                    pass 
            except Exception as cleanup_error:
                print(f"Cleanup warning: {cleanup_error}")

            uploaded_file = request.FILES['image']
            name, ext = os.path.splitext(uploaded_file.name)
            if ext.lower() not in ['.jpg', '.jpeg']:
                return JsonResponse({'error': "Only JPEG/JPG input is supported."}, status=400)

            fs = FileSystemStorage(location=temp_dir, base_url='/media/temp/')
            # Save using a unique name to prevent collisions if needed, or rely on fs handles
            filename = fs.save(uploaded_file.name, uploaded_file)
            
            # Store filename in session to track for deletion on next upload
            request.session['uploaded_filename'] = filename
            
            return JsonResponse({'filename': filename})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def compress_view(request):
    if request.method == 'POST':
        try:
            filename = request.POST.get('filename')
            level = request.POST.get('level', 'normal')
            output_format = request.POST.get('format', 'JPEG').upper()

            if not filename:
                return JsonResponse({'error': 'No file specified'}, status=400)

            # Security: Ensure filename is just a name, no paths
            filename = os.path.basename(filename)
            
            media_root_str = str(settings.MEDIA_ROOT)
            temp_dir = os.path.join(media_root_str, 'temp')
            input_path = os.path.join(temp_dir, filename)

            if not os.path.exists(input_path):
                return JsonResponse({'error': 'File not found or expired'}, status=404)

            # Prepare output
            name, ext = os.path.splitext(filename)
            
            format_map = {
                'JPEG': {'ext': '.jpg', 'label': 'JPG'},
                'PNG': {'ext': '.png', 'label': 'PNG'},
                'WEBP': {'ext': '.webp', 'label': 'WEBP'}
            }
            target_fmt = format_map.get(output_format, format_map['JPEG'])
            out_filename = f"{name}_{level}_compressed{target_fmt['ext']}"
            out_path = os.path.join(temp_dir, out_filename)
            
            # Compress
            success = compress_image_logic(input_path, out_path, level=level, output_format=output_format)
            final_url = ''
            file_size_text = ''

            if success:
                fs = FileSystemStorage(location=temp_dir, base_url='/media/temp/')
                file_size_bytes = os.path.getsize(out_path)
                file_size_mb = file_size_bytes / (1024*1024)
                file_size_text = f"{file_size_mb:.2f} MB"
                final_url = fs.url(out_filename)
                
                # Cleanup previous compressed files for this session if needed
                # For now we rely on the implementation where only one upload is active per session usually
                
                # IMPORTANT: We do NOT delete the input file here anymore, 
                # because the user might want to re-compress the same uploaded image with different settings.
                # The input file is cleaned up when a NEW file is uploaded (in upload_temp_image_view).

                return JsonResponse({
                    'results': [{
                        'format': target_fmt['label'],
                        'url': final_url,
                        'size': file_size_text,
                        'filename': out_filename
                    }]
                })
            else:
                return JsonResponse({'error': 'Compression failed'}, status=500)
                
        except Exception as e:
            import traceback
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=500)
            
    return JsonResponse({'error': 'Invalid request'}, status=400)

from django.core.mail import send_mail

def contact_view(request):
    return render(request, 'web_compressor/contact.html')

def about_view(request):
    return render(request, 'web_compressor/about.html')


