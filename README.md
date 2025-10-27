# ECAR Assistant 2.0 / ЭКАР-Ассистент 2.0

RU
---
Десктоп‑ассистент для EdTech: помощь ученикам, техподдержке и внутр.операциям. Локальная LLM (Transformers), поиск (DuckDuckGo), TTS, история (SQLite), PyQt5 UI.

Основное:
- ИИ‑ответы и семантические подсказки
- Поиск в интернете + локальный кэш
- Озвучивание ответов (pyttsx3)
- История запросов в SQLite
- Кроссплатформенный PyQt5 UI

Установка:
```bash
pip install -r requirements.txt
cp .env.example .env
python ecar_assistant.py
```

EN
---
Desktop assistant for EdTech: student help, support automation and internal ops. Local LLM (Transformers), web search (DuckDuckGo), TTS, SQLite history, PyQt5 UI.

Features:
- AI responses and semantic hints
- Web search + local cache
- Text‑to‑speech (pyttsx3)
- SQLite request history
- PyQt5 cross‑platform UI

Setup:
```bash
pip install -r requirements.txt
cp .env.example .env
python ecar_assistant.py
```

Security: see SECURITY.md • License: MIT
