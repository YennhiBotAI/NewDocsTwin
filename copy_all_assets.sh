#!/bin/bash

# Script to copy all images and assets from _files directories

echo "Copying images and assets..."

# Create assets directory
mkdir -p docs/public/assets

# Find all image files in _files directories and copy them
find . -name "*_files" -type d | while read dir; do
    echo "Processing directory: $dir"
    
    # Copy images (various formats)
    find "$dir" -type f \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" -o -name "*.gif" -o -name "*.svg" -o -name "image*" \) | while read img; do
        filename=$(basename "$img")
        # Create unique filename to avoid conflicts
        dirname_clean=$(echo "$dir" | sed 's/[^a-zA-Z0-9]/_/g')
        new_filename="${dirname_clean}_${filename}"
        
        echo "Copying image: $img -> docs/public/assets/$new_filename"
        cp "$img" "docs/public/assets/$new_filename" 2>/dev/null || echo "Failed to copy $img"
    done
    
    # Copy CSS files
    find "$dir" -name "*.css" | while read css; do
        filename=$(basename "$css")
        dirname_clean=$(echo "$dir" | sed 's/[^a-zA-Z0-9]/_/g')
        new_filename="${dirname_clean}_${filename}"
        
        echo "Copying CSS: $css -> docs/public/assets/$new_filename"
        cp "$css" "docs/public/assets/$new_filename" 2>/dev/null || echo "Failed to copy $css"
    done
done

echo "Done copying assets!"
