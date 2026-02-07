"""
Project: Automation for Audit Reconciliation
Author: Hitesh Silwal (Junior @ University of Idaho)
Major: Business Information & Analytics |
"""

import pandas as pd
import matplotlib.pyplot as plt

# --- PART 1: MOCK DATA GENERATION ---
def make_test_files():
    """Generates synthetic CSV files to simulate an audit environment."""
    ledger_data = {
        'Ref_ID': ['TXN101', 'TXN102', 'TXN103', 'TXN104', 'TXN105'],
        'Date': ['2026-02-01', '2026-02-03', '2026-02-05', '2026-02-06', '2026-02-07'],
        'Amount': [500.00, 125.50, 1000.00, 250.00, 75.00]
    }
    
    bank_data = {
        'Ref_ID': ['TXN101', 'TXN102', 'TXN103'],
        'Date': ['2026-02-01', '2026-02-03', '2026-02-05'],
        'Amount': [500.00, 125.50, 1000.00]
    }
    
    pd.DataFrame(ledger_data).to_csv('my_ledger.csv', index=False)
    pd.DataFrame(bank_data).to_csv('my_bank.csv', index=False)
    print("✓ Success: 'my_ledger.csv' and 'my_bank.csv' created.")

# --- PART 2 & 3: AUDIT LOGIC & VISUALIZATION ---
def run_audit():
    """Reconciles data and visualizes financial risk."""
    df_ledger = pd.read_csv('my_ledger.csv')
    df_bank = pd.read_csv('my_bank.csv')

    # Merging records to find what is missing from the bank
    check_match = pd.merge(df_ledger, df_bank, on=['Ref_ID', 'Amount'], how='left', indicator=True)
    errors = check_match[check_match['_merge'] == 'left_only']

    if not errors.empty:
        print("\n!!! ALERT: DISCREPANCIES FOUND !!!")
        print(errors[['Ref_ID', 'Amount', 'Date_x']])
        
        # Save results for portfolio proof
        errors.to_csv('audit_red_flags.csv', index=False)
        
        # VISUALIZATION (U-Idaho Gold: #F1B82D)
        plt.figure(figsize=(8, 5))
        plt.bar(errors['Ref_ID'], errors['Amount'], color='#F1B82D', edgecolor='#A5A9AC', linewidth=2)
        plt.title('Audit Exceptions: Financial Risk Summary', fontsize=14, fontweight='bold')
        plt.xlabel('Transaction ID')
        plt.ylabel('Risk Amount ($)')
        plt.savefig('vandal_audit_chart.png')
        print("\n✓ Chart saved as 'vandal_audit_chart.png'")
        plt.show()
    else:
        print("✓ Success: All records match.")

# Execution Block
if __name__ == "__main__":
    make_test_files()
    run_audit()
