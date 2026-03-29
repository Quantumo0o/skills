# ClawHub Publish Guide | ClawHub 发布指南

## Publish checklist | 发布前检查清单

1. Confirm the user explicitly approved publish or update.  
   确认用户已明确同意发布或更新。
2. Confirm display name uses `English | 中文`.  
   确认显示名采用 `English | 中文`。
3. Confirm description is concise and attractive.  
   确认 description 简洁、具体、抓眼。
4. Confirm changelog is bilingual and formal.  
   确认 changelog 为双语且正式。
5. Confirm version number is correct.  
   确认版本号正确。

## CLI commands worth knowing | 关键 CLI 命令

```bash
clawhub publish <path> --slug <slug> --name "<name>" --version <version> --changelog "<text>"
clawhub delete <slug> --yes
clawhub hide <slug> --yes
clawhub unhide <slug> --yes
clawhub undelete <slug> --yes
clawhub sync
```

## Publish command | 发布命令

```bash
clawhub publish <path-to-skill> \
  --slug <slug> \
  --name "<Display Name>" \
  --version <version> \
  --changelog "<changelog>"
```

## Changelog rules | 发布说明规则

- English first, Chinese after.  
  英文在前，中文在后。
- Use release-note tone, not chat tone.  
  使用发布说明语气，不要写成聊天口吻。
- Emphasize visible improvements.  
  强调用户可感知的改进。
- Avoid exposing small mistakes or awkward implementation history.  
  避免暴露小失误或尴尬实现过程。
- Avoid slang, jokes, and apology-style wording.  
  避免俚语、玩笑和道歉式表述。
- Write something suitable for a public release page, not an internal work log.  
  要写成适合公开发布页的文案，不要像内部工作记录。

## Good changelog examples | 推荐示例

- `Initial release. 首次发布。`
- `Improve cross-platform behavior with automatic Windows/macOS detection. 优化跨平台行为，新增 Windows/macOS 自动识别。`
- `Add complete working examples for both messaging flows. 新增两套可直接使用的完整示例。`

## Avoid these styles | 避免这些写法

- `Fixed a silly bug`
- `Tried a few things and this one finally works`
- `The old method was bad`
- `Sorry about the previous broken version`

## Version conflict | 版本冲突

If publish fails with `Version already exists`, bump the version and republish only after confirming with the user.  
如果发布失败并提示 `Version already exists`，应先与用户确认，再升版本号重新发布。
