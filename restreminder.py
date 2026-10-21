import time
import subprocess
import sys
from pathlib import Path
import tkinter as tk
from tkinter import messagebox


class RestReminder:
	DURATION_SECONDS = 10
	MSG = "已持续" + str(DURATION_SECONDS) + "秒，宝子，注意休息..."

	def __init__(self, root):
		self.root = root
		self.root.title("休息提醒")
		self.button = tk.Button(
			root,
			text="开始计时",
			command=self.toggle_timer,
			bg="darkgreen",
			fg="white",
			activebackground="lightgreen",
			activeforeground="grey",
		)
		self.button.pack(padx=20, pady=20)

		self.state = "idle"
		self.elapsed = 0.0
		self.started_at = None
		self.after_id = None

	def toggle_timer(self):
		if self.state == "idle":
			self.state = "running"
			self.elapsed = 0.0
			self.started_at = time.monotonic()
			self.button.config(text="计时中")
			self.schedule_reminder()
		elif self.state == "running":
			self.elapsed += time.monotonic() - self.started_at
			self.state = "paused"
			if self.after_id is not None:
				self.root.after_cancel(self.after_id)
				self.after_id = None
			self.button.config(text="暂停计时")
		else:
			self.state = "running"
			self.started_at = time.monotonic()
			self.button.config(text="继续计时")
			self.schedule_reminder()

	def schedule_reminder(self):
		remaining = max(0.0, self.DURATION_SECONDS - self.elapsed)
		self.after_id = self.root.after(int(remaining * 1000), self.show_reminder)

	def show_reminder(self):
		self.after_id = None
		if self.state != "running":
			return
		self.state = "idle"
		self.elapsed = 0.0
		self.started_at = None
		messagebox.showinfo("休息提醒", self.MSG, parent=self.root)
		self.button.config(text="开始计时")


def build_executable():
	"""Create a standalone Windows executable using PyInstaller."""
	script = Path(__file__).resolve()
	subprocess.run(
		[
			sys.executable,
			"-m",
			"PyInstaller",
			"--onefile",
			"--windowed",
			"--noconfirm",
			"--name",
			"RestReminder",
			str(script),
		],
		check=True,
	)


if __name__ == "__main__" and sys.argv[1:] == ["--build"]:
	build_executable()
elif __name__ == "__main__":
	window = tk.Tk()
	window.configure(bg="lightblue")
	window.geometry("150x100")
	RestReminder(window)
	window.mainloop()
