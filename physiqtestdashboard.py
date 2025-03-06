import streamlit as st
import pandas as pd

# Set page configuration for a wide layout and a custom title.
st.set_page_config(page_title="Creative Performance Dashboard", layout="wide")

# Custom CSS for dark mode and branding
st.markdown("""
    <style>
    .stApp {
        background-color: #121212;
        color: white;
    }
    .css-1aumxhk, .css-18e3th9, .css-1v3fvcr, .css-1d391kg, .stDataFrame, .stMarkdown {
        color: white;
    }
    .stDataFrame {
        background-color: #1e1e1e;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #96c93d;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------
# Data Loading and Cleaning
# -------------------------------
@st.cache_data
def load_data(uploaded_file):
    # Load the data from the uploaded Excel file and clean it.
    df = pd.read_excel(uploaded_file, sheet_name='Ad Insights')
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    df.dropna(how='all', inplace=True)
    # Add additional cleaning logic if needed
    return df

# -------------------------------
# Main Dashboard Code
# -------------------------------
def main():
    # File uploader for the Excel file.
    uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

    if uploaded_file:
        df = load_data(uploaded_file)

        # Dashboard Title
        st.title("📈 Physiq Creative Performance Dashboard")

        # -------------------------------
        # Top-Level Metrics
        # -------------------------------
        st.header("🏅 Top-Level Metrics")
        location_metrics = df.groupby('campaign').agg({
            'amount_spent': 'sum',
            'sync_acquire_lead': 'sum',
            'sync_acquire_membership': 'sum'
        }).rename(columns={
            'amount_spent': 'Total Spend', 
            'sync_acquire_lead': 'Leads', 
            'sync_acquire_membership': 'Memberships'
        })
        st.dataframe(location_metrics, use_container_width=True)

        # -------------------------------
        # Overall Metrics
        # -------------------------------
        st.header("Overall Metrics")
        total_spent = df['amount_spent'].sum()
        total_impressions = df['impressions'].sum()
        total_clicks = df['clicks'].sum()
        avg_ctr = df['ctr'].mean()
        total_leads = df['sync_acquire_lead'].sum()

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Spend", f"${total_spent:,.2f}")
        col2.metric("Total Impressions", f"{total_impressions:,}")
        col3.metric("Total Clicks", f"{total_clicks:,}")
        col4.metric("Total Leads", total_leads)

        # -------------------------------
        # Spend by Campaign
        # -------------------------------
        st.subheader("💰 Spend by Campaign")
        campaign_spend = df.groupby('campaign')['amount_spent'].sum().sort_values(ascending=False)
        st.bar_chart(campaign_spend, use_container_width=True)

        # -------------------------------
        # Clicks & CTR by Campaign
        # -------------------------------
        st.subheader("🖱️ Clicks and CTR by Campaign")
        click_ctr = df.groupby('campaign').agg({'clicks':'sum', 'ctr':'mean'}).sort_values(by='clicks', ascending=False)
        st.dataframe(click_ctr, use_container_width=True)

        # -------------------------------
        # Impressions vs Spend Scatter Plot
        # -------------------------------
        st.subheader("🚀 Impressions vs. Spend")
        # Using st.scatter_chart for a quick scatter plot.
        st.scatter_chart(df[['amount_spent', 'impressions']])

        # -------------------------------
        # Frequency and Reach Visualization
        # -------------------------------
        st.subheader("📡 Frequency & Reach")
        reach_frequency = df[['campaign', 'reach', 'frequency']].groupby('campaign').mean()
        st.bar_chart(reach_frequency)

        # -------------------------------
        # Conversion Tracking
        # -------------------------------
        st.subheader("✅ Leads and Memberships")
        leads_memberships = df.groupby('campaign')[['sync_acquire_lead', 'sync_acquire_membership']].sum()
        st.bar_chart(leads_memberships)
    else:
        st.info("Please upload an Excel file to view the dashboard.")

if __name__ == "__main__":
    main()
