from flask import Flask, render_template, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

# Load Excel registry
EXCEL_FILE = os.path.join(os.path.dirname(__file__), "household_list.xlsx")

def load_household_data():
    """Read the Excel file fresh each time to get latest entries."""
    df = pd.read_excel(EXCEL_FILE)
    # Normalize column names to lowercase and remove spaces
    df.columns = [c.strip().lower() for c in df.columns]
    return df

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    query = request.args.get("q", "").strip().lower()
    if len(query) < 2:
        return jsonify([])

    df = load_household_data()  # load fresh every request
    # filter household_head containing query
    results = df[df["household_head"].str.lower().str.contains(query, na=False)]

    return jsonify(
        results[["household_head", "household_id", "village"]]
        .head(10)
        .to_dict(orient="records")
    )

if __name__ == "__main__":
    app.run(debug=True)
