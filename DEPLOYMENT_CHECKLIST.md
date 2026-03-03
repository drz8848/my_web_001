# 部署检查清单

## 部署前检查

### 1. 邮箱配置 ✅
- [ ] 已获取网易163邮箱授权码
- [ ] 已修改 `myforum/settings.py` 中的邮箱配置
- [ ] 已测试邮件发送功能

### 2. 数据库迁移 ✅
- [ ] 已运行 `python manage.py makemigrations accounts`
- [ ] 已运行 `python manage.py migrate`
- [ ] 检查数据库表结构是否正确

### 3. 依赖安装 ✅
- [ ] 已安装所有依赖包 `pip install -r requirements.txt`
- [ ] Django版本正确 (4.2)
- [ ] 所有第三方包正常工作

### 4. 配置文件检查 ✅
- [ ] SECRET_KEY已修改（生产环境）
- [ ] DEBUG=False（生产环境）
- [ ] ALLOWED_HOSTS已配置
- [ ] 数据库配置正确
- [ ] 静态文件配置正确

### 5. 功能测试 ✅
- [ ] 用户注册功能正常
- [ ] 邮箱验证功能正常
- [ ] 密码重置功能正常
- [ ] 个人中心功能正常
- [ ] 帖子发布功能正常
- [ ] 权限管理正常

### 6. 安全检查 ✅
- [ ] 敏感信息不暴露在前端
- [ ] CSRF保护已启用
- [ ] 密码加密存储
- [ ] Token有效期配置合理
- [ ] 邮箱配置信息安全

## 部署步骤

### 开发环境部署

1. **配置邮箱**
   ```bash
   # 编辑 myforum/settings.py
   EMAIL_HOST_USER = 'your_email@163.com'
   EMAIL_HOST_PASSWORD = 'your_auth_code'
   DEFAULT_FROM_EMAIL = 'your_email@163.com'
   ```

2. **数据库迁移**
   ```bash
   python manage.py migrate
   ```

3. **创建超级用户**
   ```bash
   python manage.py createsuperuser
   ```

4. **启动服务器**
   ```bash
   python manage.py runserver
   ```

5. **测试功能**
   - 访问 http://127.0.0.1:8000
   - 注册新用户测试邮箱验证
   - 测试密码重置功能
   - 测试个人中心功能

### 生产环境部署

1. **环境准备**
   ```bash
   # 安装系统依赖
   apt-get install python3 python3-pip nginx postgresql
   
   # 安装Python依赖
   pip3 install -r requirements.txt
   pip3 install gunicorn psycopg2-binary
   ```

2. **配置数据库**
   ```bash
   # 创建PostgreSQL数据库
   createdb myforum
   
   # 修改 settings.py 数据库配置
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'myforum',
           'USER': 'your_db_user',
           'PASSWORD': 'your_db_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

3. **修改生产配置**
   ```python
   # myforum/settings.py
   DEBUG = False
   SECRET_KEY = 'your-secret-key-here'
   ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
   
   # 静态文件配置
   STATIC_ROOT = '/var/www/myforum/static'
   MEDIA_ROOT = '/var/www/myforum/media'
   ```

4. **收集静态文件**
   ```bash
   python manage.py collectstatic --noinput
   ```

5. **数据库迁移**
   ```bash
   python manage.py migrate
   ```

6. **创建超级用户**
   ```bash
   python manage.py createsuperuser
   ```

7. **配置Gunicorn**
   ```bash
   gunicorn --bind 127.0.0.1:8000 myforum.wsgi:application
   ```

8. **配置Nginx**
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;
       
       location /static/ {
           alias /var/www/myforum/static/;
       }
       
       location /media/ {
           alias /var/www/myforum/media/;
       }
       
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

9. **配置SSL证书（推荐）**
   ```bash
   certbot --nginx -d yourdomain.com -d www.yourdomain.com
   ```

10. **启动服务**
    ```bash
    # 启动Gunicorn
    gunicorn --daemon --bind 127.0.0.1:8000 myforum.wsgi:application
    
    # 启动Nginx
    systemctl start nginx
    ```

## 监控和维护

### 日志监控
- [ ] 配置Django日志记录
- [ ] 监控错误日志
- [ ] 监控访问日志
- [ ] 配置日志轮转

### 性能监控
- [ ] 监控服务器资源使用
- [ ] 监控数据库性能
- [ ] 监控邮件发送成功率
- [ ] 配置性能告警

### 数据备份
- [ ] 配置定期数据库备份
- [ ] 备份媒体文件
- [ ] 测试备份恢复
- [ ] 配置异地备份

### 安全维护
- [ ] 定期更新系统补丁
- [ ] 定期更新依赖包
- [ ] 监控安全漏洞
- [ ] 定期更换密钥

## 故障排查

### 常见问题

**1. 邮件发送失败**
```bash
# 检查配置
python manage.py shell
>>> from django.core.mail import send_mail
>>> send_mail('Test', 'Test message', 'from@example.com', ['to@example.com'])
```

**2. 数据库连接失败**
```bash
# 检查数据库连接
python manage.py dbshell
```

**3. 静态文件不加载**
```bash
# 重新收集静态文件
python manage.py collectstatic --noinput --clear
```

**4. 权限问题**
```bash
# 检查文件权限
ls -la /var/www/myforum/
chown -R www-data:www-data /var/www/myforum/
```

## 回滚计划

### 代码回滚
```bash
git checkout <previous-commit>
python manage.py migrate
```

### 数据库回滚
```bash
python manage.py migrate accounts 0002
```

### 配置回滚
- 保留配置文件备份
- 快速恢复脚本

## 联系信息

- 技术支持：[your-email@example.com]
- 文档：查看项目根目录下的文档文件
- 问题反馈：通过GitHub Issues提交

## 版本信息

- Django版本：4.2
- Python版本：3.8+
- 数据库：SQLite (开发) / PostgreSQL (生产)
- 邮件服务：网易163 SMTP
- 部署日期：[填写部署日期]

---

**注意**：请根据实际部署环境调整此检查清单。
