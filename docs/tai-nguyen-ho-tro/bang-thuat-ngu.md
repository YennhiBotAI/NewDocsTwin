# 6.3. Bảng thuật ngữ

Tài liệu tham khảo định nghĩa các thuật ngữ quan trọng trong Twin AI ecosystem. Perfect reference khi bạn gặp concepts mới.

## 🤖 AI & Machine Learning Terms

### **AI Expert / Twin AI Expert**
Một AI agent được training chuyên biệt cho một lĩnh vực cụ thể (ví dụ: Marketing Expert, Copywriter). Mỗi expert có knowledge base và capabilities riêng để đưa ra advice chất lượng cao trong domain của họ.

### **Prompt**
Câu hỏi, yêu cầu, hoặc instruction mà bạn gửi cho AI expert. Quality của prompt trực tiếp ảnh hưởng đến quality của response.

### **Context**
Thông tin background được cung cấp cùng với prompt để AI hiểu rõ hơn về situation, goals, constraints. Context càng chi tiết, response càng relevant.

### **Token**
Đơn vị đo lường text processing. Roughly 1 token ≈ 4 characters trong tiếng Việt. Được dùng để calculate usage và billing.

### **Fine-tuning**
Process training một AI model với data cụ thể để improve performance cho use case particular. Enterprise customers có thể fine-tune experts với company data.

### **Inference**
Process AI sử dụng trained model để generate response cho input mới. Mỗi lần bạn chat với expert = 1 inference.

### **Model Temperature**
Parameter kiểm soát creativity và randomness của AI responses. Lower temperature = consistent, higher temperature = more creative.

## 💬 Platform & Features

### **Conversation**
Một cuộc hội thoại giữa user và AI expert, bao gồm toàn bộ message history và context. AI nhớ conversation context để maintain coherence.

### **Thread**
Synonym với Conversation. Một chain of messages với cùng một expert về cùng một topic.

### **Project**
Container để organize multiple conversations, files, và team members around một mục tiêu cụ thể. Ví dụ: "Product Launch Campaign" project.

### **Workspace**
Personal hoặc team environment chứa tất cả conversations, projects, files, và settings. Mỗi user có personal workspace và có thể join team workspaces.

### **Dashboard**
Main interface của Twin AI platform nơi bạn access experts, manage conversations, view analytics.

### **Sidebar**
Navigation panel bên trái dashboard hiển thị conversations, projects, experts, và quick actions.

### **Message History**
Archive of all messages trong conversation, được save automatically và có thể search được.

### **Conversation Sharing**
Feature cho phép share conversation với team members hoặc via public link (với permissions control).

## 👥 Team & Collaboration

### **Team Member**
User được invite vào team workspace với specific role và permissions.

### **Team Admin**
Role với highest permissions: manage members, billing, settings, và all team resources.

### **Editor**
Team member role có thể create và edit conversations, projects, files nhưng không manage team settings.

### **Viewer**
Limited role chỉ có thể view shared conversations và projects, không create hoặc edit.

### **Team Workspace**
Shared environment cho team collaboration với centralized billing, member management, và resource sharing.

### **Collaboration**
Real-time working together trên projects với features như shared conversations, comments, và notifications.

### **Project Collaboration**
Specific collaboration within a project context, bao gồm shared resources và coordinated workflows.

### **Permissions**
Access control system định nghĩa ai có thể access, view, edit, hoặc manage specific resources.

## 🔧 Technical Terms

### **API (Application Programming Interface)**
Set of protocols cho phép external applications integrate với Twin AI services programmatically.

### **API Key**
Authentication credential dùng để access Twin AI API. Format: `tk_live_...` for production, `tk_test_...` for testing.

### **API Endpoint**
Specific URL path trong API để access particular functionality (ví dụ: `/v1/chat/completions`).

### **SDK (Software Development Kit)**
Pre-built libraries và tools để easier integrate Twin AI vào applications. Available cho JavaScript, Python, PHP.

### **Webhook**
HTTP callback cho phép Twin AI send real-time notifications đến external systems khi specific events occur.

### **Rate Limiting**
Restriction on number of API requests có thể made trong time period để ensure fair usage và system stability.

### **Authentication**
Process verify identity của user hoặc application trước khi grant access đến resources.

### **Bearer Token**
Type of authentication token được include trong Authorization header của API requests.

### **REST API**
Architectural style cho web services mà Twin AI API follows, sử dụng standard HTTP methods.

### **JSON (JavaScript Object Notation)**
Data format được sử dụng cho API requests và responses. Human-readable và machine-parseable.

## 📊 Analytics & Monitoring

### **Usage Analytics**
Detailed metrics about API usage, conversation patterns, token consumption, và performance.

### **Token Usage**
Tracking của total tokens consumed across all conversations và API calls trong billing period.

### **Request Volume**
Number of API requests hoặc conversation messages được processed trong time period.

### **Response Time**
Time taken để AI generate và return response sau khi receive prompt.

### **Uptime**
Percentage of time mà Twin AI services available và functioning correctly.

### **Performance Metrics**
Various measurements of system performance: latency, throughput, error rates, user satisfaction.

### **Activity Log**
Record of all user actions trong workspace: conversations created, files uploaded, team changes.

### **Audit Trail**
Detailed log of administrative actions cho compliance và security purposes (Enterprise feature).

## 💰 Billing & Plans

### **Subscription Plan**
Recurring billing model với different tiers: Free, Pro, Enterprise, each với different limits và features.

### **Monthly/Annual Billing**
Billing cycle options. Annual plans usually offer discount compared to monthly.

### **Usage-based Billing**
Billing model where cost depends on actual usage (tokens, API calls) rather than fixed subscription.

