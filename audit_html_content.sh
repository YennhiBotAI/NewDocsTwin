#!/bin/bash

echo "Bắt đầu audit content từ HTML files..."

# Tìm và list tất cả HTML files
find . -name "*.html" -type f | while read -r file; do
    echo "=== Processing: $file ==="
    
    # Extract title từ filename
    filename=$(basename "$file")
    title=$(echo "$filename" | sed 's/_ _ Twin AI Docs\.html$//' | sed 's/_/ /g')
    
    echo "Title: $title"
    
    # Extract main content text (skip headers, scripts, styles)
    # Tìm text content chính trong HTML
    content=$(grep -oP '(?<=\>)[^<]+(?=\<)' "$file" | grep -v '^[[:space:]]*$' | grep -v '^[[:digit:]]*$' | grep -E '^[A-Za-zÀ-ỹ]' | head -20)
    
    echo "Sample content:"
    echo "$content" | head -5
    echo "---"
    echo
done

echo "Hoàn tất audit!"
