🕒 SilentFocus – Smart Pomodoro Desktop App

SilentFocus is a Python-based desktop Pomodoro application designed to help users build sustainable focus habits through structured work–break cycles and context-aware feedback.

The application follows the Pomodoro technique while adding a lightweight, rule-based “focus assistant” that provides short, supportive insights based on the user’s behavior during the session.

⸻

🎯 Features
	•	Work, break, and long break cycles based on the Pomodoro technique
	•	Automatic long breaks after every 4 completed work sessions
	•	Soft extension system for work and break periods
	•	Context-aware focus feedback (non-LLM, rule-based logic)
	•	Desktop notifications when session modes change
	•	Clean and minimal desktop UI

⸻

🛠️ Technologies Used
	•	Python 3
	•	PySide6 (Qt for Python) for the desktop interface
	•	Modular architecture (UI / logic separation)
	•	Rule-based focus analysis (no external AI dependency)

⸻

🔔 System Notifications

SilentFocus sends native operating system notifications whenever the session mode changes
(e.g., Work → Break, Break → Work, Long Break).

This helps users stay aware of transitions without constantly checking the app.

⸻

📦 Requirements
	•	Python 3.10+
	•	PySide6

Install dependencies: 

```bash
pip install PySide6
```

Run the application:
```bash
python main.py
```

🧠 Project Purpose

This project was developed to:
	•	Practice building real desktop applications with Python
	•	Explore focus-oriented UX design
	•	Apply clean code principles and modular architecture
	•	Simulate intelligent behavior using deterministic logic instead of external AI services

⸻

👩‍💻 Author

Zeynep Kediz
Computer Engineering Student
Interested in Artificial Intelligence, Machine Learning, and Python desktop applications

📫 Contact: kedizzeynep@gmail.com

