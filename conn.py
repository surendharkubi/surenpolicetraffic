# 1. Import necessary libraries
import streamlit as st  # For building the web UI
import pandas as pd  # For data handling
import pymysql  # For MySQL database connection
from pymysql.cursors import DictCursor  # Import DictCursor for dictionary results
import plotly.express as px  # For creating visual charts
from pymysql.cursors import DictCursor  # Import DictCursor for dictionary results

# 2. Function to create database connection
def create_connection():  # Define a function to establish a database connection
    try:  # Attempt to connect to the database
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='12345',
            db='surenpolicetraffic',
            cursorclass=DictCursor
        )
        return connection  # Return the established connection
    except Exception as e:  # Handle any exceptions that occur during connection
        st.error(f"Database Connection Error: {e}")  # Display an error message in the Streamlit app
        return None  # Return None if connection fails

# 3. Function to fetch query results from DB and return as DataFrame
def fetch_data(query):  # Define a function to fetch data from the database
    connection = create_connection()  # Establish a database connection
    if connection:  # Check if the connection is successful
        try:  # Attempt to execute the query
            with connection.cursor() as cursor:  # Use a cursor to execute the query
                cursor.execute(query)  # Execute the query
                result = cursor.fetchall()  # Fetch all the results
                return pd.DataFrame(result)  # Convert the results to a Pandas DataFrame
        except Exception as e:  # Handle any exceptions that occur during query execution
            st.error(f"Error Fetching Data: {e}")  # Display an error message in the Streamlit app
            return pd.DataFrame()  # Return an empty DataFrame if query fails
        finally:  # Ensure the connection is closed regardless of the outcome
            connection.close()  # Close the database connection
    else:  # If the connection fails
        return pd.DataFrame()  # Return an empty DataFrame

# 4. Page config and title
st.set_page_config(page_title="SecureCheck Police Dashboard", layout='wide')  # Set the page title and layout
st.title("SecureCheck: Police Check Post Digital Leader 🚨")  # Display the title of the app
st.markdown("Real-time monitoring and insights for law enforcement 👮")  # Display a subtitle

# 5. Show full dataset
st.header("Police Logs Overview 📊")  # Display a header for the dataset section
query = 'SELECT * FROM cleaned_data_ok'  # Define a query to fetch the entire dataset
data = fetch_data(query)  # Fetch the data using the defined function

if not data.empty:  # Check if the dataset is not empty
    st.dataframe(data, use_container_width=True)  # Display the dataset in the app
else:  # If the dataset is empty
    st.warning("No data available")  # Display a warning message

# 6. Display key metrics
st.header("Key Metrics 📈")  # Display a header for the key metrics section
if not data.empty:  # Check if the dataset is not empty
    col1, col2, col3, col4 = st.columns(4)  # Create four columns for the metrics

    with col1:  # Column 1
        total_stops = data.shape[0]  # Calculate the total number of stops
        st.metric("Total Police Stops 🚨", total_stops)  # Display the total stops metric

    with col2:  # Column 2
        arrests = data[data['stop_outcome'].astype(str).str.contains('arrest', case=False, na=False)].shape[0]  # Calculate the number of arrests
        st.metric("Total Arrests 👮", arrests)  # Display the total arrests metric

    with col3:  # Column 3
        warnings = data[data['stop_outcome'].astype(str).str.contains('warning', case=False, na=False)].shape[0]  # Calculate the number of warnings
        st.metric("Total Warnings ⚠️", warnings)  # Display the total warnings metric

    with col4:  # Column 4
        drug_related = data[data['drugs_related_stop'].astype(int) == 1].shape[0]  # Calculate the number of drug-related stops
        st.metric("Drugs Related Stops 💊", drug_related)  # Display the total drug-related stops metric
else:  # If the dataset is empty
    st.warning("No data available for metrics")  # Display a warning message

# 7. Visual insights tabs
st.header("Visual Insights 📊")  # Display a header for the visual insights section
tab1, tab2 = st.tabs(["Stops by Violation 🚨", "Driver Gender Distribution 👥"])  # Create two tabs for visual insights

with tab1:  # Tab 1: Stops by Violation
    if not data.empty and "violation" in data.columns:  # Check if the dataset is not empty and has a 'violation' column
        # Count violations and reset index
        violation_counts = data["violation"].value_counts().reset_index()  # Count the occurrences of each violation
        violation_counts.columns = ['violation', 'count']  # Rename the columns for clarity

        # Create bar chart
        fig = px.bar(violation_counts, x='violation', y='count', title="Stops by Violation Type 🚨")  # Create a bar chart using Plotly Express
        fig.update_layout(xaxis_title="Violation", yaxis_title="Count")  # Update the layout of the chart
        st.plotly_chart(fig, use_container_width=True)  # Display the chart in the app
    else:  # If the dataset is empty or lacks the 'violation' column
        st.warning("No data available for Violation Chart. 🚫")  # Display a warning message

with tab2:  # Tab 2: Driver Gender Distribution
    if not data.empty and 'driver_gender' in data.columns:  # Check if the dataset is not empty and has a 'driver_gender' column
        gender_counts = data['driver_gender'].value_counts().reset_index()  # Count the occurrences of each gender
        gender_counts.columns = ['gender', 'count']  # Rename the columns for clarity

        fig = px.pie(gender_counts, names='gender', values='count', title='Driver Gender Distribution 👥')  # Create a pie chart using Plotly Express
        fig.update_layout(legend_title="Gender")  # Update the layout of the chart
        st.plotly_chart(fig, use_container_width=True)  # Display the chart in the app
    else:  # If the dataset is empty or lacks the 'driver_gender' column
        st.warning("No data available for Driver Gender chart. 🚫")  # Display a warning message

