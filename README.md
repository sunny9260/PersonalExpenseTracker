💰 Personal Expense Tracker (Tkinter + AI)

A simple and elegant desktop app built using Python + Tkinter, designed to track your personal expenses, view summaries, export data, and even get AI-powered financial advice using OpenAI’s API.

🚀 Features

➕ Add and manage daily expenses

🗂️ Categorize spending (Food, Rent, Travel, etc.)

💾 Automatically saves data in a local CSV file

📊 View total and category-wise summaries

📤 Export expenses as CSV

🧹 Clear all data with confirmation

🤖 Get AI-based financial suggestions (via OpenAI API)

🪟 Simple, offline Tkinter GUI

🛠️ Tech Stack

Python 3.10+

Tkinter – GUI framework

Pandas – Data management

dotenv – API key configuration

OpenAI API – AI-powered advice

📦 Folder Structure
expense-tracker-ai/
│── expense_tracker_tkinter.py   # Main Tkinter app
│── requirements.txt              # Dependencies
│── README.md                     # Documentation
│── .env                          # API key file (optional)
│
└── data/
    └── expenses.csv              # Auto-created data file

⚙️ Installation

Clone this repository

git clone https://github.com/<your-username>/expense-tracker-ai.git
cd expense-tracker-ai


Install dependencies

pip install -r requirements.txt


(Optional) Create a .env file and add your OpenAI key:

OPENAI_API_KEY=your_openai_api_key_here


Run the app

python expense_tracker_tkinter.py

🧠 AI Financial Advice (Optional)

The AI feature analyzes your expense patterns and provides short, smart budgeting tips.

Works only if your .env file has a valid OpenAI key.

You’ll see a “Get AI Advice 🤖” button in the app.

📊 Example Screens

(Add screenshots of your running app here)

assets/
 └── screenshot1.png
 └── screenshot2.png

🧾 requirements.txt
pandas
python-dotenv
openai

📘 Documentation of Attempts

✅ Added persistent CSV storage for expense tracking

✅ Created a responsive Tkinter GUI

✅ Implemented category-wise and total summaries

✅ Integrated OpenAI for AI advice

⚠️ Fixed input validation (non-numeric amount handling)

⚠️ Added confirmation before clearing data

📌 Future Improvements

Add graphical visualizations (matplotlib bar charts)

Include monthly budget goals

Multi-user login system

PDF report export
