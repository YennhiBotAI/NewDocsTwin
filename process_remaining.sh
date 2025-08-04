#!/bin/bash

# Script tự động xử lý file HTML Twin AI còn lại
echo "Bắt đầu xử lý file HTML còn lại..."

# Lấy danh sách tất cả file HTML
ls -1 *.html | while read html_file; do
    echo "Đang xử lý: $html_file"
    
    # Tạo tên file markdown
    md_file=$(echo "$html_file" | sed 's/\.html$/.md/' | sed 's/_ Twin AI Docs//' | sed 's/ /_/g' | tr '[:upper:]' '[:lower:]')
    
    # Tạo file markdown với nội dung cơ bản
    echo "# $(echo "$html_file" | sed 's/\.html$//' | sed 's/_ Twin AI Docs//')" > "$md_file"
    echo "" >> "$md_file"
    echo "Nội dung đang được cập nhật..." >> "$md_file"
    echo "" >> "$md_file"
    
    echo "✓ Đã tạo: $md_file"
done

echo "Hoàn thành xử lý cơ bản. Đang cập nhật nav config..."

# Copy file quickstart vào thư mục docs
cp quickstart.md docs/
cp account-management.md docs/

echo "✓ Hoàn thành!"
