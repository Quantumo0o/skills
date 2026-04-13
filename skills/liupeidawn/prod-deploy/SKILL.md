---
name: prod-deploy
description: 生产环境发布部署自动化技能。用于 SM 交友网站 (zmq-club.com) 的一键发布流程，包括：数据库备份、结构对比、前端构建、代码部署、迁移执行、服务重启、生产验证。Use when 沛哥要求发布生产、部署代码、上线新功能、或执行发布 SOP。
---

# 生产环境发布部署技能

## 快速开始

**触发场景：**
- "发布到生产"
- "部署代码"
- "上线新功能"
- "执行发布流程"

**核心流程（10 步）：**
1. 本地测试 → 2. DB 结构对比 → 3. 前端构建 → 4. 回归测试 → 5. 备份生产 → 6. 部署代码 → 7. 执行迁移 → 8. 重启服务 → 9. 生产验证 → 10. 记录发布

## 服务器配置

```
生产服务器：157.245.56.178
用户名：root
密码：7758258Liu
端口：22
部署路径：/var/www/sm-dating-website/
前端构建：/home/administrator/.openclaw/workspace-main/projects/sm-dating-website/frontend/dist
后端路径：/home/administrator/.openclaw/workspace-main/projects/sm-dating-website/backend
```

## 发布前检查清单

执行发布前必须确认：

- [ ] 本地测试通过（npm test / pytest）
- [ ] 数据库结构对比无冲突（scripts/db_diff_check.py）
- [ ] 前端构建成功（npm run build）
- [ ] 回归测试通过率 >90%
- [ ] 已通知相关人员（如需要）

## 一键发布

使用自动化脚本执行完整发布流程：

```bash
cd /home/administrator/.openclaw/workspace-main
python3 skills/prod-deploy/scripts/deploy.py
```

**脚本自动执行：**
1. 连接生产服务器
2. 备份当前代码和数据库
3. 上传前端构建文件
4. 上传后端代码
5. 执行数据库迁移（knex migrate:latest）
6. 重启 PM2 服务
7. 验证服务健康状态
8. 输出发布报告

## 分步执行

### 1. 数据库备份

```bash
ssh root@157.245.56.178 "pg_dump smdating > /tmp/smdating_backup_$(date +%Y%m%d_%H%M%S).dump"
```

### 2. 数据库结构对比

```bash
python3 scripts/db_diff_check.py
```

### 3. 前端构建

```bash
cd projects/sm-dating-website/frontend
npm run build
```

### 4. 部署前端

```bash
python3 scripts/deploy_frontend.py
```

### 5. 部署后端

```bash
# 使用 SCP 上传后端代码
scp -r projects/sm-dating-website/backend/* root@157.245.56.178:/var/www/sm-dating-website/backend/
```

### 6. 执行数据库迁移

```bash
ssh root@157.245.56.178 "cd /var/www/sm-dating-website/backend && npm run migrate"
```

### 7. 重启服务

```bash
ssh root@157.245.56.178 "pm2 restart all"
```

### 8. 生产验证

```bash
python3 scripts/check_prod_frontend.py
curl -I https://zmq-club.com
curl https://zmq-club.com/api/health
```

## 回滚流程

如果发布失败，立即执行回滚：

```bash
# 1. 恢复数据库
ssh root@157.245.56.178 "pg_restore -d smdating /tmp/smdating_backup_YYYYMMDD_HHMMSS.dump"

# 2. 恢复代码（从 Git）
ssh root@157.245.56.178 "cd /var/www/sm-dating-website && git reset --hard HEAD~1"

# 3. 重启服务
ssh root@157.245.56.178 "pm2 restart all"
```

## 相关脚本

- `scripts/deploy.py` - 一键发布主脚本（本技能）
- `scripts/deploy_frontend.py` - 前端部署（项目脚本）
- `scripts/db_diff_check.py` - 数据库结构对比
- `scripts/check_prod_frontend.py` - 生产环境检查
- `backend/knexfile.js` - Knex 迁移配置

## 参考文档

- `references/RELEASE-SOP.md` - 完整发布 SOP
- `references/QUICK-REFERENCE.md` - 快速参考

## 注意事项

⚠️ **发布窗口：** 避免在高峰期（20:00-23:00）发布
⚠️ **备份优先：** 任何操作前先备份
⚠️ **迁移顺序：** 先执行 DB 迁移，再重启服务
⚠️ **验证必须：** 发布后必须执行健康检查
⚠️ **记录发布：** 在 memory/YYYY-MM-DD.md 中记录发布内容和时间

## 常见问题

**Q: 数据库迁移失败？**
A: 检查 knexfile.js 配置，确认生产数据库连接正常，查看 migrations 文件是否有语法错误。

**Q: 前端构建失败？**
A: 检查 node_modules 是否完整，尝试 `npm ci` 重新安装依赖。

**Q: PM2 服务启动失败？**
A: 查看 `pm2 logs` 输出，检查 .env 配置文件是否正确，确认端口未被占用。

**Q: 回滚后数据丢失？**
A: 确认备份文件完整，使用 `pg_restore --list` 查看备份内容再恢复。