### **Quota**
Limit on usage within billing period. Ví dụ: 10,000 tokens/month cho Pro plan.

### **Credit**
Pre-paid units có thể used để pay for usage. Especially useful cho Enterprise customers với variable usage.

### **Overage**
Usage beyond included quota trong plan, typically billed at per-unit rate.

### **Billing Cycle**
Time period (usually monthly) cho subscription billing và quota reset.

### **Plan Upgrade/Downgrade**
Changing subscription plan để access different features hoặc limits.

## 🔒 Security & Compliance

### **Data Encryption**
Protection of data bằng cách convert nó into coded format. Twin AI uses end-to-end encryption.

### **Data Residency**
Geographic location where data được stored. Twin AI stores Vietnamese user data trong Singapore region.

### **GDPR Compliance**
Adherence to General Data Protection Regulation, EU privacy law. Includes right to delete và export data.

### **SOC 2 Compliance**
Security standard for organizations handling customer data. Twin AI is SOC 2 Type II certified.

### **Data Retention**
Policy về how long data được kept before automatic deletion. Configurable cho Enterprise customers.

### **Privacy Policy**
Legal document describing how Twin AI collects, uses, và protects user data.

### **Terms of Service**
Legal agreement between Twin AI và users về acceptable use của platform.

### **Single Sign-On (SSO)**
Authentication method cho phép users access Twin AI using existing corporate credentials.

## 🚀 Advanced Features

### **Streaming Response**
Real-time delivery of AI response as it's being generated, rather than waiting for complete response.

### **Batch Processing**
Processing multiple requests simultaneously để improve efficiency, especially useful cho API integrations.

### **Custom Expert**
AI expert được trained specifically cho organization's needs, industry, hoặc use cases (Enterprise feature).

### **Template**
Pre-defined prompt structure có thể reused cho consistent results across similar tasks.

### **Workflow Automation**
Automated sequences of actions triggered by specific events hoặc conditions.

### **Integration**
Connection between Twin AI và external systems/tools như Slack, CRM, hoặc custom applications.

### **White-label**
Customization của Twin AI interface với customer's branding cho seamless user experience.

### **On-premise Deployment**
Installation của Twin AI services on customer's own infrastructure cho maximum security và control.

## 🎯 Use Case Specific Terms

### **Prompt Engineering**
Art và science của crafting effective prompts để get optimal results from AI experts.

### **Content Strategy**
Comprehensive plan cho creating, publishing, và managing content across different channels.

### **Copy Optimization**
Process of improving written content để increase engagement, conversions, hoặc other desired outcomes.

### **Brand Voice**
Consistent personality và tone của brand communication across all channels và touchpoints.

### **Marketing Funnel**
Journey that potential customers take from awareness đến purchase, với different stages requiring different approaches.

### **A/B Testing**
Comparing two versions of content, design, hoặc strategy để determine which performs better.

### **ROI (Return on Investment)**
Measure of efficiency của investment, calculated as (Gain - Cost) / Cost.

### **KPI (Key Performance Indicator)**
Specific, measurable metrics used để evaluate success của strategy hoặc campaign.

## 🔄 Process & Workflow Terms

### **Onboarding**
Process of getting new users familiar với Twin AI platform và best practices.

### **Training**
Educational process để help users maximize value from Twin AI features và capabilities.

### **Implementation**
Process of integrating Twin AI into existing workflows và systems.

### **Adoption**
Rate và extent mà users incorporate Twin AI into their regular work processes.

### **Change Management**
Structured approach để transitioning individuals và organizations to new tools và processes.

### **Best Practices**
Proven methods và approaches cho achieving optimal results với Twin AI.

### **Use Case**
Specific scenario hoặc application where Twin AI provides value, often industry hoặc function-specific.

### **Success Metrics**
Quantifiable measures used để evaluate effectiveness của Twin AI implementation.

## 📝 Content & Communication

### **Content Brief**
Document outlining requirements, goals, audience, và guidelines cho content creation project.

### **Style Guide**
Document defining brand voice, tone, formatting rules, và other communication standards.

### **Content Calendar**
Schedule planning when different pieces of content will be created và published.

### **Editorial Workflow**
Process for creating, reviewing, approving, và publishing content.

### **Content Optimization**
Process of improving content để better achieve intended goals: SEO, engagement, conversions.

### **Multichannel**
Approach của distributing content across multiple platforms hoặc channels simultaneously.

### **Personalization**
Customizing content hoặc experience based on individual user characteristics hoặc behavior.

### **Localization**
Adapting content cho specific geographic hoặc cultural markets beyond simple translation.

---

## 📚 Quick Reference

### Common Abbreviations
- **AI**: Artificial Intelligence
- **API**: Application Programming Interface  
- **CRM**: Customer Relationship Management
- **FAQ**: Frequently Asked Questions
- **KPI**: Key Performance Indicator
- **ROI**: Return on Investment
- **SDK**: Software Development Kit
- **SLA**: Service Level Agreement
- **SSO**: Single Sign-On
- **UI/UX**: User Interface/User Experience

### Units & Measurements
- **Token**: ~4 characters text processing unit
- **Request**: Single API call hoặc conversation message
- **Concurrent**: Simultaneous operations
- **Latency**: Response time in milliseconds
- **Throughput**: Operations per second/minute/hour

### Status & States
- **Active**: Currently functioning hoặc in use
- **Pending**: Awaiting processing hoặc approval
- **Completed**: Successfully finished
- **Failed**: Encountered error hoặc unsuccessful
- **Archived**: Stored but not actively used
- **Deprecated**: Being phased out

---

**💡 Pro tip**: Bookmark this page for quick reference! Thuật ngữ sẽ được update regularly khi Twin AI evolves với new features và capabilities.
