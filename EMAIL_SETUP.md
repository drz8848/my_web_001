# 邮箱配置说明

## 1. 配置网易163邮箱

### 步骤1：获取网易163邮箱授权码

1. 登录网易163邮箱 (https://mail.163.com)
2. 点击"设置" -> "POP3/SMTP/IMAP"
3. 开启"SMTP服务"
4. 点击"授权码管理"，获取授权码

### 步骤2：修改settings.py配置

编辑 `myforum/settings.py` 文件，找到邮件配置部分：

```python
# 邮件配置 - 使用网易163邮箱
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 465
EMAIL_USE_TLS = True
EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'your_email@163.com'  # 替换为你的163邮箱
EMAIL_HOST_PASSWORD = 'your_auth_code'   # 替换为你的163邮箱授权码
DEFAULT_FROM_EMAIL = 'your_email@163.com'
EMAIL_SUBJECT_PREFIX = '[东方幻绮梦] '
```

将 `your_email@163.com` 替换为你的163邮箱地址，将 `your_auth_code` 替换为你获取的授权码。

### 步骤3：应用数据库迁移

运行以下命令应用数据库迁移：

```bash
python manage.py migrate
```

## 2. 功能说明

### 2.1 邮箱验证功能

- 用户注册时会自动发送验证邮件
- 用户可以在个人中心查看邮箱验证状态
- 未验证邮箱的用户可以点击"发送验证邮件"重新发送
- 验证链接24小时内有效

### 2.2 密码重置功能

- 用户可以通过邮箱重置密码
- 密码重置链接1小时内有效
- 保留了原有的密保问题重置功能

### 2.3 个人中心增强

- 显示用户统计信息（发帖数、获赞数）
- 支持编辑个人资料
- 支持修改密码
- 显示邮箱验证状态
- 显示用户角色和禁言状态

### 2.4 权限管理

- 统一了权限判断逻辑
- 添加了权限管理装饰器
- 禁言用户无法发布新帖
- 管理员和拥有者可以删除任何帖子

## 3. 配置选项

在 `myforum/settings.py` 中可以配置以下选项：

```python
# 邮箱验证配置
EMAIL_VERIFICATION_REQUIRED = False  # 是否强制要求邮箱验证
EMAIL_VERIFICATION_EXPIRE_HOURS = 24  # 邮箱验证链接有效期（小时）
PASSWORD_RESET_EXPIRE_HOURS = 1       # 密码重置链接有效期（小时）
```

- `EMAIL_VERIFICATION_REQUIRED`: 设为True时，未验证邮箱的用户无法进行某些操作
- `EMAIL_VERIFICATION_EXPIRE_HOURS`: 邮箱验证链接的有效期
- `PASSWORD_RESET_EXPIRE_HOURS`: 密码重置链接的有效期

## 4. 测试

### 测试邮箱发送

1. 注册一个新用户
2. 检查邮箱是否收到验证邮件
3. 点击验证链接进行验证
4. 登录查看个人中心的验证状态

### 测试密码重置

1. 在登录页面点击"忘记密码"
2. 输入注册邮箱
3. 检查邮箱是否收到重置邮件
4. 点击重置链接设置新密码

## 5. 故障排除

### 邮件发送失败

1. 检查邮箱配置是否正确
2. 确认授权码是否正确（不是邮箱密码）
3. 检查网络连接
4. 查看Django日志错误信息

### 验证链接无效

1. 检查链接是否已过期
2. 确认用户 token 是否正确
3. 检查数据库中的 token 字段

### 数据库迁移问题

如果迁移失败，可以尝试：

```bash
python manage.py makemigrations accounts
python manage.py migrate accounts --fake
```

## 6. 安全建议

1. 不要将邮箱配置信息提交到版本控制系统
2. 使用环境变量存储敏感信息
3. 定期更换邮箱授权码
4. 在生产环境中使用HTTPS
5. 设置合理的链接有效期

## 7. 环境变量配置（推荐）

为了安全起见，建议使用环境变量：

```python
import os

EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'your_email@163.com')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'your_auth_code')
```

然后在启动应用前设置环境变量：

```bash
export EMAIL_HOST_USER='your_email@163.com'
export EMAIL_HOST_PASSWORD='your_auth_code'
python manage.py runserver
```
