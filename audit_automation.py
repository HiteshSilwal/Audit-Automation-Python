"""
Project: Automation for Audit Reconciliation
Author: Hitesh Silwal (Junior @ University of Idaho)
Description: This is a project I am building to show how my BIA major 
can help automate manual accounting tasks like bank recs.
"""

import pandas as pd

# PART 1: MOCK DATA GENERATION
# Since I don't have real company data yet, I am making these CSVs 
# to test if my logic for finding "Red Flags" actually works.

def make_test_files():
    # What the company thinks happened (Internal Ledger)
    ledger_data = {
        'Ref_ID': ['TXN101', 'TXN102', 'TXN103', 'TXN104'],
        'Date': ['2026-02-01', '2026-02-03', '2026-02-05', '2026-02-06'],
        'Amount': [500.00, 125.50, 1000.00, 250.00]
    }
    
    # What actually hit the bank (Bank Statement)
    # Note: I'm leaving out TXN104 to see if the script catches it
    bank_data = {
        'Ref_ID': ['TXN101', 'TXN102', 'TXN103'],
        'Date': ['2026-02-01', '2026-02-03', '2026-02-05'],
        'Amount': [500.00, 125.50, 1000.00]
    }
    
    pd.DataFrame(ledger_data).to_csv('my_ledger.csv', index=False)
    pd.DataFrame(bank_data).to_csv('my_bank.csv', index=False)
    print("Files 'my_ledger.csv' and 'my_bank.csv' created for testing.")

# PART 2: THE AUDIT LOGIC
def run_audit():
    # Loading the data using Pandas (Learning this in BIA classes)
    df_ledger = pd.read_csv('my_ledger.csv')
    df_bank = pd.read_csv('my_bank.csv')

    print("\n--- Running Reconciliation ---")

    # Using a 'left merge' to find things in my books that aren't in the bank
    # This is like a VLOOKUP but much faster for big data
    check_match = pd.merge(df_ledger, df_bank, on=['Ref_ID', 'Amount'], how='left', indicator=True)

    # If the indicator says 'left_only', it means the bank is missing that transaction
    errors = check_match[check_match['_merge'] == 'left_only']

    if not errors.empty:
        print("!!! ALERT: DISCREPANCIES FOUND !!!")
        # Just showing the important columns for the auditor to see
        print(errors[['Ref_ID', 'Amount', 'Date_x']])
        
        # Saving these so I can show them to a professor or manager
        errors.to_csv('audit_red_flags.csv', index=False)
        print("\nReport saved as 'audit_red_flags.csv'")
    else:
        print("Everything matches! No issues found.")

# Running the script
if __name__ == "__main__":
    make_test_files()
    run_audit()
    
# TODO for future: 
# 1. Add Benford's Law analysis (once I finish BIA 4610)
# 2. Try to connect this directly to an SQL database (after BIA 4530)

