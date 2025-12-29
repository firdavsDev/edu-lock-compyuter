# EduLock

A minimal, focus-first desktop app that locks a frameless window on top and challenges you with quick math problems. Each day you answer a fixed number of questions under a time limit. Answers and session progress are stored locally in SQLite.

## Overview
- Always-on-top, frameless window keeps focus on the task
- Random arithmetic questions (+, −, ×, ÷ with safe divisibility)
- Per-question countdown timer
- Daily target with automatic session completion
- Local SQLite storage for sessions and answers
- Optional autostart when packaged on Windows

## Features
- **Focus Lock:** Enforced via Qt flags and a periodic focus check in [app/security/window_lock.py](app/security/window_lock.py).
- **Daily Goal:** `QUESTIONS_PER_DAY` from [app/config.py](app/config.py) defines how many questions per day.
- **Timer:** `TIME_LIMIT_SECONDS` from [app/config.py](app/config.py) sets seconds per question.
- **Math Engine:** Random problems from [app/core/math_engine.py](app/core/math_engine.py) using +, −, ×, ÷. Division ensures integer results.
- **Persistence:** SQLite DB created and managed by [app/persistence/db.py](app/persistence/db.py). CRUD handled in [app/persistence/repository.py](app/persistence/repository.py) with data models in [app/persistence/models.py](app/persistence/models.py).
- **Autostart (Windows only):** See [app/security/autostart.py](app/security/autostart.py). Active when running a packaged `.exe`.

## Requirements
- Python 3.10+ (PyQt6 is listed in requirements)
- macOS or Windows (Linux likely fine but untested)
- Dependencies: see [requirements.txt](requirements.txt)

Install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\\Scripts\\activate  # Windows PowerShell
pip install -r requirements.txt
```

## Run (Development)
Run the app directly:

```bash
python -m app.main
```

Or use the helper script:

```bash
./start.sh
```

Entry point: [app/main.py](app/main.py). Main window: [app/ui/main_window.py](app/ui/main_window.py).

## Build (PyInstaller)
Create a single-file build (GUI, no console):

```bash
pip install pyinstaller
./build.sh
```

Artifacts will be in `dist/` (e.g., `dist/EduLock`). On Windows, the packaged `.exe` can autostart via [app/security/autostart.py](app/security/autostart.py). On macOS, autostart is disabled by design in this app.

Notes:
- If PyQt resources are missing at runtime, ensure PyInstaller finds Qt plugins. You may need `--add-data` for some environments.
- The spec file [EduLock.spec](EduLock.spec) is available if you prefer `pyinstaller EduLock.spec`.

## Configuration
Adjust behavior in [app/config.py](app/config.py):
- **`QUESTIONS_PER_DAY`**: Number of questions required per day.
- **`TIME_LIMIT_SECONDS`**: Seconds per question.
- **`MIN_NUMBER` / `MAX_NUMBER`**: Range for generated numbers.
- **`DB_NAME`**: SQLite file name (defaults to `edu_lock.db`).

## Data Storage
- SQLite DB file: created on first run as `edu_lock.db` in the working directory.
- Tables: `sessions` and `answers` created by [app/persistence/db.py](app/persistence/db.py).
- In-app data types: see [app/persistence/models.py](app/persistence/models.py).

## Design Notes
- The window is intentionally hard to close. `closeEvent` is ignored in [app/ui/main_window.py](app/ui/main_window.py) to maintain focus. The app exits when the daily session completes.
- The window lock uses `WindowStaysOnTopHint` and periodic `activateWindow()` to retain focus.
- Division questions are generated as divisible pairs to avoid fractional answers; evaluation is safe-cast to `int`.

## Troubleshooting
- **Cannot close the window:** This is by design. Complete the session or modify `closeEvent` in [app/ui/main_window.py](app/ui/main_window.py).
- **Database not updating:** Verify write permissions in the working directory and that `Database.init()` runs (called in [app/main.py](app/main.py)).
- **Build issues on macOS:** Ensure you’re using a supported Python and PyQt6 version. Try `pyinstaller EduLock.spec` if `build.sh` doesn’t capture all resources.

## Project Structure
- App logic: [app/core](app/core)
- Persistence: [app/persistence](app/persistence)
- Security/lock: [app/security](app/security)
- UI and widgets: [app/ui](app/ui)

## License
Internal/Personal project. Add a license section if you plan to distribute.
