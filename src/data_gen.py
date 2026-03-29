import pandas as pd
from sklearn.datasets import load_wine
import os
import sys

def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ['v1', 'v2']:
        print("Usage: python data_gen.py [v1|v2]")
        return
    
    os.makedirs('data', exist_ok=True)
    data = load_wine()
    df = pd.DataFrame(data.data, columns=data.feature_names)
    df['target'] = data.target

    if sys.argv[1] == 'v1':
        # V1 mapping - partial data (first 100 rows)
        df = df.iloc[:100]
    
    df.to_csv('data/dataset.csv', index=False)
    print(f"Generated {sys.argv[1]} dataset.csv (Wine Quality)")

if __name__ == "__main__":
    main()
