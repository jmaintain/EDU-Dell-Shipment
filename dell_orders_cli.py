#!/usr/bin/env python3
"""
Dell Orders Tracker - Command Line Version
Simple script to filter Dell order files and generate reports
"""

import pandas as pd
import sys
from datetime import datetime
import argparse

def process_dell_orders(input_file, output_file=None):
    """Process Dell orders file and filter for Service Tag Quantity = 1"""
    
    print(f"📂 Reading file: {input_file}")
    
    # Read file
    if input_file.endswith('.csv'):
        df = pd.read_csv(input_file)
    else:
        df = pd.read_excel(input_file)
    
    print(f"✅ Loaded {len(df)} total rows")

    # Filter for Service Tag Quantity = 1
    df_filtered = df[df['Service Tag Quantity'] == 1.0].copy()

    # Parse Order Date and filter for 10/30/2025
    if 'Order Date' in df_filtered.columns:
        df_filtered['Order Date'] = pd.to_datetime(df_filtered['Order Date'], errors='coerce')
        target_date = pd.to_datetime('10/30/2025')
        df_filtered = df_filtered[df_filtered['Order Date'].dt.date == target_date.date()].copy()
        print(f"🔍 Filtered to {len(df_filtered)} orders with Service Tag Quantity = 1 and Order Date = 10/30/2025")
    else:
        print(f"🔍 Filtered to {len(df_filtered)} orders with Service Tag Quantity = 1")
    
    if len(df_filtered) == 0:
        print("⚠️  No orders found with Service Tag Quantity = 1")
        return
    
    # Select relevant columns
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
    
    df_display = df_filtered[columns_to_keep].copy()
    
    # Combine ship dates (prefer Actual > Revised > Estimated)
    df_display['Ship Date'] = df_display.apply(
        lambda row: row['Actual Ship Date'] if pd.notna(row['Actual Ship Date'])
        else (row['Revised Ship Date(RSD)'] if pd.notna(row['Revised Ship Date(RSD)'])
        else row['Estimated Ship Date(ESD)']), axis=1
    )
    
    # Create final dataframe
    df_final = df_display[[
        'Ship To Customer',
        'Ship To Contact',
        'Service Tag',
        'Ship Date',
        'Status',
        'Sub/Secondary Status',
        'Track Your Order'
    ]].copy()
    
    df_final.columns = [
        'Customer Name',
        'Contact',
        'Service Tag',
        'Ship Date',
        'Status',
        'Secondary Status',
        'Tracking URL'
    ]
    
    # Print summary
    print("\n" + "="*80)
    print(f"📊 DELL ORDERS SUMMARY - {datetime.now().strftime('%B %d, %Y')}")
    print("="*80)
    print(f"\nTotal Orders: {len(df_final)}")
    print("\nStatus Breakdown:")
    for status, count in df_final['Status'].value_counts().items():
        print(f"  • {status}: {count}")
    
    # Print detailed report
    print("\n" + "="*80)
    print("📋 DETAILED ORDERS")
    print("="*80 + "\n")
    
    for idx, row in df_final.iterrows():
        print(f"Customer: {row['Customer Name']}")
        print(f"Contact: {row['Contact']}")
        print(f"Service Tag: {row['Service Tag']}")
        print(f"Ship Date: {row['Ship Date']}")
        print(f"Status: {row['Status']}")
        print(f"Secondary Status: {row['Secondary Status']}")
        if pd.notna(row['Tracking URL']):
            print(f"Tracking: {row['Tracking URL']}")
        print("-" * 80)
    
    # Save to file if requested
    if output_file:
        if output_file.endswith('.csv'):
            df_final.to_csv(output_file, index=False)
            print(f"\n💾 Saved to CSV: {output_file}")
        else:
            df_final.to_excel(output_file, index=False, sheet_name='Filtered Orders')
            print(f"\n💾 Saved to Excel: {output_file}")
    
    return df_final


def main():
    parser = argparse.ArgumentParser(
        description='Filter Dell order files for Service Tag Quantity = 1',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python dell_orders_cli.py orders.xlsx
  python dell_orders_cli.py orders.xlsx -o filtered_orders.xlsx
  python dell_orders_cli.py orders.xlsx -o output.csv
        """
    )
    
    parser.add_argument('input_file', help='Input Dell orders file (Excel or CSV)')
    parser.add_argument('-o', '--output', help='Output file (Excel or CSV)', default=None)
    
    args = parser.parse_args()
    
    try:
        process_dell_orders(args.input_file, args.output)
    except FileNotFoundError:
        print(f"❌ Error: File not found: {args.input_file}")
        sys.exit(1)
    except KeyError as e:
        print(f"❌ Error: Missing required column in file: {e}")
        print("Make sure your file has the 'Service Tag Quantity' column")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error processing file: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Dell Orders Tracker - Command Line Tool")
        print("\nUsage: python dell_orders_cli.py <input_file> [-o <output_file>]")
        print("\nExamples:")
        print("  python dell_orders_cli.py orders.xlsx")
        print("  python dell_orders_cli.py orders.xlsx -o filtered.xlsx")
        print("  python dell_orders_cli.py orders.xlsx -o output.csv")
        print("\nFor more help: python dell_orders_cli.py --help")
        sys.exit(0)
    
    main()
