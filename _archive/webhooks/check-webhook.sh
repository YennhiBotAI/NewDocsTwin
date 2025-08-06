#!/bin/bash
# Script kiểm tra hoạt động của webhook

echo "======================================="
echo "Kiểm tra Webhook từ GitHub đến Vercel"
echo "======================================="
echo ""

# Kiểm tra thông tin Deploy Hook
echo "Bạn đã cấu hình Deploy Hook trên Vercel chưa? (y/n)"
read has_deploy_hook

if [ "$has_deploy_hook" != "y" ]; then
  echo ""
  echo "⚠️ Hãy làm theo hướng dẫn để tạo Deploy Hook trước:"
  echo "1. Đăng nhập vào Vercel Dashboard"
  echo "2. Chọn project Twin AI Docs"
  echo "3. Vào Settings > Git Integration > Deploy Hooks"
  echo "4. Tạo hook mới với tên 'GitHub Auto Deploy' và branch 'main'"
  echo ""
  exit 1
fi

# Kiểm tra thông tin Webhook trên GitHub
echo ""
echo "Bạn đã cấu hình Webhook trên GitHub repository gốc chưa? (y/n)"
read has_github_webhook

if [ "$has_github_webhook" != "y" ]; then
  echo ""
  echo "⚠️ Hãy làm theo hướng dẫn để thêm webhook vào GitHub:"
  echo "1. Đăng nhập vào GitHub với tài khoản có quyền admin"
  echo "2. Vào repository > Settings > Webhooks > Add webhook"
  echo "3. Điền Payload URL bằng Deploy Hook URL từ Vercel"
  echo "4. Chọn Content type: application/json"
  echo "5. Chọn chỉ kích hoạt webhook cho Push events"
  echo ""
  exit 1
fi

# Kiểm tra trigger deploy
echo ""
echo "Bạn muốn kiểm tra webhook bằng cách tạo một commit test không? (y/n)"
read want_test

if [ "$want_test" == "y" ]; then
  echo ""
  echo "Tạo file test..."
  echo "This is a test file to trigger webhook: $(date)" > webhook-test.txt
  
  echo "Thêm và commit file..."
  git add webhook-test.txt
  git commit -m "test: trigger webhook deploy"
  
  echo "Push lên repository..."
  git push
  
  echo ""
  echo "✅ Đã push commit test. Kiểm tra Vercel Dashboard để xem deployment mới."
  echo "   URL: https://vercel.com/dashboard"
  echo ""
else
  echo ""
  echo "Bạn có thể kiểm tra webhook sau bằng cách:"
  echo "1. Tạo một thay đổi nhỏ trong repository"
  echo "2. Commit và push"
  echo "3. Kiểm tra Vercel Dashboard để xem deployment mới"
  echo ""
fi

echo "======================================"
echo "Cảm ơn đã sử dụng script kiểm tra webhook!"
echo "======================================"
