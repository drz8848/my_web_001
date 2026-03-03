# 东方幻绮梦 - Django论坛项目

一个基于Django开发的现代化论坛系统，支持用户注册、邮箱验证、帖子发布、权限管理等功能。

## ✨ 主要特性

### 用户管理
- ✅ 用户注册与登录
- ✅ 邮箱验证功能
- ✅ 密码重置（邮箱+密保）
- ✅ 个人资料管理
- ✅ 用户统计信息
- ✅ 角色权限管理

### 帖子功能
- ✅ 帖子发布与编辑
- ✅ 图片上传支持
- ✅ 点赞与收藏
- ✅ 帖子搜索
- ✅ 转发功能

### 权限管理
- ✅ 三个用户角色（普通用户、管理员、拥有者）
- ✅ 禁言功能
- ✅ 统一权限控制
- ✅ 安全的权限检查

### 安全特性
- ✅ 邮箱验证
- ✅ 安全Token机制
- ✅ 密码加密存储
- ✅ CSRF保护
- ✅ 链接过期保护

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/drz8848/my_web_001.git
cd my_web_001
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置邮箱

编辑 `myforum/settings.py`，配置网易163邮箱：

```python
EMAIL_HOST_USER = 'your_email@163.com'
EMAIL_HOST_PASSWORD = 'your_auth_code'
DEFAULT_FROM_EMAIL = 'your_email@163.com'
```

获取授权码步骤：
1. 登录 https://mail.163.com
2. 设置 → POP3/SMTP/IMAP → 开启SMTP服务
3. 授权码管理 → 生成授权码

### 4. 数据库迁移

```bash
python manage.py migrate
```

### 5. 创建超级用户

```bash
python manage.py createsuperuser
```

### 6. 启动服务器

```bash
python manage.py runserver
```

访问 http://127.0.0.1:8000

## 📖 详细文档

- **快速开始指南**: [QUICKSTART.md](QUICKSTART.md)
- **邮箱配置说明**: [EMAIL_SETUP.md](EMAIL_SETUP.md)
- **功能改进总结**: [IMPROVEMENTS.md](IMPROVEMENTS.md)
- **部署检查清单**: [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)

## 🧪 测试

运行功能测试脚本：

```bash
python test_features.py
```

## 📁 项目结构

```
my_web_001/
├── accounts/               # 用户管理应用
│   ├── migrations/        # 数据库迁移
│   ├── admin.py          # 管理后台
│   ├── decorators.py     # 权限装饰器
│   ├── forms.py          # 表单类
│   ├── models.py         # 数据模型
│   ├── urls.py           # URL路由
│   ├── utils.py          # 工具函数
│   └── views.py          # 视图函数
├── posts/                # 帖子管理应用
│   ├── migrations/       # 数据库迁移
│   ├── admin.py         # 管理后台
│   ├── forms.py         # 表单类
│   ├── models.py        # 数据模型
│   ├── urls.py          # URL路由
│   └── views.py         # 视图函数
├── templates/            # 模板文件
│   ├── accounts/        # 用户模板
│   └── posts/           # 帖子模板
├── myforum/             # 项目配置
│   ├── settings.py      # 设置
│   ├── urls.py          # 主URL
│   └── wsgi.py          # WSGI
├── db.sqlite3           # 数据库
├── manage.py            # 管理脚本
├── test_features.py     # 测试脚本
└── requirements.txt     # 依赖包
```

## 🔧 技术栈

- **后端**: Django 4.2
- **前端**: Bootstrap 5, jQuery
- **数据库**: SQLite (开发) / PostgreSQL (生产)
- **邮件**: 网易163 SMTP
- **表单**: Django Crispy Forms

## 👥 用户角色

### 普通用户 (user)
- 浏览帖子
- 发布帖子（未禁言）
- 点赞和收藏
- 编辑个人资料

### 管理员 (mod)
- 所有普通用户权限
- 删除任何帖子
- 禁言用户
- 访问管理后台

### 网站拥有者 (owner)
- 所有管理员权限
- 修改用户角色
- 完全的系统控制

## 🆕 最新更新 (v2.0)

### 新增功能
- ✅ 完整的邮箱验证系统
- ✅ 邮箱密码重置功能
- ✅ 用户统计信息
- ✅ 个人资料编辑
- ✅ 密码修改功能
- ✅ 统一权限管理
- ✅ 禁言用户控制
- ✅ 增强的管理后台

### 安全改进
- ✅ 安全Token机制
- ✅ 链接过期保护
- ✅ 邮箱验证要求
- ✅ 权限检查统一

### 用户体验
- ✅ 美化的个人中心
- ✅ 统计数据展示
- ✅ 友好的错误提示
- ✅ 响应式设计

## 🛠️ 开发指南

### 添加新功能

1. **创建模型**：在相应应用的 `models.py` 中定义
2. **创建迁移**：`python manage.py makemigrations`
3. **应用迁移**：`python manage.py migrate`
4. **创建视图**：在 `views.py` 中实现业务逻辑
5. **配置URL**：在 `urls.py` 中添加路由
6. **创建模板**：在 `templates/` 目录下创建HTML文件

### 权限控制

使用装饰器进行权限控制：

```python
from accounts.decorators import login_required, role_required, not_muted_required

@login_required
def my_view(request):
    # 需要登录
    pass

@role_required('mod', 'owner')
def admin_view(request):
    # 需要管理员或拥有者权限
    pass

@not_muted_required
def post_view(request):
    # 需要未被禁言
    pass
```

### 邮件发送

使用工具函数发送邮件：

```python
from accounts.utils import send_verification_email, send_password_reset_email

# 发送验证邮件
send_verification_email(request, user)

# 发送密码重置邮件
send_password_reset_email(request, user)
```

## 📝 待办事项

- [ ] 添加私信功能
- [ ] 添加评论功能
- [ ] 添加标签系统
- [ ] 添加用户等级系统
- [ ] 添加通知功能
- [ ] 添加搜索优化
- [ ] 添加富文本编辑器
- [ ] 添加文件上传优化

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

## 👤 作者

drz8848

## 🙏 致谢

- Django团队
- Bootstrap团队
- 所有贡献者

---

**注意**: 这是一个学习项目，请根据实际需求进行调整和优化。
