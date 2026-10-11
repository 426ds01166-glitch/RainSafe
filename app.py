from flask import Flask, render_template, request

app = Flask(__name__)


# ==============================
# HASH TABLE
# ==============================

class HashTable:

    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(size)]

    def hash_function(self, key):
        return sum(ord(char) for char in key) % self.size

    def insert(self, key, value):
        index = self.hash_function(key)

        for item in self.table[index]:
            if item[0] == key:
                item[1] = value
                return

        self.table[index].append([key, value])

    def search(self, key):
        index = self.hash_function(key)

        for item in self.table[index]:
            if item[0] == key:
                return item[1]

        return None

    def delete(self, key):
        index = self.hash_function(key)

        for item in self.table[index]:
            if item[0] == key:
                self.table[index].remove(item)
                return True

        return False

    def get_all(self):
        records = []

        for bucket in self.table:
            for key, value in bucket:
                records.append((key, value))

        return records


# Create Hash Table
roads = HashTable(10)


# ==============================
# SAMPLE ROAD DATA
# ==============================

roads.insert("R101", {
    "road_name": "OMR Main Road",
    "status": "Safe",
    "severity": "Low",
    "description": "Road condition is normal"
})

roads.insert("R102", {
    "road_name": "Velachery Main Road",
    "status": "Waterlogging",
    "severity": "High",
    "description": "Heavy waterlogging reported"
})

roads.insert("R103", {
    "road_name": "Tambaram Main Road",
    "status": "Heavy Traffic",
    "severity": "Medium",
    "description": "Traffic is moving slowly"
})


# ==============================
# HOME PAGE
# ==============================

@app.route("/")
def home():
    return render_template("index.html")


# ==============================
# ADD ROAD ALERT
# ==============================

@app.route("/add", methods=["POST"])
def add_alert():

    road_id = request.form["road_id"].upper().strip()

    road_data = {
        "road_name": request.form["road_name"],
        "status": request.form["status"],
        "severity": request.form["severity"],
        "description": request.form["description"]
    }

    roads.insert(road_id, road_data)

    return f"""
    <h2>✅ Road Alert Added Successfully!</h2>
    <p>Road ID: {road_id}</p>
    <a href="/">Go Back</a>
    """


# ==============================
# SEARCH ROAD
# ==============================

@app.route("/search", methods=["POST"])
def search_road():

    road_id = request.form["search_id"].upper().strip()

    result = roads.search(road_id)

    if result:
        return f"""
        <h2>🔍 Road Found</h2>

        <p><b>Road ID:</b> {road_id}</p>
        <p><b>Road Name:</b> {result['road_name']}</p>
        <p><b>Status:</b> {result['status']}</p>
        <p><b>Severity:</b> {result['severity']}</p>
        <p><b>Description:</b> {result['description']}</p>

        <br>

        <a href="/">⬅ Back to Home</a>
        """

    return f"""
    <h2>❌ Road ID Not Found</h2>

    <p>No road alert found for <b>{road_id}</b>.</p>

    <br>

    <a href="/">⬅ Back to Home</a>
    """

# ==============================
# VIEW ALL ALERTS
# ==============================

@app.route("/alerts")
def alerts():

    records = roads.get_all()

    html = """
    <html>
    <head>
        <title>RainSafe Alerts</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>

    <body>

    <div class="container">

    <h2>🛣️ Current Road Alerts</h2>
    """

    for road_id, data in records:

        html += f"""
        <div class="alert-card">
            <h3>🚧 {road_id} - {data['road_name']}</h3>

            <p><b>Status:</b> {data['status']}</p>
            <p><b>Severity:</b> {data['severity']}</p>
            <p><b>Description:</b> {data['description']}</p>
        </div>
        """

    html += """
        <a href="/">Go Back</a>

        </div>

        </body>
        </html>
    """

    return html


# ==============================
# RUN APPLICATION
# ==============================

if __name__ == "__main__":
    app.run(debug=True)