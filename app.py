from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load Excel data
data = pd.read_excel("household_list.xlsx")
data['household_head'] = data['household_head'].astype(str)
data['village'] = data['village'].astype(str)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    q = request.args.get("q", "")
    matches = data[data['household_head']
                   .str.contains(q, case=False, na=False)].head(10)
    return jsonify(matches['household_head'].tolist())

@app.route("/details")
def details():
    name = request.args.get("name", "")
    match = data[data['household_head'].str.lower() == name.lower()]

    if not match.empty:
        row = match.iloc[0]
        return jsonify({
            "household_head": row['household_head'],
            "household_id": row['household_ID'],
            "village": row['village']
        })
    return jsonify({"error": "Not found"})

if __name__ == "__main__":
    app.run(debug=True)
