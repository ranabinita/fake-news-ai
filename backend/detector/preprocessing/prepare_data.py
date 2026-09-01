import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_DIR = BASE_DIR/"datasets"
FAKE_FILE = DATASET_DIR/"Fake.csv"
TRUE_FILE=DATASET_DIR/"True.csv"
OUTPUT_FILE = DATASET_DIR/"cleaned_news.csv"

fake=pd.read_csv(FAKE_FILE)
true=pd.read_csv(TRUE_FILE)

print(f"original fake articles: {len(fake)}")
print(f"original true articles: {len(true)}")

fake["label"]=0
true["label"]=1
fake["text"]=fake["text"].fillna("").str.strip()
true["text"]=true["text"].fillna("").str.strip()
fake=fake[fake["text"].str.len()>10]
true=true[true["text"].str.len()>10]

fake["content"]=fake["title"].fillna("").str.strip()+" "+fake["text"].fillna("")
true["content"]=true['title'].fillna('').str.strip()+" "+true["text"].fillna("")

fake=fake[["title","text","content","label"]]
true=true[["title","text","content","label"]]
df=pd.concat([fake,true],ignore_index=True)

print(f"combined articles: {len(df)}")
before_duplicates=len(df)
df=df.drop_duplicates(subset=["content"])
print(f"removed duplicates:{before_duplicates-len(df)}")
# before_short=len(df)
# df["content"]=df["content"].str.strip()
# df=df[df["content"].str.strip().str.len()>10]
# print(f"Removed short articales: {before_short-len(df)}")
df=df.sample(frac=1,random_state=42).reset_index(drop=True)
df.to_csv(OUTPUT_FILE,index=False)
print(f"final dataset:{len(df)}")
print(f"saved to: {OUTPUT_FILE}")
print("\nClass distribution:")
print(df["label"].value_counts())