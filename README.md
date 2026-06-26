# 📊 Project Monitoring Dashboard (LU)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Google Sheets](https://img.shields.io/badge/Google_Sheets-34A853?style=for-the-badge&logo=google-sheets&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)

A modern, interactive, and cloud-integrated web dashboard designed to track and monitor the progress of Learning Unit (LU) materials (Videos, Articles, Infographics, Audio, and Quizzes). Built with a minimalist Red & White UI.

## ✨ Key Features

* **📊 Analytics Dashboard:** Real-time data visualization including key metrics, overall status distribution (Pie Chart), progress per category (Bar Chart), and daily completion trends (Line Chart).
* **📝 Interactive Live Editor:** Edit data directly through the web interface with double-click interactions. No need to open the raw spreadsheet.
* **🔄 Cloud Synchronization:** Seamless two-way integration with Google Sheets API. Push updates and finalize data with a single click.
* **🧠 Smart Status Tracking:** Automatically calculates completion rates (treats both "Selesai" and "Under Review" as completed tasks).
* **🎨 Minimalist UI/UX:** Clean, responsive, and distraction-free design.

## 🛠️ Tech Stack

* **Frontend & Backend:** [Streamlit](https://streamlit.io/)
* **Data Manipulation:** [Pandas](https://pandas.pydata.org/)
* **Data Visualization:** [Plotly Express](https://plotly.com/python/plotly-express/)
* **Database connection:** `st-gsheets-connection` (Google Sheets API)

## 🚀 Local Installation & Setup

To run this project locally on your machine, follow these steps:

### 1. Clone the repository
```bash
git clone [https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git](https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git)
cd YOUR-REPO-NAME
2. Install dependencies
Ensure you have Python installed, then run:

Bash
pip install -r requirements.txt
3. Setup Google Sheets Credentials
This app requires a Google Cloud Service Account to read and write to Google Sheets.

Create a project in Google Cloud Console.

Enable Google Sheets API and Google Drive API.

Create a Service Account and generate a JSON key.

Share your target Google Sheet file with the Service Account email (give Editor access).

Create a folder named .streamlit in the root of your project.

Inside it, create a file named secrets.toml and format your JSON credentials like this:

Ini, TOML
[connections.gsheets]
spreadsheet = "[https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit](https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit)"
type = "service_account"
project_id = "..."
private_key_id = "..."
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "..."
client_id = "..."
auth_uri = "[https://accounts.google.com/o/oauth2/auth](https://accounts.google.com/o/oauth2/auth)"
token_uri = "[https://oauth2.googleapis.com/token](https://oauth2.googleapis.com/token)"
auth_provider_x509_cert_url = "[https://www.googleapis.com/oauth2/v1/certs](https://www.googleapis.com/oauth2/v1/certs)"
client_x509_cert_url = "..."
(Note: Never commit your secrets.toml file to GitHub!)

4. Run the Application
Bash
streamlit run app.py
🌐 Deployment (Streamlit Community Cloud)
Push your code (app.py and requirements.txt) to a public/private GitHub repository.

Log in to Streamlit Community Cloud.

Click New app and select your repository.

Before clicking Deploy, go to Advanced settings (⚙️ icon) and paste the contents of your secrets.toml into the Secrets text box.

Click Deploy!
