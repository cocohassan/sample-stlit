import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from data_processor import DataProcessor

def main():
    st.set_page_config(page_title="COIQ",
                       page_icon="🚀",
                       layout="wide")

    # Custom CSS for logo positioning
    st.markdown("""
        <style>
        .logo-container {
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 999;
        }
        .logo-image {
            width: 40px;
            height: auto;
        }
        </style>
    """, unsafe_allow_html=True)

    # Add logo in top right corner
    st.markdown("""
        <div class="logo-container">
            <img src="attached_assets/c-star@1500x%20white.png" class="logo-image">
        </div>
    """, unsafe_allow_html=True)

    # Simple header with just COIQ
    st.markdown("<h1 style='text-align: center;'>C O I Q</h1>", unsafe_allow_html=True)

    # Create three columns for the top section
    upload_col, process_col, stats_col = st.columns([1, 1, 1])

    # File Upload Section (Left)
    with upload_col:
        st.subheader("📤 Upload Data")
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    # Stats Summary Section (Right)
    with stats_col:
        st.subheader("📊 Key Stats")
        if 'processed_data' in st.session_state:
            df = st.session_state.processed_data
            st.metric("Total Startups", len(df))
            if 'Final Label' in df.columns:
                rocket_counts = df['Final Label'].value_counts()
                st.write("Rocket Type Distribution:")
                for rocket_type, count in rocket_counts.items():
                    st.metric(f"Type {rocket_type}", count)
        else:
            st.info("Upload and process data to view statistics")

    # Process Button (Center)
    with process_col:
        st.subheader("🚀 Process Data")
        if uploaded_file is not None:
            if st.button("Run AI Processing", use_container_width=True):
                with st.spinner("🤖 AI Processing in progress..."):
                    # Load and process the data
                    df = pd.read_csv(uploaded_file)
                    processed_df, stats = DataProcessor.process_csv(df)

                    # Store in session state
                    st.session_state.processed_data = processed_df
                    st.session_state.stats = stats

                    st.success("✅ Processing completed!")

    # Define color scheme for rocket types
    color_scheme = {
        'W': '#8db3da',  # Soft blue
        'X': '#f4b183',  # Soft orange
        'Y': '#a8d5a7',  # Soft green
        'Z': '#f8a0a0'   # Soft red
    }

    # Visualization Section (Middle)
    if 'processed_data' in st.session_state:
        st.subheader("📈 Data Visualization")
        viz_col1, viz_col2 = st.columns([2, 1])

        with viz_col1:
            if 'Final Label' in st.session_state.processed_data.columns:
                # Create bar chart with consistent colors
                df_counts = st.session_state.processed_data['Final Label'].value_counts().reset_index()
                df_counts.columns = ['Rocket Type', 'Count']

                fig = px.bar(
                    df_counts,
                    x='Rocket Type',
                    y='Count',
                    title="Rocket Type Distribution",
                    color='Rocket Type',
                    color_discrete_map=color_scheme
                )
                st.plotly_chart(fig, use_container_width=True)

        with viz_col2:
            if 'Final Label' in st.session_state.processed_data.columns:
                # Create pie chart with the same color scheme
                fig = px.pie(
                    values=st.session_state.processed_data['Final Label'].value_counts(),
                    names=st.session_state.processed_data['Final Label'].value_counts().index,
                    title="Rocket Type Breakdown",
                    color=st.session_state.processed_data['Final Label'].value_counts().index,
                    color_discrete_map=color_scheme
                )
                st.plotly_chart(fig, use_container_width=True)

        # Labeled Dataset View (Bottom)
        st.subheader("🔍 Detailed Results")
        with st.expander("View Processed Dataset", expanded=False):
            st.dataframe(st.session_state.processed_data, use_container_width=True)

            # Download button for processed data
            csv = st.session_state.processed_data.to_csv(index=False)
            st.download_button(
                label="📥 Download Processed CSV",
                data=csv,
                file_name="processed_startups.csv",
                mime="text/csv",
                use_container_width=True
            )

    else:
        # Show placeholder when no file is uploaded
        st.info("👆 Please upload a CSV file to begin")

if __name__ == "__main__":
    main()