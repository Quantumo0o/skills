---
name: meetingos
display_name: "MeetingOS"
version: 1.0.0
description: "Auto meeting notes and action item execution loop. Trigger this skill whenever the user mentions: meeting notes, meeting summary, action items, follow-up, transcript, recording, Zoom summary, Teams meeting, Tencent Meeting, Feishu meeting, WeCom meeting, upload audio, upload video, meeting template, task creation, hui yi ji yao, xing dong xiang, hui hou gen jin, zheng li hui yi."
homepage: "https://clawhub.ai/DTTNpole-commits/meetingos"

metadata:
  clawdbot:
    emoji: "🧠"

  openclaw:
    user_invocable: true
    requires:
      env:
        - name: "OPENAI_API_KEY"
          description: "OpenAI API Key for cloud transcription"
          required: false
        - name: "WECOM_CORP_ID"
          description: "WeCom Enterprise CorpID"
          required: false
        - name: "WECOM_AGENT_ID"
          description: "WeCom Application AgentID"
          required: false
        - name: "WECOM_AGENT_SECRET"
          description: "WeCom Application Secret"
          required: false
        - name: "WECOM_WEBHOOK_URL"
          description: "WeCom Group Robot Webhook URL"
          required: false
        - name: "FEISHU_APP_ID"
          description: "Feishu App ID starting with cli_"
          required: false
        - name: "FEISHU_APP_SECRET"
          description: "Feishu App Secret"
          required: false
        - name: "FEISHU_CHAT_ID"
          description: "Feishu default group chat ID starting with oc_"
          required: false
        - name: "FEISHU_BITABLE_TOKEN"
          description: "Feishu Bitable App Token"
          required: false
        - name: "FEISHU_BITABLE_TABLE"
          description: "Feishu Bitable Table ID"
          required: false
        - name: "NOTION_API_KEY"
          description: "Notion Integration Token"
          required: false
        - name: "NOTION_DATABASE_ID"
          description: "Notion Database ID"
          required: false
        - name: "MEETINGOS_PRIVACY_MODE"
          description: "Processing mode: local or cloud"
          required: false
        - name: "MEETINGOS_DOWNLOAD_DIR"
          description: "Temporary directory for downloaded recordings"
          required: false
        - name: "MEETINGOS_MAX_FILE_MB"
          description: "Max file size in MB"
          required: false
      bins:
        - ffmpeg
        - python3
---

# MeetingOS - Auto Meeting Notes and Action Items

Full automation for meeting transcription, structured notes, action item extraction, and task execution loop.

## When to Use

Use this skill whenever the user says any of the following:

- "Help me organize this meeting"
- "Extract action items"
- "Push to Notion / Feishu / WeCom"
- "Generate meeting notes from this transcript"
- "Upload recording for summary"
- "What happened in the follow-up from last meeting"
- "Use sales template to summarize this meeting"
- "Send meeting summary to Feishu group"
- "Create Linear issues from our standup"
- "Batch process this week's recordings"

## Core Commands
```
/meeting new       Start new meeting processing flow
/meeting upload    Upload audio / video / transcript file
/meeting paste     Paste text transcript directly
/meeting template  Choose a notes template
/meeting push      Push action items to task management tool
/meeting notify    Send notes to notification channel
/meeting followup  Pull last meeting action item completion status
/meeting batch     Batch process multiple meetings
/meeting settings  Configure integrations and preferences
/meeting help      Show help
```

## Configuration

### Required Environment Variables

Set these in your .env file or in the OpenClaw settings panel.

**Minimum setup (only needs one key):**
```
OPENAI_API_KEY=sk-...
MEETINGOS_PRIVACY_MODE=cloud
```

**For local privacy mode (no data leaves your machine):**
```
MEETINGOS_PRIVACY_MODE=local
```

Install local Whisper:
```
pip install openai-whisper
```

**Feishu integration:**
```
FEISHU_APP_ID=cli_...
FEISHU_APP_SECRET=...
FEISHU_CHAT_ID=oc_...
FEISHU_BITABLE_TOKEN=bascn...
FEISHU_BITABLE_TABLE=tbl...
```

