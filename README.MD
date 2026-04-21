# PR Reviewer CLI (AI-powered)

A simple CLI tool to review GitHub PRs using AI.

---

## 🚀 Setup

### 1. Clone the project

---

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file in root:

```env
# GitHub
GITHUB_TOKEN=your_github_token
GITHUB_REPO=owner/repo

# Gemini
GOOGLE_API_KEY=your_gemini_key
MODEL_NAME=your_gemini_model_name
```

### Notes

- `GITHUB_TOKEN`: must have repo + PR access
- `GITHUB_REPO`: format → `owner/repository`
- `GOOGLE_API_KEY`: get from Google AI Studio
- `MODEL_NAME`: keep as `gemini-1.5-flash`

---

## ▶️ Run

```bash
python cli.py
```

---

## 💻 Usage

### Review PR

```bash
review #23
```

### Multiple PRs

```bash
review #23,#24
```

---

## 🔁 Refinement Loop

After review:

### Give instruction

```bash
refine your instructions
```

### Reset given instructions

```bash
reset
```

---

## ✅ Confirm & Post Review

```bash
confirm
```
