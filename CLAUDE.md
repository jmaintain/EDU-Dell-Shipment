# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Dell Laptop Orders Tracker - A Streamlit web application for filtering and tracking Dell laptop orders. The application filters Dell order files for orders with Service Tag Quantity = 1 and presents them in a clean, exportable format.

## Architecture

This is a simple Python application with two main components:

1. **dell_orders_app.py** - Streamlit web interface for interactive filtering and downloading
2. **dell_orders_cli.py** - Command-line tool for batch processing and terminal-based reports

Both share the same core logic: filter Dell orders by Service Tag Quantity = 1, combine ship dates (preferring Actual > Revised > Estimated), and present selected columns in a clean format.

## Development Commands

### Running the Application

**Web Interface:**
```bash
streamlit run dell_orders_app.py
```
The app runs on http://localhost:8501 by default.

**Command Line:**
```bash
python dell_orders_cli.py <input_file.xlsx>
python dell_orders_cli.py <input_file.xlsx> -o filtered_output.xlsx
python dell_orders_cli.py <input_file.xlsx> -o output.csv
```

### Environment Setup

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Unix/MacOS)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Data Processing Logic

### Expected Input Format

Dell order files (Excel or CSV) must contain these columns:
- Service Tag Quantity (filtering column)
- Ship To Customer
- Ship To Contact
- Service Tag
- Actual Ship Date
- Revised Ship Date(RSD)
- Estimated Ship Date(ESD)
- Status
- Sub/Secondary Status
- Track Your Order

### Ship Date Priority Logic

The application combines three date fields into one "Ship Date" using this priority:
1. Actual Ship Date (if present)
2. Revised Ship Date(RSD) (if Actual not present)
3. Estimated Ship Date(ESD) (if neither Actual nor Revised present)

This logic is implemented identically in both [dell_orders_app.py:57-61](dell_orders_app.py#L57-L61) and [dell_orders_cli.py:49-53](dell_orders_cli.py#L49-L53).

### Output Format

Filtered data is presented with these columns:
- Customer Name (from Ship To Customer)
- Contact (from Ship To Contact)
- Service Tag
- Ship Date (combined as described above)
- Status
- Secondary Status (from Sub/Secondary Status)
- Tracking URL (from Track Your Order, rendered as clickable link in web UI)

## Key Implementation Details

### Streamlit App Features

- File upload supporting Excel (.xlsx, .xls) and CSV
- Real-time filtering and statistics display
- Multi-select status filter
- Download options (Excel and CSV with timestamped filenames)
- Print-friendly report generation
- Clickable tracking URLs via `st.column_config.LinkColumn`

### CLI Tool Features

- Supports both Excel and CSV input/output
- Prints formatted report to terminal
- Status breakdown summary
- Optional file output with `-o` flag

## Deployment

The README documents deployment to Streamlit Cloud, Heroku, Railway, or custom server. For Streamlit Cloud deployment:
1. Push to GitHub
2. Connect at https://share.streamlit.io
3. Deploy (no additional configuration needed)

## Important Notes

- All data processing happens in memory; no persistent storage
- The application expects exact column names as specified above
- Date handling uses pandas' built-in date parsing
- Both tools handle missing values (NaN) appropriately in date combination logic
