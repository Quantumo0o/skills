# 生产环境发布标准操作流程 (SOP)

**适用项目：** SM 交友网站 (zmq-club.com)  
**服务器：** 157.245.56.178  
**最后更新：** 2026-04-09

---

## 📋 发布流程总览

```
本地开发 → 本地测试 → DB 对比 → 前端构建 → 回归测试 → 
备份生产 → 部署代码 → 执行迁移 → 重启服务 → 生产验证
```

---

## ✅ 发布前检查清单

### 代码层面
- [ ] 所有功能在本地测试通过
- [ ] 前端 `npm run build` 无错误
- [ ] 后端 `npm test` 通过率 >90%
- [ ] TypeScript 编译无错误
- [ ] Git 代码已提交并推送

### 数据库层面
- [ ] 运行 `python3 scripts/db_diff_check.py` 检查结构差异
- [ ] 新增的迁移文件已创建并测试
- [ ] 确认迁移不会破坏现有数据

### 沟通层面
- [ ] 如影响用户，提前在群里通知
- [ ] 避开高峰期（20:00-23:00）
- [ ] 准备好回滚方案

---

## 🚀 一键发布（推荐）

```bash
cd /home/administrator/.openclaw/workspace-main
python3 skills/prod-deploy/scripts/deploy.py
```

---

## 🔧 分步执行

### Step 1: 本地测试
```bash
cd projects/sm-dating-website/frontend && npm test
cd projects/sm-dating-website/backend && npm test
cd projects/sm-dating-website/frontend && npm run build
```

### Step 2: 数据库结构对比
```bash
python3 scripts/db_diff_check.py
```

### Step 3: 备份生产环境
```bash
ssh root@157.245.56.178 "pg_dump smdating > /tmp/smdating_backup_$(date +%Y%m%d_%H%M%S).dump"
```

### Step 4: 部署前端
```bash
python3 scripts/deploy_frontend.py
```

### Step 5: 部署后端
```bash
scp -r projects/sm-dating-website/backend/src/* root@157.245.56.178:/var/www/sm-dating-website/backend/src/
```

### Step 6: 执行数据库迁移
```bash
ssh root@157.245.56.178 "cd /var/www/sm-dating-website/backend && npm run migrate"
```

### Step 7: 重启服务
```bash
ssh root@157.245.56.178 "pm2 restart all"
```

### Step 8: 生产验证
```bash
curl -I https://zmq-club.com
curl https://zmq-club.com/api/health
```

---

## 🔄 回滚流程

```bash
# 1. 恢复数据库
ssh root@157.245.56.178 "pg_restore -d smdating /tmp/smdating_backup_YYYYMMDD_HHMMSS.dump"

# 2. 回滚代码
ssh root@157.245.56.178 "cd /var/www/sm-dating-website && git reset --hard HEAD~1"

# 3. 重启服务
ssh root@157.245.56.178 "pm2 restart all"
```

---

## ⚠️ 注意事项

1. **发布窗口**：避免 20:00-23:00 和周五下午
2. **备份优先**：任何操作前先备份
3. **迁移顺序**：DB 迁移 → 后端代码 → 前端代码 → 重启服务
4. **验证必须**：发布后检查健康状态和核心功能
5. **记录发布**：在 memory/YYYY-MM-DD.md 中记录

---

## 📚 相关文档

- [快速参考](QUICK-REFERENCE.md)
- [Knex 迁移指南](../../backend/MIGRATION_README.md)
