# 🛡️ Commit Guardian

**Commit Guardian** is a lightweight security pre-commit hook that scans your code for hardcoded secrets, environment misconfigurations, and insecure development leftovers before they ever reach your repository.

> Built to protect your commits in `dev`, `staging`, and `production` environments.

---

## 🚀 Features

- ✅ Detects hardcoded **passwords, API keys, tokens, DB credentials**
- ⚠️ Warns about insecure logs (`print`, `console.log`, etc.) in `staging`
- ❌ Blocks commits with dangerous config like `DEBUG = True` or `ALLOWED_HOSTS = ["*"]` in `production`
- 🌐 Environment-aware: behaves differently in `dev`, `staging`, and `prod`
- 🔧 Easy to configure with YAML + JSON

---

## 📁 Project Structure

```
commit-guardian/
├── .pre-commit-config.yaml         # Hook definition
├── config/
│   └── default.json                # Environment config
├── hooks/
│   └── pre-commit.py               # Entry point script
├── rules/
│   └── patterns.yaml               # Regex rules
├── utils/
│   └── file_scanner.py             # Scanner logic
```

---

## ⚙️ Setup

### 1. Install Pre-Commit

```bash
pip install pre-commit
```

### 2. Set the environment

Edit `config/default.json`:

```json
{ "env": "staging" }
```

Options: `"dev"`, `"staging"`, `"prod"`

### 3. Install the hook

```bash
pre-commit install
```

### 4. Test the hook

```bash
pre-commit run --all-files
```

---

## 🧠 Example Detections

| Environment | Pattern | Action |
|-------------|---------|--------|
| Any         | `password="secret123"` | ❌ Block |
| Staging     | `print("debugging")`   | ⚠️ Warn |
| Prod        | `DEBUG = True`         | ❌ Block |
| Prod        | `ALLOWED_HOSTS = ["*"]`| ❌ Block |

---

## 🧩 Customize Rules

You can edit `rules/patterns.yaml` to add or remove regex patterns per environment.

Example:

```yaml
secrets:
  - "(?i)api_key\s*=\s*["'].*["']"
```

---

## 📣 Contributing

Feel free to fork and enhance the tool. Ideas for next versions:
- Scan staged diffs instead of full files
- GitHub Action integration
- Dashboard or audit logging

---

## 🧑‍💻 Author

Made with love by [Paolo Veliz](https://www.linkedin.com/in/tu-perfil), Fullstack Developer + Security Enthusiast 🇬🇹

---

## 📄 License

MIT – Use freely, contribute openly.
