import pandas as pd
import sys

src = sys.argv[1]
dest = sys.argv[2]

df = pd.read_csv(src, sep='\t')

df = df.drop(axis=1, labels="P")

df.to_json(dest, orient="records", lines=True)
