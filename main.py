import streamlit as st
import pandas as pd
import io
from data_processor import DataProcessor


def main():
    st.set_page_config(page_title="CONTINUUM INTELLIGENCE",
                       page_icon="🚀",
                       layout="wide")

    st.title("🚀 CoCo Intellgence")
    st.write("Upload your CSV file, view the data, and process it with ease!")

    # File upload section
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        try:
            # Load the data
            df = pd.read_csv(uploaded_file)

            # Display original data
            st.subheader("📄 Original Data Preview")
            st.dataframe(df.head())

            # Display basic information
            st.subheader("ℹ️ Basic Information")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Rows", df.shape[0])
            with col2:
                st.metric("Columns", df.shape[1])
            with col3:
                st.metric("Missing Values", df.isnull().sum().sum())

            # Process data button
            if st.button("🔄 Process Data"):
                with st.spinner("Processing data..."):
                    # Process the data
                    processed_df, stats = DataProcessor.process_csv(df)

                    # Display processed data
                    st.subheader("✨ Processed Data Preview")
                    st.dataframe(processed_df.head())

                    # Display statistics
                    st.subheader("📈 Processing Statistics")
                    st.json(stats)

                    # Create download button for processed data
                    csv = processed_df.to_csv(index=False)
                    st.download_button(label="📥 Download Processed CSV",
                                       data=csv,
                                       file_name="processed_data.csv",
                                       mime="text/csv")

                st.success("✅ Processing completed successfully!")

        except Exception as e:
            st.error(f"❌ Error processing file: {str(e)}")

    else:
        # Show placeholder when no file is uploaded
        st.info("👆 Please upload a CSV file to begin")

        # Example of expected format
        st.subheader("📝 Expected CSV Format")
        example_df = pd.DataFrame({
            'Name': ['John', 'Jane', 'Bob'],
            'Age': [25, 30, 35],
            'City': ['New York', 'London', 'Paris']
        })
        st.dataframe(example_df)


if __name__ == "__main__":
    main()
