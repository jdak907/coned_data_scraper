import argparse
import pandas as pd

def transform(input_csv: str, output_csv: str | None = None) -> pd.DataFrame:
    """Transform raw ConEd data CSV into a normalized schema."""
    df = pd.read_csv(input_csv)
    cols_to_drop = [
        'Name','Service Address','Town','Zip Code','Seasonal Turn-Off','Next Read Date','Tension Code',
        'Trip Number','Stratum Variable','ICAP','Residential %','LBMP Zone','Recharge New York',
        'Net Metering','Service Class','Previous Account No','Min Month Demand','TOD Code','Profile','Tax','Muni','Bill Amt'
    ]
    df = df.drop(columns=[c for c in cols_to_drop if c in df.columns], errors='ignore')
    df['Utility Code'] = 'CONED'
    df['Usage UOM'] = 'kWh'
    df['Demand UOM'] = 'kW'
    df['Reactive Power UOM'] = 'kVAR'
    df = df.rename(columns={
        'Account':'Utility Account Number','From Date':'Start Date','To Date':'End Date',
        'Use':'Usage','Reading':'Reading Type','KVARS':'Reactive Power'
    })
    desired = ['Utility Code','Utility Account Number','Start Date','End Date','Usage','Usage UOM',
               'Demand','Demand UOM','Reactive Power','Reactive Power UOM','Reading Type']
    cols = [c for c in desired if c in df.columns] + [c for c in df.columns if c not in desired]
    df = df[cols]
    if output_csv:
        df.to_csv(output_csv, index=False)
    return df

def main():
    parser = argparse.ArgumentParser(description="Normalize ConEd CSV -> clean CSV.")
    parser.add_argument("--input", required=True, help="Path to input CSV")
    parser.add_argument("--output", help="Optional output CSV path")
    args = parser.parse_args()
    df = transform(args.input, args.output)
    if not args.output:
        print(df.to_string(index=False))

if __name__ == "__main__":
    main()
