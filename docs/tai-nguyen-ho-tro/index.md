# 6. TÀI NGUYÊN & HỖ TRỢ

Đây là trung tâm hỗ trợ, nơi người dùng có thể tìm thấy câu trả lời cho các câu hỏi, các kênh liên lạc và các tài nguyên bổ sung.

<div class="grid-container">
  <div class="resource-card">
    <h3>
      <a href="./cac-cau-hoi-thuong-gap-faqs" class="card-link">
        <strong>Các câu hỏi thường gặp (FAQs)</strong>
      </a>
    </h3>
    <p>Tìm câu trả lời nhanh cho những thắc mắc phổ biến nhất về Twin AI</p>
  </div>

  <div class="resource-card">
    <h3>
      <a href="./cac-kenh-ho-tro" class="card-link">
        <strong>Các kênh hỗ trợ</strong>
      </a>
    </h3>
    <p>Các cách để liên hệ với đội ngũ Twin AI khi bạn cần sự trợ giúp</p>
  </div>

  <div class="resource-card">
    <h3>
      <a href="./bang-thuat-ngu" class="card-link">
        <strong>Bảng thuật ngữ</strong>
      </a>
    </h3>
    <p>Giải thích các thuật ngữ và khái niệm chính được sử dụng trong Twin AI</p>
  </div>
</div>

<style>
.grid-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin: 2rem 0;
}

.resource-card {
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-border);
  border-radius: 12px;
  padding: 1.5rem;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.resource-card:hover {
  border-color: var(--vp-c-brand);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.resource-card h3 {
  margin: 0 0 1rem 0;
  font-size: 1.2rem;
  font-weight: 600;
}

.card-link {
  text-decoration: none;
  color: var(--vp-c-text-1);
  transition: color 0.3s ease;
}

.card-link:hover {
  color: var(--vp-c-brand);
}

.resource-card p {
  margin: 0;
  color: var(--vp-c-text-2);
  line-height: 1.6;
}

.resource-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, var(--vp-c-brand), var(--vp-c-brand-light));
  opacity: 0;
  transition: opacity 0.3s ease;
}

.resource-card:hover::before {
  opacity: 1;
}

@media (max-width: 768px) {
  .grid-container {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .resource-card {
    padding: 1rem;
  }
}
</style>
