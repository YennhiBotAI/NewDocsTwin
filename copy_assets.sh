#!/bin/bash

# Tạo thư mục đích
mkdir -p /workspaces/NewDocsTwin/docs/images
mkdir -p /workspaces/NewDocsTwin/docs/videos

echo "Copying images and videos from HTML files..."

# Copy tất cả file ảnh (jpg, jpeg, png, svg)
find /workspaces/NewDocsTwin -name "*_files" -type d | while read dir; do
    echo "Processing directory: $dir"
    
    # Copy images
    find "$dir" -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" -o -name "*.svg" -o -name "image" -o -name "image(*)" \) | while read file; do
        filename=$(basename "$file")
        # Đổi tên file nếu cần để tránh trùng lặp
        if [[ -f "/workspaces/NewDocsTwin/docs/images/$filename" ]]; then
            # Tạo tên file unique
            dir_name=$(basename "$(dirname "$file")" | sed 's/ /_/g' | sed 's/[^a-zA-Z0-9_-]//g')
            new_filename="${dir_name}_${filename}"
            cp "$file" "/workspaces/NewDocsTwin/docs/images/$new_filename"
            echo "  Copied: $filename -> $new_filename"
        else
            cp "$file" "/workspaces/NewDocsTwin/docs/images/$filename"
            echo "  Copied: $filename"
        fi
    done
    
    # Copy video/html embeds
    find "$dir" -type f \( -name "*.html" -o -name "*.mp4" -o -name "*.webm" \) | while read file; do
        filename=$(basename "$file")
        if [[ -f "/workspaces/NewDocsTwin/docs/videos/$filename" ]]; then
            dir_name=$(basename "$(dirname "$file")" | sed 's/ /_/g' | sed 's/[^a-zA-Z0-9_-]//g')
            new_filename="${dir_name}_${filename}"
            cp "$file" "/workspaces/NewDocsTwin/docs/videos/$new_filename"
            echo "  Copied video: $filename -> $new_filename"
        else
            cp "$file" "/workspaces/NewDocsTwin/docs/videos/$filename"
            echo "  Copied video: $filename"
        fi
    done
done

echo "Asset copying completed!"
echo "Images in: /workspaces/NewDocsTwin/docs/images"
echo "Videos in: /workspaces/NewDocsTwin/docs/videos"

# List what we copied
echo ""
echo "Images copied:"
ls -la /workspaces/NewDocsTwin/docs/images/ | head -20

echo ""
echo "Videos copied:"
ls -la /workspaces/NewDocsTwin/docs/videos/ | head -10
