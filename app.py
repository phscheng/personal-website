from flask import Flask, render_template, redirect, url_for, request, flash
from DAL import DataAccessLayer

app = Flask(__name__)
app.secret_key = "change-me"  # only needed if you use flash() below

# Initialize the Data Access Layer
dal = DataAccessLayer()

# Home page
@app.route("/")
def index():
    return render_template("index.html")

# About
@app.route("/about")
def about():
    return render_template("about.html")

# Projects
@app.route("/projects", methods=["GET", "POST"])
def projects():
    if request.method == "POST":
        # Handle project submission
        title = request.form.get("project_title", "")
        description = request.form.get("project_description", "")
        image_filename = request.form.get("project_image", "")
        
        if title and description and image_filename:
            try:
                dal.add_project(title, description, image_filename)
                flash("Project added successfully!")
                return redirect(url_for("projects"))
            except Exception as e:
                flash(f"Error adding project: {str(e)}")
        else:
            flash("Please fill in all required fields.")
    
    # Get all projects from the database
    projects = dal.get_all_projects()
    return render_template("projects.html", projects=projects)

# Resume
@app.route("/resume")
def resume():
    return render_template("resume.html")

# Contact (GET shows form; POST handles submit)
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "")
        message = request.form.get("message", "")
        # TODO: do something with name/message (email it, save to DB, etc.)
        flash("Thanks! Your message was sent.")  # optional
        return redirect(url_for("thankyou"))
    return render_template("contact.html")

# Thank You page (after form submit)
@app.route("/thankyou")
def thankyou():
    return render_template("thankyou.html")

# Optional: nicer 404 page if you create templates/404.html
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    import os

    # Allow overriding host/port/debug via environment variables so the container
    # can be configured at runtime. Defaults: 0.0.0.0:5000, debug off.
    host = os.environ.get("FLASK_RUN_HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "False").lower() in ("1", "true", "yes")

    print(f"Starting Flask app on {host}:{port} (debug={debug})")
    app.run(host=host, port=port, debug=debug)