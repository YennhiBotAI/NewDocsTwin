# Hướng Dẫn Thiết Lập Webhook

Tài liệu này mô tả cách thiết lập webhook để tự động trigger build trên Vercel khi có commit mới vào repository GitHub gốc.

## Lấy Webhook URL từ Vercel

1. Đăng nhập vào [Vercel Dashboard](https://vercel.com/dashboard)
2. Chọn project Twin AI Docs
3. Vào **Settings > Git Integration**
4. Cuộn xuống phần **Deploy Hooks**
5. Nhấp vào **Create Hook**:
   - **Name**: GitHub Auto Deploy
   - **Branch**: main
   - Nhấp **Create Hook**
6. Lưu lại URL được tạo ra, có dạng: `https://api.vercel.com/v1/integrations/deploy/xxxx...`

## Thêm Webhook vào GitHub Repository Gốc

1. Đăng nhập vào GitHub với tài khoản có quyền admin trên repository gốc (https://github.com/BachKhoiMaoGia/NewDocsTwin)
2. Vào repository > **Settings** > **Webhooks** > **Add webhook**
3. Điền các thông tin:
   - **Payload URL**: [URL từ Vercel Deploy Hook]
   - **Content type**: `application/json`
   - **Secret**: [Để trống hoặc thiết lập secret tùy chọn]
   - **Which events would you like to trigger this webhook?**: Chỉ chọn `Push events`
   - **Active**: Đánh dấu chọn
4. Nhấp **Add webhook**

## Kiểm tra hoạt động

1. Thực hiện một commit và push lên repository gốc
2. Vào Vercel Dashboard > Twin AI Docs > Deployments
3. Một deployment mới sẽ tự động được kích hoạt

## Xử lý sự cố

Nếu webhook không hoạt động:

1. Kiểm tra lại URL Deploy Hook của Vercel
2. Xem tab **Recent Deliveries** trong phần Webhooks của GitHub để xem lỗi
3. Đảm bảo repository gốc có thể kết nối được với Vercel (không bị chặn bởi firewall)

## Bảo trì

- Kiểm tra hoạt động của webhook định kỳ
- Nếu cần thay đổi cấu hình build hoặc deployment, hãy cập nhật trong Vercel Dashboard

---

**Lưu ý**: Deploy Hook này chỉ trigger quá trình build và deploy, không đồng bộ code giữa repository Vercel và GitHub. Để đồng bộ hoàn toàn, bạn nên cấu hình GitHub App của Vercel với quyền truy cập đúng.
