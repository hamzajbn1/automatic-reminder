📧 Automated Invoice Reminder

## 👋 About The Project
I built this automation tool to solve a specific problem: manually checking Excel sheets for unpaid invoices and writing email reminders is tedious and prone to error.

This Python script automates the entire process. It reads a local dataset (`data.csv`), checks who is late on their payment, and uses the **Gmail API** to send them a personalized, professional HTML email instantly.

It was a great project for me to learn how to connect Python scripts to real-world APIs and handle data securely.

## ⚙️ How It Works
* **Smart Date Checking:** The script runs through my client list using **Pandas**. It compares today's date with the `reminder_date` column to decide exactly who needs an email.
* **No Hardcoded Passwords:** Instead of putting my Gmail password in the code (which is unsafe), I implemented **OAuth 2.0**. The script logs in once via a browser window, saves a secure token, and uses that for future runs.
* **Custom HTML Emails:** I didn't want to send plain text. The script injects the client's name, invoice number, and amount into an HTML template so the emails look professional.

## 🛠️ Tech Stack
* **Python 3.10+**
* **Pandas** (for reading CSVs and handling dates)
* **Gmail API & Google Client Library** (for sending the emails)
* **OAuth 2.0** (for secure authentication)

* Security Note
You won't find my client_secret.json or data.csv files here. I excluded them using .gitignore to keep my API keys and personal data safe. You will need to provide your own to test the code!
