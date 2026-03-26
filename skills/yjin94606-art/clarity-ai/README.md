# Clarity AI

<h1 align="center">智能意图解析器</h1>

<p align="center">
  <em>Transform messy input into crystal-clear instructions</em>
</p>

---

<p align="center">
  <img src="https://img.shields.io/badge/version-2.0.1-blue?style=flat-square" alt="Version">
  <img src="https://img.shields.io/badge/platform-OpenClaw-green?style=flat-square" alt="Platform">
  <img src="https://img.shields.io/badge/privacy-100%25-red?style=flat-square" alt="Privacy">
  <img src="https://img.shields.io/badge/speed-millisecond-yellow?style=flat-square" alt="Speed">
  <img src="https://img.shields.io/badge/intents-7-orange?style=flat-square" alt="Intents">
</p>

---

## What is Clarity AI?

**Clarity AI** is an intelligent intent parser that transforms your verbose, conversational input into structured, precise instructions that AI assistants understand perfectly.

No more vague questions. No more back-and-forth clarification. Just clear, actionable instructions.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🎯 **Smart Recognition** | Accurately identifies 7 intent types |
| ⚡ **Millisecond Response** | Local rule engine, no waiting |
| 🔒 **Privacy First** | 100% local processing |
| 🌏 **Bilingual** | Chinese & English support |
| 🔧 **Extensible** | Optional Ollama AI enhancement |

---

## 📊 Before vs After

| Messy Input | Clean Output |
|-------------|--------------|
| "Hi, I was wondering, about Python for loops, why is it running so slow?" | **Intent:** Performance Optimization<br>**Language:** Python<br>**Goal:** Analyze why for loop is slow |
| "Can you help me check this code, what might be the problem?" | **Intent:** Code Debug<br>**Goal:** Find and fix code issues |

---

## 🎯 Supported Intents

| Intent | Keywords | Example |
|--------|----------|---------|
| Code Debug | debug, error, bug, issue | "Help me debug this code" |
| Performance | slow, performance, optimize | "Why is it running so slow?" |
| Code Creation | write, create, generate | "Write me a login feature" |
| Concept Explain | what is, explain, principle | "What is React Hooks?" |
| Code Modify | modify, refactor, change | "Convert this to TypeScript" |
| Code Review | review, check, analyze | "Review this code for me" |
| Learning | teach, learn, understand | "Explain this concept to me" |

---

## 💻 Supported Languages

**Backend:** JavaScript, TypeScript, Python, Java, C, C++, C#, Go, Rust, PHP, Ruby, Swift, Kotlin

**Frontend:** HTML, CSS, React, Vue, Next.js, Angular

**Other:** SQL, Flutter/Dart, Shell/Bash

---

## 🚀 Quick Start

### Installation

```bash
clawhub install clarity-ai
```

### Usage

**Activate:**
```
You: 开启精准模式 / Enable precision mode
```

**Transform:**
```
You: Can you help me check this Python code, it seems to have some issues, thanks!
```

**Output:**
```markdown
## 🎯 Precision Instruction

**📌 Intent:** Code Debug
**💻 Language:** Python

**🎯 Goal:** Find and fix code issues

**💡 To help you better, please provide:**
- Code content
- Error message (if any)
```

**Deactivate:**
```
You: 关闭精准模式 / Disable precision mode
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│           User Input                 │
└─────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────┐
│        Rule Engine (Core)           │
│   Millisecond · Deterministic       │
└─────────────────────────────────────┘
                  ↓ (optional)
┌─────────────────────────────────────┐
│       Ollama Local AI              │
│    Smarter Semantic Understanding   │
└─────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────┐
│     Structured Precision Output     │
└─────────────────────────────────────┘
```

---

## 🔧 Advanced: Ollama Enhancement

Enable local AI for smarter understanding:

```bash
# Install Ollama
brew install ollama

# Download model (394MB)
ollama pull qwen:0.5b

# Start service
brew services start ollama
```

---

## 📈 Comparison

| Aspect | Engine | Ollama Enhanced |
|--------|--------|----------------|
| Speed | ⚡⚡⚡⚡ Millisecond | ⚡⚡⚡ Fast |
| Intelligence | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| Dependencies | None | Ollama |
| Privacy | 100% | 100% |

---

## 🎨 Use Cases

| Scenario | Benefit |
|----------|---------|
| 💬 Chat with AI | Get better responses |
| 💻 Code Debug | Describe issues precisely |
| 📚 Learning | Ask clearer questions |
| 🔍 Problem Solving | Faster resolution |

---

## 📝 Examples

### Example 1: Performance Issue

**Input:**
> Hi, about Python for loops, why is it running so slow, thanks

**Output:**
```markdown
## 🎯 Precision Instruction

**📌 Intent:** Performance Optimization
**💻 Language:** Python
**🎯 Focus:** Loop Structure

**🎯 Goal:** Analyze why for loop is slow
```

### Example 2: Code Creation

**Input:**
> Could you please help me write a user login function?

**Output:**
```markdown
## 🎯 Precision Instruction

**📌 Intent:** Code Creation
**💻 Language:** (not detected)

**🎯 Goal:** Create user login functionality

**💡 To help you better, please provide:**
- Specific requirements?
- Technology stack?
```

---

## 🤝 Contributing

Issues and pull requests are welcome!

---

## 📄 License

MIT License

---

<h3 align="center">
  Made with ❤️ for better AI communication
</h3>
