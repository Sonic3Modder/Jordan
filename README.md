# jordan 🇯🇴

A lightweight, no-boilerplate prefix command handler built specifically for the **Hikari** Discord API wrapper. Designed to be completely immune to framework-version mismatches, fully supporting **Hikari 2.5.0+** and **Python 3.14+**.

---

## 📂 Internal Project Structure

To use `jordan` with a clean `import jordan` statement, make sure your project is structured like this:

```text
your_bot_project/
│
├── jordan/                  <-- The library folder
│   ├── __init__.py          <-- Exposes the handler
│   └── handler.py           <-- Core framework logic
│
└── main.py                  <-- Your actual bot script
