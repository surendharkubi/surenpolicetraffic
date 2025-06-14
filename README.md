# README for SecureCheck Police Dashboard

## 📌 Overview
SecureCheck is a comprehensive police dashboard application designed to provide real-time monitoring and insights for law enforcement agencies. The application connects to a MySQL database (`skpolice`) to display and analyze traffic stop data.

## 🚀 Features
1. **Real-time Data Visualization**: View all police stop records in an interactive table
2. **Key Metrics Dashboard**: Track important statistics like total stops, arrests, warnings, and drug-related stops
3. **Visual Insights**: Interactive charts showing stops by violation type and driver gender distribution
4. **Advanced Query System**: 19 pre-built analytical queries to uncover patterns and trends
5. **Prediction System**: Predict stop outcomes based on historical data patterns
6. **Data Entry Form**: Add new police logs directly through the interface

## 🛠️ Technical Requirements
- Python 3.7+
- Required Python packages:
  - streamlit
  - pandas
  - pymysql
  - plotly
  - numpy

## 🗄️ Database Setup
1. MySQL database named `skpolice`
2. Table structure:
   ```sql
   CREATE TABLE surenpolicetraffic (
       id INT AUTO_INCREMENT PRIMARY KEY,
       stop_date DATE,
       stop_time TIME,
       country_name VARCHAR(100),
       driver_gender VARCHAR(10),
       driver_age INT,
       driver_race VARCHAR(50),
       violation VARCHAR(100),
       search_conducted BOOLEAN,
       stop_outcome VARCHAR(50),
       is_arrested BOOLEAN,
       stop_duration VARCHAR(50),
       drugs_related_stop BOOLEAN,
       vehicle_number VARCHAR(50)
   );
   ```

## ⚙️ Installation
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure database connection in the script:
   ```python
   connection = pymysql.connect(
       host='localhost',
       user='root',
       password='12345',
       db='skpolice',
       cursorclass=DictCursor
   )
   ```

## 🏃 Running the Application
```bash
streamlit run police_dashboard.py
```

## 📊 Available Analytical Queries
The dashboard includes 19 pre-built queries covering:
- Basic stop statistics
- Demographic analysis
- Time-based patterns
- Violation trends
- Location-based insights
- Complex multi-dimensional analysis

## 🤖 Prediction System
The application can predict likely stop outcomes based on:
- Driver demographics (age, gender, race)
- Search conducted status
- Stop duration
- Drug-related status

## 📝 License
This project is open-source and available for law enforcement use.

## 📧 Contact
For support or customization requests, please contact the development team.

---

Built with ❤️ for Law Enforcement by SecureCheck Team
