# Finder Skill 配置说明

这个 skill 不依赖自定义 CLI，直接通过 Finder 开放接口工作。

## 默认地址

- 站点首页：`https://finder.optell.com`
- 访问密钥页面：`https://finder.optell.com/api-key`
- 接口基础地址：`https://finder.optell.com/api`

## 第一次使用

1. 打开 `https://finder.optell.com` 注册或登录。
2. 打开 `https://finder.optell.com/api-key`。
3. 生成并复制访问密钥。
4. 把访问密钥保存到环境变量。

如果用户已经把 key 直接贴给 Codex，优先让 Codex 直接帮用户保存，不要再要求手工重复输入。

更友好的引导话术可以是：

```text
我先帮你把 Finder 配置接起来。
你先去 https://finder.optell.com/api-key 生成一份访问秘钥，拿到后直接发给我，我可以继续帮你保存到环境变量里。
```

## 持久化保存访问密钥

macOS / Linux:

```bash
KEY="<你的访问密钥>"
if [ -f "$HOME/.zshrc" ]; then
  grep -q 'FINDER_API_KEY=' "$HOME/.zshrc" && \
    sed -i '' '/FINDER_API_KEY=/d' "$HOME/.zshrc" || true
  printf '\nexport FINDER_API_KEY="%s"\n' "$KEY" >> "$HOME/.zshrc"
else
  grep -q 'FINDER_API_KEY=' "$HOME/.bashrc" 2>/dev/null && \
    sed -i '/FINDER_API_KEY=/d' "$HOME/.bashrc" || true
  printf '\nexport FINDER_API_KEY="%s"\n' "$KEY" >> "$HOME/.bashrc"
fi
export FINDER_API_KEY="$KEY"
```

Windows PowerShell:

```powershell
$key = "<你的访问密钥>"
[Environment]::SetEnvironmentVariable("FINDER_API_KEY", $key, "User")
$env:FINDER_API_KEY = $key
```

macOS / Linux:

```bash
export FINDER_API_KEY="<你的访问密钥>"
```

Windows PowerShell:

```powershell
$env:FINDER_API_KEY="<你的访问密钥>"
```

## 校验访问密钥

macOS / Linux:

```bash
curl -X GET 'https://finder.optell.com/api/user/me' \
  -H "Authorization: Bearer $FINDER_API_KEY"
```

Windows PowerShell:

```powershell
$headers = @{
  Authorization = "Bearer $env:FINDER_API_KEY"
}

Invoke-RestMethod -Method Get `
  -Uri "https://finder.optell.com/api/user/me" `
  -Headers $headers
```

## 项目相关命令

列出项目：

```bash
curl -X POST 'https://finder.optell.com/api/project/list' \
  -H "Authorization: Bearer $FINDER_API_KEY"
```

```powershell
$headers = @{
  Authorization = "Bearer $env:FINDER_API_KEY"
}

Invoke-RestMethod -Method Post `
  -Uri "https://finder.optell.com/api/project/list" `
  -Headers $headers
```

创建默认项目：

```bash
curl -X POST 'https://finder.optell.com/api/project/create' \
  -H "Authorization: Bearer $FINDER_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Finder Skill 默认项目",
    "description": "由 Finder skill 自动创建"
  }'
```

```powershell
$headers = @{
  Authorization = "Bearer $env:FINDER_API_KEY"
  "Content-Type" = "application/json"
}

$body = @{
  name = "Finder Skill 默认项目"
  description = "由 Finder skill 自动创建"
} | ConvertTo-Json

Invoke-RestMethod -Method Post `
  -Uri "https://finder.optell.com/api/project/create" `
  -Headers $headers `
  -Body $body
```

## 搜索命令模板

macOS / Linux:

```bash
curl -X POST 'https://finder.optell.com/api/creator/search' \
  -H "Authorization: Bearer $FINDER_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "projectId": 123,
    "platform": "TikTok",
    "keyword": "beauty",
    "minFollowerCount": 100000,
    "maxFollowerCount": 500000
  }'
```

Windows PowerShell:

```powershell
$headers = @{
  Authorization = "Bearer $env:FINDER_API_KEY"
  "Content-Type" = "application/json"
}

$body = @{
  projectId = 123
  platform = "TikTok"
  keyword = "beauty"
  minFollowerCount = 100000
  maxFollowerCount = 500000
} | ConvertTo-Json

Invoke-RestMethod -Method Post `
  -Uri "https://finder.optell.com/api/creator/search" `
  -Headers $headers `
  -Body $body
```

## 常见错误

- `未设置访问密钥`
  - 先去 `https://finder.optell.com/api-key` 生成密钥，再设置环境变量。
- `API Key 无权访问该接口`
  - 说明调用了普通达人搜索白名单之外的接口。
- `没有可用项目`
  - 先调用项目列表接口；如果为空，先创建项目再搜索。
- `已经设置过但新开会话后又失效`
  - 说明只设置了当前会话变量，没有持久化；请改用上面的持久化命令。

## 推荐反馈语句

- 保存成功后：

```text
我已经帮你保存好了，后面就不用再重复输入这串 key 了。
```

- 继续下一步前：

```text
配置已经就绪，我继续帮你检查项目并开始搜索。
```

- 没有项目时：

```text
Finder 会把这次搜索挂在一个项目下面，方便你后面继续查看。你现在还没有项目，要我顺手帮你建一个默认项目吗？
```
