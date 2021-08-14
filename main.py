from colorthief import ColorThief
from flask import Flask, render_template, redirect, url_for, flash, request
from wtforms import StringField, SubmitField, SelectField, FileField, IntegerField
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms.validators import *
import datetime
from werkzeug.utils import secure_filename
import os
# Choices for the selector field. Values and keys are mismatched to account for a bug in the "color_count" argument in
# colorthief.get_palette
CHOICES = [(2, 3), (4, 4), (5, 5), (6, 6), (7, 7), (9, 8), (10, 9), (11, 10)]
dog_hex = ['#765245', '#d5a48d', '#2b2b2a', '#b8a7a0', '#ae989e']  # hex values for default dog photo
app = Flask(__name__)
app.config["SECRET_KEY"] = "pmlgxrrmj54wbuqw"
# setting up the upload folder
UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

Bootstrap(app)

# Form for choosing photo and the amount of colors in the palette
class PhotoForm(FlaskForm):
    photo = FileField("Choose a photo:", validators=[DataRequired()])
    colors = SelectField("Number of colors:", choices=CHOICES, validators=[DataRequired()])
    run = SubmitField("Run")

#check if file type is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#  Makes the "current_year" variable available in every template#
@app.context_processor
def inject_now():
    return {'current_year': datetime.date.today().strftime("%Y")}


@app.route("/", methods=["GET", "POST"])
def home():
    form = PhotoForm()
    if form.validate_on_submit():
        # get the uploaded file, create a secure filename, and save file to the upload directory
        file = request.files["photo"]
        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            path = f"static/images/{filename}"
            # create a colorthief object from the uploaded file and get the color palette in RGB
            im = ColorThief(path)
            rgb_list = im.get_palette(color_count=int(form.colors.data))
            # Convert RGB color palette to HEX
            hex_list = ["#"+"".join(f'{i:02x}' for i in rgb) for rgb in rgb_list]
            return render_template("index.html", form=form, path=path, list=hex_list)
        else:
            flash(message="File type not supported. Please choose a valid image file.")
            return render_template("index.html", form=form)
    return render_template("index.html", form=form, path="static/dog-img.jpg", list=dog_hex)




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)



