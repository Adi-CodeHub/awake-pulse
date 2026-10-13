# ⚡ AwakePulse (Screen Sleep Preventer for Windows)

A lightweight, modern Windows desktop application that prevents your PC and screen from sleeping, locking, or triggering screensavers — **with zero CPU overhead and zero mouse-jiggling tricks**.

---

## ✨ Features

- **⚡ Native Windows Kernel Execution:** Calls `SetThreadExecutionState` directly in `kernel32.dll`. No fake mouse movement, no lags, no CPU usage.
- **🎨 Modern Dark Mode UI:** Built with CustomTkinter for a sleek, high-contrast fintech aesthetic.
- **⏱️ Live Session Timer:** Tracks exactly how long your machine has been kept awake.
- **⏳ Auto-Stop Presets:** Keep awake indefinitely or auto-stop after 15 mins, 30 mins, 1 hour, or 2 hours.
- **🖥️ Display Toggle:** Choose whether to keep only the CPU awake (for long downloads) or keep both Display and CPU awake.
- **🚀 Built-in Auto-Update Checker:** Automatically notifies you whenever a new release is available on GitHub.
- **📦 Single Standalone Executable:** No Python or dependencies required to run!

---

## 📥 Download & Installation

0. Go to the [**Website**](https://adi-codehub.github.io/awake-pulse/).
1. Go to the [**Releases**](https://github.com/Adi-CodeHub/awake-pulse/releases) section.
2. Download `AwakePulse-v1.0.0.zip`.
3. Extract the ZIP and double-click **`AwakePulse.exe`**.
4. *(Optional)* Right-click `AwakePulse.exe` $\rightarrow$ **Send to $\rightarrow$ Desktop (create shortcut)**.

> **Note on Windows SmartScreen:**  
> On first launch, Windows might show a blue *"Windows protected your PC"* popup because the binary is open-source and not signed with an enterprise certificate. Simply click **"More info"** $\rightarrow$ **"Run anyway"**.

---

## 🛠️ For Developers (Build from Source)

This project uses [`uv`](https://github.com/astral-sh/uv) for ultra-fast dependency management.

### Prerequisites
- Python 3.12+
- `uv` package manager installed (`pip install uv` or `winget install astral-sh.uv`)

### 1. Clone the repository
```bash
git clone https://github.com/Adi-CodeHub/awake-pulse.git
cd awake-pulse
```

### 2. Install dependencies & Run
```bash
uv sync
uv run python main.py
```

### 3. Build Single Standalone `.exe`
```bash
uv run pyinstaller --noconsole --onefile --icon="icon.ico" --add-data "icon.ico;." --collect-all customtkinter --name "AwakePulse" main.py
```
The final binary will be generated inside `dist/AwakePulse.exe`.

---

## 🛡️ License
MIT License. Free to use and distribute.
