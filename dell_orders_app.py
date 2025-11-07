import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Dell Orders Tracker",
    page_icon="💻",
    layout="wide"
)

# Title
st.title("💻 Dell Laptop Orders Tracker")
st.markdown("Upload your daily Dell order file to filter and analyze shipments")

# File uploader
uploaded_file = st.file_uploader(
    "Upload Dell Orders File (Excel or CSV)", 
    type=['xlsx', 'xls', 'csv'],
    help="Upload the daily Dell orders file"
)

if uploaded_file is not None:
    try:
        # Read the file
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        st.success(f"✅ File loaded successfully! Total rows: {len(df)}")

        # Filter for Service Tag Quantity = 1 AND Order Date = 10/30/2025
        df_filtered = df[df['Service Tag Quantity'] == 1.0].copy()

        # Parse Order Date and filter for 10/30/2025
        if 'Order Date' in df_filtered.columns:
            df_filtered['Order Date'] = pd.to_datetime(df_filtered['Order Date'], errors='coerce')
            target_date = pd.to_datetime('10/30/2025')
            df_filtered = df_filtered[df_filtered['Order Date'].dt.date == target_date.date()].copy()

            st.info(f"📊 Filtered to {len(df_filtered)} orders with Service Tag Quantity = 1 and Order Date = 10/30/2025")
        else:
            st.info(f"📊 Filtered to {len(df_filtered)} orders with Service Tag Quantity = 1")
        
        if len(df_filtered) > 0:
            # Select only the columns you need
            columns_to_keep = [
                'Ship To Customer',
                'Ship To Contact',
                'Service Tag',
                'Actual Ship Date',
                'Revised Ship Date(RSD)',
                'Estimated Ship Date(ESD)',
                'Status',
                'Sub/Secondary Status',
                'Track Your Order'
            ]
            
            # Create display dataframe with only needed columns
            df_display = df_filtered[columns_to_keep].copy()
            
            # Combine ship dates into one column (prefer Actual > Revised > Estimated)
            df_display['Ship Date'] = df_display.apply(
                lambda row: row['Actual Ship Date'] if pd.notna(row['Actual Ship Date'])
                else (row['Revised Ship Date(RSD)'] if pd.notna(row['Revised Ship Date(RSD)'])
                else row['Estimated Ship Date(ESD)']), axis=1
            )
            
            # Reorder and clean up
            df_final = df_display[[
                'Ship To Customer',
                'Ship To Contact',
                'Service Tag',
                'Ship Date',
                'Status',
                'Sub/Secondary Status',
                'Track Your Order'
            ]].copy()
            
            # Rename for clarity
            df_final.columns = [
                'Customer Name',
                'Contact',
                'Service Tag',
                'Ship Date',
                'Status',
                'Secondary Status',
                'Tracking URL'
            ]
            
            # Show statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Orders", len(df_final))
            with col2:
                status_counts = df_final['Status'].value_counts()
                if len(status_counts) > 0:
                    st.metric("Most Common Status", status_counts.index[0])
            with col3:
                shipped = len(df_final[df_final['Status'] == 'Shipped'])
                st.metric("Shipped Orders", shipped)
            
            # Display the data
            st.subheader("📋 Filtered Orders")
            
            # Add status filter
            status_filter = st.multiselect(
                "Filter by Status (optional)",
                options=df_final['Status'].unique(),
                default=None
            )

            if status_filter:
                df_final = df_final[df_final['Status'].isin(status_filter)]
                st.success(f"✅ Showing {len(df_final)} orders matching selected status filter")

            # Display table
            st.dataframe(
                df_final,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Tracking URL": st.column_config.LinkColumn("Tracking URL")
                }
            )
            
            # Download options
            st.subheader("📥 Download Options")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Excel download
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df_final.to_excel(writer, index=False, sheet_name='Filtered Orders')
                excel_data = output.getvalue()
                
                st.download_button(
                    label="📊 Download as Excel",
                    data=excel_data,
                    file_name=f"dell_orders_filtered_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            
            with col2:
                # CSV download
                csv = df_final.to_csv(index=False)
                st.download_button(
                    label="📄 Download as CSV",
                    data=csv,
                    file_name=f"dell_orders_filtered_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            
            # Print-friendly report
            st.subheader("🖨️ Print-Friendly Report")
            if st.button("Generate Report"):
                st.markdown("---")
                st.markdown(f"### Dell Laptop Orders Report")
                st.markdown(f"**Date:** {datetime.now().strftime('%B %d, %Y')}")
                st.markdown(f"**Total Orders:** {len(df_final)}")
                st.markdown("---")
                
                for idx, row in df_final.iterrows():
                    st.markdown(f"**{row['Customer Name']} - {row['Contact']}**")
                    st.markdown(f"- Service Tag: `{row['Service Tag']}`")
                    st.markdown(f"- Ship Date: {row['Ship Date']}")
                    st.markdown(f"- Status: {row['Status']}")
                    st.markdown(f"- Secondary Status: {row['Secondary Status']}")
                    if pd.notna(row['Tracking URL']):
                        st.markdown(f"- [Track Order]({row['Tracking URL']})")
                    st.markdown("---")
        
        else:
            st.warning("No orders found with Service Tag Quantity = 1")
            
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        st.info("Make sure the file has the expected columns including 'Service Tag Quantity'")

else:
    # Instructions when no file is uploaded
    st.info("👆 Upload your Dell orders file to get started")
    
    with st.expander("ℹ️ How to use this app"):
        st.markdown("""
        1. **Upload** your daily Dell orders Excel file
        2. The app automatically filters for Service Tag Quantity = 1
        3. View the filtered data in a clean table
        4. **Download** as Excel or CSV to update your tracking spreadsheet
        5. **Generate Report** for a print-friendly view
        
        **Columns Displayed:**
        - Customer Name & Contact
        - Service Tag
        - Ship Date (uses Actual → Revised → Estimated in that priority)
        - Status & Secondary Status
        - Tracking URL (clickable)
        """)
