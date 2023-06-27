from flask import Flask, render_template, request, send_from_directory

app = Flask(
        "WiFiSetupApp",
        static_url_path="/static",
        static_folder="static",
        template_folder="templates"
)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        ssid = request.form.get("ssid")
        password = request.form.get("password")
        print(ssid, password)
        return render_template("index.html")

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
