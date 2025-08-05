# Hướng dẫn Setup Domain cho Twin AI Docs

## 📧 Thông tin cần thiết
- **Project**: Twin AI Documentation
- **Vercel URL hiện tại**: [URL tự động từ Vercel]
- **Domain mục tiêu**: [Điền domain muốn setup]

## ✅ Checklist cho Partner

### Bước 1: Truy cập Project
- [ ] Đăng nhập Vercel
- [ ] Tìm project "Twin AI Docs" trong dashboard
- [ ] Vào tab **Settings** → **Domains**

### Bước 2: Thêm Domain
- [ ] Nhấn **"Add Domain"**
- [ ] Nhập domain (ví dụ: `docs.twinai.com`)
- [ ] Nhấn **"Add"**

### Bước 3: Cấu hình DNS
**Nếu là Subdomain (docs.twinai.com):**
```
Type: CNAME
Name: docs
Value: cname.vercel-dns.com
TTL: Auto hoặc 300
```

**Nếu là Root Domain (twinai.com):**
```
Type: A
Name: @ (hoặc để trống)
Value: 76.76.19.61
TTL: Auto hoặc 300
```

### Bước 4: Verify Domain
- [ ] Chờ DNS propagation (5-30 phút)
- [ ] Vercel sẽ tự động verify
- [ ] Check SSL certificate được tạo tự động

### Bước 5: Kiểm tra
- [ ] Truy cập domain mới
- [ ] Kiểm tra HTTPS hoạt động
- [ ] Test các link internal

## 🚨 Lưu ý quan trọng

1. **DNS Propagation**: Có thể mất 5-30 phút để domain hoạt động
2. **SSL Certificate**: Vercel tự động tạo, có thể mất vài phút
3. **Wildcard Domain**: Nếu cần `*.twinai.com`, setup riêng
4. **Redirect**: Có thể setup redirect từ domain cũ sang mới

## 🆘 Troubleshooting

**Lỗi thường gặp:**
- DNS chưa propagate → Chờ thêm
- SSL pending → Chờ Vercel tạo certificate
- Domain không resolve → Kiểm tra DNS settings

**Kiểm tra DNS:**
```bash
nslookup docs.twinai.com
dig docs.twinai.com
```

## 📞 Liên hệ hỗ trợ
Nếu gặp vấn đề, liên hệ:
- Vercel Support: vercel.com/support
- Hoặc ping owner project

---
*Cập nhật lần cuối: [Date]*