**WeCom integration:**
```
WECOM_CORP_ID=wx...
WECOM_AGENT_ID=1000002
WECOM_AGENT_SECRET=...
WECOM_WEBHOOK_URL=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=...
```

**Notion integration:**
```
NOTION_API_KEY=secret_...
NOTION_DATABASE_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

## Usage Examples

### Example 1: Upload recording and get full notes

User says:
```
Help me organize the notes from this product review meeting.
Push action items to Notion and notify the responsible people.
```

MeetingOS will:
1. Extract audio from the uploaded file using ffmpeg
2. Transcribe using Whisper
3. Generate structured notes with action items
4. Push to Notion database
5. Send summary card to Feishu or WeCom group

### Example 2: Paste transcript and create Linear issues

User says:
```
Here is our engineering standup transcript.
Create Linear issues for all action items.
```

MeetingOS will:
1. Parse the pasted transcript
2. Extract action items with owner, deadline, and priority
3. Create Linear issues via API
4. Return issue URLs

### Example 3: Follow-up digest before next meeting

User says:
```
Pull the action item completion status from last week before Monday's meeting.
```

MeetingOS will:
1. Query Notion or Feishu Bitable for last meeting action items
2. Check completion status
3. Generate follow-up report showing done, overdue, and pending items

### Example 4: Use sales template

User says:
```
Use the sales template to summarize this client call.
Focus on pain points and next steps.
```

MeetingOS will:
1. Load the sales debrief template
2. Transcribe and structure the content
3. Extract BANT analysis and next actions
4. Generate sales-specific notes

### Example 5: Batch process a week of meetings

User says:
```
Batch process all five meetings from this week and generate a weekly summary.
```

MeetingOS will:
1. Queue all uploaded files
2. Process each in parallel
3. Generate individual notes for each meeting
4. Produce a weekly rollup report

## Security and Privacy

- Default mode is local processing using on-device Whisper
- Zero data retention after session ends
- All API keys stored only in environment variables
- Temporary files use randomized names and are deleted after processing
- No meeting content is written to any persistent log
- GDPR friendly design

## Templates Available
```
templates/default.md          General purpose
templates/weekly_standup.md   Weekly standup
templates/one_on_one.md       One on one meeting
templates/sales_debrief.md    Sales debrief with BANT
templates/project_sync.md     Project sync
templates/product_review.md   Product review
templates/board_meeting.md    Board meeting
templates/retrospective.md    Agile retrospective
```

## File Structure
```
meetingos/
├── SKILL.md
├── scripts/
│   ├── transcribe.py
│   ├── push_notion.py
│   ├── feishu_helper.py
│   ├── wecom_helper.py
│   ├── meeting_fetcher.py
│   └── main_processor.py
└── templates/
    ├── default.md
    └── sales_debrief.md
```

## Version History

### 1.0.0

- Multi-platform meeting ingestion (Zoom, Teams, Feishu, WeCom, Tencent Meeting)
- Local Whisper transcription with Chinese and mixed language support
- Structured notes with WHO / WHAT / WHEN / PRIORITY / WHY extraction
- Task push to Notion, Linear, Jira, Feishu Bitable, WeCom Tasks, Todoist
- Notifications via Slack, email, Feishu group card, WeCom Webhook
- Follow-up digest generation before next meeting
- Batch processing mode
- Nine built-in note templates
- Privacy-first local processing with zero data retention
```

---

## 保存后还要做一件事

保存 SKILL.md 之后，在 VS Code 右下角检查编码格式：

底部状态栏会显示 `UTF-8` 和 `LF`，如果显示的是 `CRLF` 就点一下改成 `LF`，如果编码不是 `UTF-8` 就点一下改成 `UTF-8`。

然后按 `Ctrl + S` 再保存一次，这样可以避免非标准字符的警告。

---

## 重新打包上传
```
1. 在文件夹里选中 meeting-os 整个文件夹
2. 右键 → 压缩为 ZIP 文件
3. 回到 ClawHub 你的 meetingos 页面
4. 点击右上角「更新版本」
5. 上传 ZIP 文件
6. 等待重新扫描（约 2-5 分钟）