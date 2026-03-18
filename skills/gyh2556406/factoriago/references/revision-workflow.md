# FactoriaGo Revise & Resubmit Workflow

## Overview

FactoriaGo is built around the academic paper revision cycle:
**Submit → Get Reviews → Revise → Resubmit**

## Standard Workflow

### 1. Create a Project
- Upload existing `.tex` / `.zip` file OR start blank with `POST /paper/new-submission`
- Project = one submission attempt (paper + reviewer round)

### 2. Import Reviewer Comments
- Paste raw reviewer text into `POST /paper/:id/analyze`
- System extracts individual concerns, categorizes by severity
- Returns structured revision tasks

### 3. Revision Tasks
- Each reviewer concern becomes a task (`/tasks`)
- Tasks have: title, description, priority (high/medium/low), status
- Agent can create/update tasks via API

### 4. AI-Assisted Revision
- Use chat (`POST /chat`) to discuss specific concerns with AI
- Specify model based on task type:
  - **Claude** → nuanced argumentation, writing quality
  - **GPT-4o** → general revision, broad suggestions
  - **Gemini** → fast iteration, structural suggestions
  - **Kimi / GLM** → Chinese-language papers

### 5. LaTeX Editing
- Read file: `GET /paper/:paperId/files/:fileId/content`
- Edit file: `PUT /paper/:paperId/files/:fileId`
- Compile: `POST /paper/:paperId/files/compile`

### 6. Response Letter
- After revision, generate a point-by-point response letter
- See `reviewer-response.md` for templates

## Common Agent Tasks

| User Says | Agent Action |
|-----------|-------------|
| "帮我分析审稿意见" | POST /paper/:id/analyze with pasted review text |
| "列出我的修改任务" | GET /tasks/by-paper/:paperId |
| "帮我回复这条审稿意见" | Use reviewer-response.md template + AI |
| "打开我的项目" | GET /paper/list → let user pick |
| "编译论文" | POST /paper/:paperId/files/compile |
| "帮我修改第3节" | GET file content → edit → PUT back |

## Key Constraints
- All API calls require authentication (session cookie)
- LaTeX compilation runs server-side (no local install needed)
- File size limit: 20MB per file, 100MB per project
- AI chat quota varies by plan
