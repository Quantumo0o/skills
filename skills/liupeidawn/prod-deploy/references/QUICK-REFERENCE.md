# 发布流程快速参考

## 🚀 一键发布

```bash
cd /home/administrator/.openclaw/workspace-main
python3 skills/prod-deploy/scripts/deploy.py
```

---

## 📋 快速检查清单

- [ ] 本地 `npm run build` 成功
- [ ] 数据库迁移文件已创建
- [ ] 已备份生产数据库
- [ ] 避开高峰期（20:00-23:00）
- [ ] 准备好回滚方案

---

## 🔧 常用命令速查

```bash
# 连接服务器
ssh root@157.245.56.178

# 数据库备份
ssh root@157.245.56.178 "pg_dump smdating > /tmp/backup_$(date +%Y%m%d_%H%M%S).dump"

# 查看服务状态
ssh root@157.245.56.178 "pm2 status"

# 查看日志
ssh root@157.245.56.178 "pm2 logs --lines 50"

# 重启服务
ssh root@157.245.56.178 "pm2 restart all"

# 执行迁移
ssh root@157.245.56.178 "cd /var/www/sm-dating-website/backend && npm run migrate"

# 检查前端
curl -I https://zmq-club.com

# 检查 API
curl https://zmq-club.com/api/health
```

---

## 🔄 紧急回滚

```bash
# 1. 恢复数据库
ssh root@157.245.56.178 "pg_restore -d smdating /tmp/smdating_backup_YYYYMMDD_HHMMSS.dump"

# 2. 回滚代码
ssh root@157.245.56.178 "cd /var/www/sm-dating-website && git reset --hard HEAD~1"

# 3. 重启服务
ssh root@157.245.56.178 "pm2 restart all"
```

---

## 📊 服务器信息

| 项目 | 值 |
|------|-----|
| 服务器 IP | 157.245.56.178 |
| 用户名 | root |
| 密码 | 7758258Liu |
| 端口 | 22 |
| 前端路径 | /var/www/sm-dating-website/backend/public |
| 后端路径 | /var/www/sm-dating-website/backend |
| 数据库 | smdating (PostgreSQL) |

---

## ⚠️ 注意事项

1. **发布窗口**：避免 20:00-23:00 和周五下午
2. **备份优先**：任何操作前先备份
3. **迁移顺序**：DB 迁移 → 后端代码 → 前端代码 → 重启服务
4. **验证必须**：发布后检查健康状态和核心功能
5. **记录发布**：在 memory/YYYY-MM-DD.md 中记录

---

## 🆘 常见问题

**Q: 发布后页面 404？**
```bash
ssh root@157.245.56.178 "ls -la /var/www/sm-dating-website/backend/public/"
ssh root@157.245.56.178 "systemctl restart nginx"
```

**Q: API 返回 500？**
```bash
ssh root@157.245.56.178 "pm2 logs --lines 100"
```

**Q: 数据库迁移失败？**
```bash
ssh root@157.245.56.178 "cd /var/www/sm-dating-website/backend && npm run migrate:rollback"
```
