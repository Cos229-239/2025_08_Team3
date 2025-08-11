import re, json, ast, pandas as pd
from flask import Flask, request, jsonify, render_template
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import os, pathlib

app = Flask(__name__, template_folder="templates", static_folder="static")

df = pd.read_csv("data/recipes.csv") 

def norm(s: str) -> str:

    s = "" if pd.isna(s) else str(s).lower()
    s = re.sub(r"[^a-z0-9, /+\-]", " ", s).replace("/", " ")
    return " ".join(t for t in re.split(r"[, \s]+", s) if t)

df["ing_norm"] = df["ingredients"].astype(str).apply(norm)

vec = TfidfVectorizer(ngram_range=(1,2), min_df=1)
X = vec.fit_transform(df["ing_norm"])

knn = NearestNeighbors(metric="cosine", algorithm="brute")

knn.fit(X)

def _instructions_to_text(x):

    try:
        if isinstance(x, str) and x.strip().startswith("["):
            lst = ast.literal_eval(x)
            if isinstance(lst, list):
                return " ".join(map(str, lst))
        return str(x)
    except Exception:
        return str(x)

def find_recipes(ingredients: str, k: int = 12, require_all: bool = False):

    q = norm(ingredients)
    if not q:
        return []
    
    q_vec = vec.transform([q])
    dists, idxs = knn.kneighbors(q_vec, n_neighbors=min(k*5, X.shape[0]))
    out = df.iloc[idxs[0]].copy()
    out["score"] = (1 - dists[0])  

    if require_all:

        toks = set(q.split())
        out = out[out["ing_norm"].apply(lambda s: toks.issubset(set(s.split())))]

    keep = ["title", "image", "total time", "ingredients", "instructions", "description", "score"]
    out = out[keep].head(k).copy()
    out["instructions"] = out["instructions"].apply(_instructions_to_text)
    return out.to_dict(orient="records")

@app.get("/")
def home():
    return render_template("index.html")

@app.get("/search")
def search():

    q = request.args.get("ingredient", "")
    require_all = request.args.get("require_all", "false").lower() == "true"
    k = int(request.args.get("k", 12))
    results = find_recipes(q, k=k, require_all=require_all)
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
