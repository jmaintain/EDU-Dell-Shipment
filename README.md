# Dell Laptop Orders Tracker 💻

A simple Streamlit web app to filter and track Dell laptop orders for your staff.

## Features

✅ Upload daily Dell order files (Excel/CSV)
✅ Automatically filters for Service Tag Quantity = 1
✅ Displays only relevant columns: Customer, Contact, Service Tag, Ship Date, Status, Tracking URL
✅ Download filtered data as Excel or CSV
✅ Print-friendly report generation
✅ Status filtering
✅ Clean, simple interface

## Quick Start with AI Coding Tools

### Option 1: Claude Code (Recommended)

1. Open your terminal
2. Install Claude Code if you haven't: `brew install anthropics/claude/claude`
3. Navigate to where you want the project
4. Run: `claude code "Create the Dell Orders Tracker app"`
5. When prompted, paste the contents of `dell_orders_app.py`
6. Run the app: `streamlit run dell_orders_app.py`

### Option 2: Cursor

1. Open Cursor
2. Create a new folder for your project
3. Copy `dell_orders_app.py` and `requirements.txt` into the folder
4. Open terminal in Cursor
5. Run: `pip install -r requirements.txt`
6. Run: `streamlit run dell_orders_app.py`
7. Your browser will open to http://localhost:8501

### Option 3: Replit

1. Go to https://replit.com
2. Click "Create Repl"
3. Choose "Python" template
4. Name it "Dell Orders Tracker"
5. Copy the contents of `dell_orders_app.py` into `main.py`
6. Add to `.replit` configuration file:
   ```
   run = "streamlit run main.py --server.port 5000 --server.address 0.0.0.0"
   ```
7. Install packages in Shell: `pip install streamlit pandas openpyxl`
8. Click "Run"

## Local Setup (Manual)

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run dell_orders_app.py
```

The app will open in your browser at http://localhost:8501

## How to Use

1. **Upload File**: Click "Browse files" and select your daily Dell orders Excel file
2. **View Filtered Data**: The app automatically shows only orders with Service Tag Quantity = 1
3. **Filter by Status**: (Optional) Use the dropdown to filter specific statuses
4. **Download**: Click "Download as Excel" or "Download as CSV" to save the filtered data
5. **Generate Report**: Click to create a print-friendly version
6. **Copy Data**: Use the filtered output to update your third-party tracking spreadsheet

## Deployment Options

### Streamlit Cloud (Free & Easy)

1. Push your code to GitHub
2. Go to https://share.streamlit.io
3. Connect your GitHub repository
4. Deploy!
5. You'll get a URL like: `https://your-app.streamlit.app`

### Other Options

- **Heroku**: Easy deployment with free tier
- **Railway**: Simple deployment with generous free tier
- **Your own server**: Run with `streamlit run dell_orders_app.py --server.port 80`

## Data Privacy

- All processing happens in your browser/server
- No data is stored or sent to third parties
- Uploaded files are processed in memory and discarded

## Troubleshooting

**App won't start:**
- Make sure you have Python 3.8+
- Install requirements: `pip install -r requirements.txt`

**File upload error:**
- Ensure your file has the column "Service Tag Quantity"
- Check file format (Excel .xlsx or CSV)

**No data showing:**
- Verify there are rows with Service Tag Quantity = 1 in your file

## Customization

Want to change which columns are displayed? Edit this section in `dell_orders_app.py`:

```python
columns_to_keep = [
    'Ship To Customer',
    'Ship To Contact',
    'Service Tag',
    # Add or remove columns here
]
```

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify your Excel file has the expected format
3. Make sure Service Tag Quantity column exists

---

**Built with Streamlit** | **AI-Powered Development Ready** 🚀
