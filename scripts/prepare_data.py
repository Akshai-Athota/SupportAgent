from datasets import load_dataset
import pandas as pd
import re
from pathlib import Path
from app.config import CSV_PATH



ds = load_dataset("bitext/Bitext-customer-support-llm-chatbot-training-dataset")

df = ds["train"].to_pandas()


df = df.drop_duplicates(subset=["instruction"]).reset_index(drop=True)



def clean_placeholders(text):
    text = re.sub(r"\{\{\s*order\s*num\s*\}\}", "the user's order number", text, flags=re.I)
    text = re.sub(r"\{\{\s*order\s*number\s*\}\}", "the user's order number", text, flags=re.I)
    text = re.sub(r"\{\{\s*email\s*\}\}", "the user's email address", text, flags=re.I)
    text = re.sub(r"\{\{\s*online\s*company\s*portal\s*info\s*\}\}", "the company portal", text, flags=re.I)
    text = re.sub(r"\{\{\s*online\s*order\s*interaction\s*\}\}", "orders section", text, flags=re.I)

    text = re.sub(r"\{\{\s*(.*?)\s*\}\}", r"the required \1", text)
    return text


df["instruction"] = df["instruction"].apply(clean_placeholders)
df["response"] = df["response"].apply(clean_placeholders)

df_sampled = (df.groupby(["category", "intent"], group_keys=False).sample(frac=0.5, random_state=42).reset_index(drop=True))


df_sampled.to_csv(CSV_PATH, index=False)

