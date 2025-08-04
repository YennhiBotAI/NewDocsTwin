#!/usr/bin/env python3
import re
import glob
import urllib.parse
import subprocess
import os

def decode_url(encoded_url):
    """Decode URL encoded string"""
    return urllib.parse.unquote(encoded_url)

def extract_image_urls(html_files):
    """Extract all GitBook image URLs from HTML files"""
    urls = set()
    
    # Pattern to find encoded GitBook URLs
    pattern = r'url=([^&"\']*(?:\.png|\.jpg|\.jpeg)[^&"\']*)'
    
    for file in html_files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                matches = re.findall(pattern, content)
                for match in matches:
                    if '4266852894-files.gitbook.io' in match:
                        decoded = decode_url(match)
                        urls.add(decoded)
        except Exception as e:
            print(f"Error reading {file}: {e}")
    
    return sorted(urls)

def get_filename_from_url(url):
    """Extract filename from URL"""
    # Extract the upload ID and filename from the URL
    parts = url.split('/')
    for i, part in enumerate(parts):
        if part == 'uploads' and i + 1 < len(parts):
            upload_id = parts[i + 1]
            if i + 2 < len(parts):
                filename_part = parts[i + 2]
                # Extract filename before ?alt=media
                filename = filename_part.split('?')[0]
                # URL decode the filename
                filename = decode_url(filename)
                return filename
    return 'unknown.png'

def download_image(url, filename, output_dir):
    """Download image using curl"""
    output_path = os.path.join(output_dir, filename)
    try:
        cmd = ['curl', '-o', output_path, url]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ Downloaded: {filename}")
            return True
        else:
            print(f"✗ Failed to download {filename}: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ Error downloading {filename}: {e}")
        return False

def main():
    # Find all HTML files
    html_files = glob.glob('*.html')
    print(f"Found {len(html_files)} HTML files")
    
    # Extract image URLs
    print("Extracting image URLs...")
    urls = extract_image_urls(html_files)
    print(f"Found {len(urls)} unique image URLs")
    
    # Create images directory if it doesn't exist
    images_dir = 'docs/images'
    os.makedirs(images_dir, exist_ok=True)
    
    # Download each image
    print("\nDownloading images...")
    for url in urls:
        filename = get_filename_from_url(url)
        print(f"URL: {url}")
        print(f"Filename: {filename}")
        download_image(url, filename, images_dir)
        print()

if __name__ == "__main__":
    main()