# 8. Advanced queries dropdown
st.header("Advanced Insights 🔍")  # Display a header for the advanced insights section
selected_query = st.selectbox("Select a Query to Run", [  # Create a dropdown for selecting queries
    "Total Number of Police Stops",
    "Count of Stops by Violation Type",
    "Number of Arrests vs. Warnings",
    "Average Age of Drivers Stopped",
    "Top 5 Most Frequent Search Types",
    "Count of Stops by Gender",
    "Most Common Violation for Arrests"
])

# 9. Query mapping
query_map = {  # Define a dictionary mapping query names to SQL queries
    "Total Number of Police Stops": "SELECT COUNT(*) AS total_stops FROM cleaned_data_ok",
    "Count of Stops by Violation Type": "SELECT violation, COUNT(*) AS count FROM cleaned_data_ok GROUP BY violation ORDER BY count DESC",
    "Number of Arrests vs. Warnings": "SELECT stop_outcome, COUNT(*) AS count FROM cleaned_data_ok GROUP BY stop_outcome",
    "Average Age of Drivers Stopped": "SELECT AVG(driver_age) AS average_age FROM cleaned_data_ok",
    "Top 5 Most Frequent Search Types": "SELECT search_type, COUNT(*) AS count FROM cleaned_data_ok WHERE search_type != '' GROUP BY search_type ORDER BY count DESC LIMIT 5",
    "Count of Stops by Gender": "SELECT driver_gender, COUNT(*) AS count FROM cleaned_data_ok GROUP BY driver_gender",
    "Most Common Violation for Arrests": "SELECT violation, COUNT(*) AS count FROM cleaned_data_ok WHERE stop_outcome LIKE '%arrest%' GROUP BY violation ORDER BY count DESC"
}

# 10. Run query button
if st.button("Run Query 🚀"):  # Create a button to run the selected query
    result = fetch_data(query_map[selected_query])  # Fetch the data using the defined function
    if not result.empty:  # Check if the result is not empty
        st.dataframe(result, use_container_width=True)  # Display the result in the app
    else:  # If the result is empty
        st.warning("No data available for the selected query. 🚫")  # Display a warning message

st.markdown("---")  # Display a horizontal line
st.markdown("Built with ❤️ for Law Enforcement by SecureCheck")  # Display a footer

# 11. Natural Language Filter (UI only)
st.header("Custom Natural Language Filter 🤖")  # Display a header for the natural language filter section
st.markdown("Fill in the details below to get a natural language prediction of the stop outcome based on existing data.")  # Display a description

if not data.empty and 'stop_duration' in data.columns:
    stop_duration_options = data["stop_duration"].dropna().unique().tolist()
else:
    stop_duration_options = ["0-15 Min", "16-30 Min", "30+ Min"]  # default options
# 12. Form to add new log and predict
st.header("Add New Police Log & Predict Outcome and Violation 📝")  # Display a header for the prediction section
with st.form("new_log_form"):  # Create a form for adding new logs
    stop_date = st.date_input("Stop Date")  # Input field for stop date
    stop_time = st.time_input("Stop Time")  # Input field for stop time
    country_name = st.text_input("Country Name")  # Input field for country name
    driver_gender = st.selectbox("Driver Gender", ["male", "female"])  # Dropdown for driver gender
    driver_age = st.number_input("Driver Age", min_value=16, max_value=100, value=27)  # Input field for driver age
    driver_race = st.text_input("Driver Race")  # Input field for driver race
    search_conducted = st.selectbox("Was a Search Conducted?", ["0", "1"])  # Dropdown for search conducted
    drugs_related_stop = st.selectbox("Was it Drug Related?", ["0", "1"])  # Dropdown for drug-related stop
    stop_duration = st.selectbox("Stop Duration", stop_duration_options)  # Dropdown for stop duration
    vechicle_number = st.text_input("Vechicle Number")  # Input field for vehicle number
    timestamp = pd.Timestamp.now()  # Get the current timestamp

    submitted = st.form_submit_button("Predict Stop Outcome & Violation")  # Create a button to submit the form

    if submitted:  # If the form is submitted
        # Filter data based on input
        filtered_data = data[
            (data['driver_gender'] == driver_gender) &
            (data['driver_age'] == driver_age) &
            (data['search_conducted'] == int(search_conducted)) &
            (data['stop_duration'] == stop_duration) &
            (data['drugs_related_stop'] == int(drugs_related_stop))
        ]

        if not filtered_data.empty:  # Check if the filtered data is not empty
            predicted_outcome = filtered_data['stop_outcome'].mode()[0]  # Predict the stop outcome
            predicted_violation = filtered_data['violation'].mode()[0]  # Predict the violation
        else:  # If the filtered data is empty
            predicted_outcome = "warning"  # Fallback prediction for stop outcome
            predicted_violation = "speeding"  # Fallback prediction for violation

        # Human-readable summary
        search_text = "A search was conducted" if int(search_conducted) else "NO search was conducted"
        drug_text = "was drug-related" if int(drugs_related_stop) else "was not drug related"

        st.markdown(f"""
        **Predicted Summary**
        
        - **Predicted Violation**: {predicted_violation}  
        - **Predicted Stop Outcome**: {predicted_outcome}  
        A {driver_age}-year-old {driver_gender} driver in {country_name} was stopped at {stop_time.strftime('%I:%M %p')} on {stop_date}.  
        {search_text}, and the stop {drug_text}.  
        Stop Duration: **{stop_duration}**  
        Vehicle Number: **{vechicle_number}**
        """)  # Display the predicted summary