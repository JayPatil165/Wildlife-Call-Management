# 🐾 Wildlife Call Management Dashboard  

A **Streamlit-based dashboard** for managing and analyzing wildlife incident calls. This project provides an interactive interface to explore wildlife call data with KPIs, charts, and filters, powered by live data from Google Sheets.  

## 🚀 Features  
- 📊 **Interactive Data Visualization**  
  - Line, Bar, and Pie charts for incident trends and distributions  
  - KPIs for total calls, resolved cases, pending cases, etc.  
- 🔍 **Smart Filters**  
  - Filter incidents by date range, call type, severity, or status  
- ☁️ **Live Data Integration**  
  - Fetches data directly from **Google Sheets via OpenSheet API**  
- ⚡ **Lightweight & Fast**  
  - Powered by **Streamlit**, no backend setup required  
- 📱 **Responsive Layout**  
  - Clean and easy-to-use dashboard interface  

## 🛠️ Tech Stack  
- **Framework:** Streamlit  
- **Data Source:** Google Sheets (via OpenSheet API)  
- **Visualization:** Matplotlib, Plotly, Altair  
- **Deployment:** Streamlit Cloud / local server  

## 📂 Project Structure  
```
wildlife-dashboard-streamlit/
│── app.py             # Main Streamlit app
│── requirements.txt   # Dependencies
│── utils.py           # Helper functions
│── assets/            # Logos, images
│── README.md
```

## ⚙️ Installation & Setup  

1. **Clone the repository**  
```bash
git clone https://github.com/your-username/wildlife-dashboard-streamlit.git
cd wildlife-dashboard-streamlit
```

2. **Create a virtual environment & activate it**  
```bash
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
```

3. **Install dependencies**  
```bash
pip install -r requirements.txt
```

4. **Run the app locally**  
```bash
streamlit run app.py
```

## 🔗 Data Setup (Google Sheets)  
1. Create a **Google Sheet** with wildlife call records.  
2. Publish the sheet to the web.  
3. Get the **OpenSheet API link**:  
   ```
   https://opensheet.elk.sh/<SHEET_ID>/<SHEET_NAME>
   ```  
4. Update the API link in your `app.py` or config file.  

## 📸 Screenshots (Demo)  
_Add screenshots or GIFs of your Streamlit dashboard here._  

## 📌 Future Improvements  
- Add login/authentication  
- Role-based dashboards (e.g., for forest officers, analysts)  
- Export reports as **PDF/CSV**  
- Real-time alerts via email/SMS  

## 🤝 Contributing  
Contributions are welcome! Feel free to fork this repo, create a branch, and submit a pull request.  

## 📄 License  
This project is licensed under the **MIT License**.  
