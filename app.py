from flask import Flask,render_template, request
import os
from image_processing import process_image

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/upload", methods=["GET", "POST"])
def upload():

    if request.method == "POST":

        file = request.files["signature"]

        if file:

            filepath = os.path.join(
                app.config["UPLOAD_FOLDER"],
                file.filename
            )

            result = process_image(file, filepath)
            if result is None:
                return "Unable to process image", 400

            return render_template(
               "output.html",
               pngFile=result["pngFile"],
               svgFile=result["svgFile"],
               width=result["width"],
               height=result["height"],
               pngSize=result["pngSize"],
               svgSize=result["svgSize"])



    return render_template("upload.html")

@app.route("/connect")
def connect():
    return render_template('connect.html')

@app.route("/compare")
def compare():
    return render_template('compare.html')



if __name__ == "__main__":
    app.run(debug=True)
