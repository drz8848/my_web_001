# 快速开始指南

## 1. 环境准备

### 安装依赖

```bash
pip install -r requirements.txt
```

### 安装Django（如果requirements.txt中没有）

```bash
pip install Django==4.2
```

## 2. 配置邮箱

### 获取网易163邮箱授权码

1. 登录 https://mail.163.com
2. 设置 → POP3/SMTP/IMAP → 开启SMTP服务
3. 授权码管理 → 生成授权码

### 修改配置文件

编辑 `myforum/settings.py`，找到邮件配置部分：

```python
EMAIL_HOST_USER = 'thhqm_web@163.com'      # 替换为你的邮箱
EMAIL_HOST_PASSWORD = 'PDceLVmm5AYsJuWm'      # 替换为你的授权码
DEFAULT_FROM_EMAIL = 'thhqm_web@163.com'   # 替换为你的邮箱
```

## 3. 数据库迁移

```bash
python manage.py migrate
```

## 4. 创建超级用户

```bash
python manage.py createsuperuser
```

按照提示输入用户名、邮箱和密码。

## 5. 启动开发服务器

```bash
python manage.py runserver
```

访问 http://127.0.0.1:8000

## 6. 测试新功能

### 测试邮箱验证

1. 访问注册页面：http://127.0.0.1:8000/accounts/register/
2. 填写注册信息并提交
3. 检查邮箱是否收到验证邮件
4. 点击邮件中的验证链接
5. 登录查看个人中心的验证状态

### 测试密码重置

1. 在登录页面点击"忘记密码"
2. 输入注册邮箱
3. 检查邮箱是否收到重置邮件
4. 点击邮件中的重置链接
5. 设置新密码

### 测试个人中心

1. 登录后访问个人中心
2. 查看统计信息
3. 点击"编辑资料"修改个人信息
4. 点击"修改密码"更改密码

## 7. 管理后台

访问管理后台：http://127.0.0.1:8000/admin/

使用超级用户登录，可以：
- 查看用户列表和验证状态
- 修改用户角色和禁言状态
- 查看用户统计数据
- 管理帖子内容

## 常见问题

### Q: 邮件发送失败怎么办？

A: 检查以下几点：
1. 邮箱配置是否正确
2. 授权码是否正确（不是邮箱密码）
3. 网络连接是否正常
4. 网易邮箱是否开启了SMTP服务

### Q: 数据库迁移失败怎么办？

A: 尝试以下命令：
```bash
python manage.py makemigrations accounts
python manage.py migrate accounts --fake
```

### Q: 如何修改邮箱验证要求？

A: 在 `myforum/settings.py` 中修改：
```python
EMAIL_VERIFICATION_REQUIRED = True  # 强制要求邮箱验证
```

### Q: 如何调整链接有效期？

A: 在 `myforum/settings.py` 中修改：
```python
EMAIL_VERIFICATION_EXPIRE_HOURS = 48  # 验证链接48小时有效
PASSWORD_RESET_EXPIRE_HOURS = 2        # 重置链接2小时有效
```

## 项目结构

```
my_web_001/
├── accounts/               # 用户管理应用
│   ├── migrations/        # 数据库迁移文件
│   ├── admin.py          # 管理后台配置
│   ├── decorators.py     # 权限装饰器
│   ├── forms.py          # 表单类
│   ├── models.py         # 数据模型
│   ├── urls.py           # URL路由
│   ├── utils.py          # 工具函数
│   └── views.py          # 视图函数
├── posts/                # 帖子管理应用
│   ├── migrations/       # 数据库迁移文件
│   ├── admin.py         # 管理后台配置
│   ├── forms.py         # 表单类
│   ├── models.py        # 数据模型
│   ├── urls.py          # URL路由
│   └── views.py         # 视图函数
├── templates/            # 模板文件
│   ├── accounts/        # 用户相关模板
│   └── posts/           # 帖子相关模板
├── myforum/             # 项目配置
│   ├── settings.py      # 设置文件
│   ├── urls.py          # 主URL配置
│   └── wsgi.py          # WSGI配置
├── db.sqlite3           # 数据库文件
├── manage.py            # Django管理脚本
├── EMAIL_SETUP.md       # 邮箱配置详细说明
├── IMPROVEMENTS.md      # 改进功能总结
├── QUICKSTART.md        # 快速开始指南（本文件）
└── requirements.txt     # 依赖包列表
```

## 开发建议

1. **使用虚拟环境**：建议使用虚拟环境隔离项目依赖
2. **版本控制**：使用Git进行版本控制
3. **环境变量**：使用环境变量存储敏感信息
4. **代码规范**：遵循PEP 8代码规范
5. **测试**：编写单元测试和功能测试

## 生产部署注意事项

1. **修改SECRET_KEY**：生成新的SECRET_KEY
2. **DEBUG=False**：关闭调试模式
3. **ALLOWED_HOSTS**：配置正确的域名
4. **静态文件**：收集静态文件 `python manage.py collectstatic`
5. **数据库**：使用PostgreSQL或MySQL替代SQLite
6. **HTTPS**：配置SSL证书
7. **日志**：配置日志记录
8. **备份**：定期备份数据库

## 技术支持

如有问题，请查看：
- 邮箱配置说明：`EMAIL_SETUP.md`
- 改进功能总结：`IMPROVEMENTS.md`
- Django官方文档：https://docs.djangoproject.com/

## 更新日志

### v2.0 (2026-03-03)
- ✅ 添加邮箱验证功能
- ✅ 添加密码重置功能
- ✅ 完善个人中心功能
- ✅ 统一权限管理
- ✅ 添加用户统计功能
- ✅ 增强管理后台
- ✅ 改进安全性
- ✅ 优化用户体验

### v1.0
- 基础论坛功能
- 用户注册登录
- 帖子发布和管理
- 点赞收藏功能
