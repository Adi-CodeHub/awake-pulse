import ctypes
import os
import sys
import time
import threading
import webbrowser
import urllib.request
import json
import customtkinter as ctk

CURRENT_VERSION = "1.0.0"
GITHUB_REPO = "adityasharma/awake-pulse"  # Aap apna GitHub username/repo update kar sakte hain

def get_resource_path(relative_path: str) -> str:
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# ================= Windows Kernel Execution State Flags =================
ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001
ES_DISPLAY_REQUIRED = 0x00000002

class SleepPreventerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AwakePulse • Screen Sleep Preventer")
        self.geometry("420x570")
        self.resizable(False, False)

        icon_path = get_resource_path("icon.ico")
        if os.path.exists(icon_path):
            try:
                self.iconbitmap(icon_path)
            except Exception:
                pass

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.is_active = False
        self.start_time = None
        self.auto_timer_limit = 0

        self.setup_ui()
        self.check_for_updates_background()

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_ui(self):
        # Update Banner (Initially Hidden)
        self.update_banner = ctk.CTkFrame(self, fg_color="#1E3A8A", height=36, corner_radius=0)
        self.update_label = ctk.CTkLabel(
            self.update_banner,
            text="🚀 New Version Available!",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#93C5FD"
        )
        self.update_label.pack(side="left", padx=16, pady=4)

        self.update_btn = ctk.CTkButton(
            self.update_banner,
            text="Download",
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color="#3B82F6",
            hover_color="#2563EB",
            height=24,
            width=80,
            corner_radius=12,
            command=self.open_update_link
        )
        self.update_btn.pack(side="right", padx=16, pady=4)
        self.download_url = f"https://github.com/{GITHUB_REPO}/releases"

        # Header Section
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=24, pady=(20, 10))

        h_box = ctk.CTkFrame(header, fg_color="transparent")
        h_box.pack(fill="x")

        title = ctk.CTkLabel(
            h_box,
            text="⚡ AwakePulse",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#F8FAFC"
        )
        title.pack(side="left")

        version_badge = ctk.CTkLabel(
            h_box,
            text=f"v{CURRENT_VERSION}",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color="#64748B",
            fg_color="#0F172A",
            corner_radius=10,
            padx=8,
            pady=2
        )
        version_badge.pack(side="right")

        subtitle = ctk.CTkLabel(
            header,
            text="Native zero-overhead Windows screen & sleep prevention",
            font=ctk.CTkFont(size=12),
            text_color="#94A3B8"
        )
        subtitle.pack(anchor="w", pady=(2, 0))

        # Main Card Surface
        card = ctk.CTkFrame(
            self,
            corner_radius=16,
            fg_color="#1E293B",
            border_width=1,
            border_color="#334155"
        )
        card.pack(fill="both", expand=True, padx=24, pady=12)

        # Status Badge Indicator
        self.status_badge = ctk.CTkLabel(
            card,
            text="● SYSTEM SLEEP ALLOWED",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#94A3B8",
            fg_color="#0F172A",
            corner_radius=20,
            padx=14,
            pady=6
        )
        self.status_badge.pack(pady=(22, 10))

        # Active Session Timer
        self.timer_label = ctk.CTkLabel(
            card,
            text="00:00:00",
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color="#F8FAFC"
        )
        self.timer_label.pack(pady=4)

        timer_sub = ctk.CTkLabel(
            card,
            text="Active Awake Duration",
            font=ctk.CTkFont(size=11),
            text_color="#64748B"
        )
        timer_sub.pack(pady=(0, 18))

        # Master Toggle Switch
        toggle_container = ctk.CTkFrame(card, fg_color="#0F172A", corner_radius=12)
        toggle_container.pack(fill="x", padx=20, pady=8)

        toggle_label = ctk.CTkLabel(
            toggle_container,
            text="Sleep Prevention",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#F1F5F9"
        )
        toggle_label.pack(side="left", padx=16, pady=14)

        self.toggle_switch = ctk.CTkSwitch(
            toggle_container,
            text="",
            command=self.on_toggle,
            width=50,
            switch_width=44,
            switch_height=24,
            progress_color="#10B981"
        )
        self.toggle_switch.pack(side="right", padx=16)

        # Keep Display Active Checkbox
        self.keep_display_var = ctk.BooleanVar(value=True)
        self.display_checkbox = ctk.CTkCheckBox(
            card,
            text="Keep Display / Screen ON (not just CPU)",
            variable=self.keep_display_var,
            font=ctk.CTkFont(size=12),
            text_color="#CBD5E1",
            fg_color="#3B82F6",
            command=self.update_api_state
        )
        self.display_checkbox.pack(padx=20, pady=(14, 8), anchor="w")

        # Duration Selector
        timer_box = ctk.CTkFrame(card, fg_color="transparent")
        timer_box.pack(fill="x", padx=20, pady=(8, 14))

        timer_txt = ctk.CTkLabel(
            timer_box,
            text="Auto Stop Timer:",
            font=ctk.CTkFont(size=12),
            text_color="#94A3B8"
        )
        timer_txt.pack(side="left")

        self.timer_dropdown = ctk.CTkOptionMenu(
            timer_box,
            values=["Indefinite", "15 Mins", "30 Mins", "1 Hour", "2 Hours"],
            width=130,
            height=28,
            fg_color="#334155",
            button_color="#475569",
            command=self.on_timer_option_changed
        )
        self.timer_dropdown.pack(side="right")

        # Bottom Information
        footer = ctk.CTkLabel(
            self,
            text="🛡️ Native Windows execution state • Zero CPU usage",
            font=ctk.CTkFont(size=10),
            text_color="#64748B"
        )
        footer.pack(side="bottom", pady=12)

    def check_for_updates_background(self):
        def _check():
            try:
                url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
                req = urllib.request.Request(url, headers={"User-Agent": "AwakePulse-App"})
                with urllib.request.urlopen(req, timeout=3) as resp:
                    data = json.loads(resp.read().decode())
                    tag = data.get("tag_name", "").lstrip("v")
                    if tag and tag > CURRENT_VERSION:
                        self.download_url = data.get("html_url", self.download_url)
                        self.after(0, lambda: self.show_update_banner(tag))
            except Exception:
                pass
        threading.Thread(target=_check, daemon=True).start()

    def show_update_banner(self, new_ver: str):
        self.update_label.configure(text=f"🚀 Version {new_ver} Available!")
        self.update_banner.pack(side="top", fill="x", before=self.winfo_children()[1])

    def open_update_link(self):
        webbrowser.open(self.download_url)

    def on_timer_option_changed(self, choice):
        mapping = {
            "Indefinite": 0,
            "15 Mins": 15 * 60,
            "30 Mins": 30 * 60,
            "1 Hour": 60 * 60,
            "2 Hours": 120 * 60,
        }
        self.auto_timer_limit = mapping.get(choice, 0)

    def on_toggle(self):
        self.is_active = self.toggle_switch.get() == 1
        if self.is_active:
            self.start_time = time.time()
            self.status_badge.configure(
                text="● PREVENTING SLEEP (ACTIVE)",
                text_color="#10B981",
                fg_color="#064E3B"
            )
            self.update_api_state()
            self.run_timer_loop()
        else:
            self.stop_prevention()

    def update_api_state(self):
        if self.is_active:
            flags = ES_CONTINUOUS | ES_SYSTEM_REQUIRED
            if self.keep_display_var.get():
                flags |= ES_DISPLAY_REQUIRED
            ctypes.windll.kernel32.SetThreadExecutionState(flags)
        else:
            ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)

    def stop_prevention(self):
        self.is_active = False
        self.toggle_switch.deselect()
        self.status_badge.configure(
            text="● SYSTEM SLEEP ALLOWED",
            text_color="#94A3B8",
            fg_color="#0F172A"
        )
        self.timer_label.configure(text="00:00:00")
        ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)

    def run_timer_loop(self):
        if not self.is_active:
            return

        elapsed = int(time.time() - self.start_time)
        hrs = elapsed // 3600
        mins = (elapsed % 3600) // 60
        secs = elapsed % 60
        self.timer_label.configure(text=f"{hrs:02d}:{mins:02d}:{secs:02d}")

        if self.auto_timer_limit > 0 and elapsed >= self.auto_timer_limit:
            self.stop_prevention()
            return

        self.after(1000, self.run_timer_loop)

    def on_closing(self):
        ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
        self.destroy()

if __name__ == "__main__":
    app = SleepPreventerApp()
    app.mainloop()
