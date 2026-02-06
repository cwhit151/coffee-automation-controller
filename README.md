# coffee-automation-controller
Marketing control system 
# ☕ Coffee Automation Controller

A simple Streamlit web app used to control Make.com marketing automations (Instagram posting + photo recycling) using an ON/OFF toggle.

This project is designed to act like a "water valve" for automation — instead of logging into Make every time, you can enable or disable automations from a clean web dashboard.

---

## 🚀 Features

- Toggle Instagram posting automation ON/OFF
- Toggle photo recycling automation ON/OFF
- Controls automations through a Google Sheets flag system
- Built with Streamlit (fast, lightweight, deployable)

---

## 🛠 How It Works

This app updates a Google Sheet that stores automation settings (ex: `TRUE/FALSE` values).

Each Make.com scenario checks that sheet before running.

If the automation flag is `FALSE`, Make stops immediately.

---

## 📂 Folder Structure

