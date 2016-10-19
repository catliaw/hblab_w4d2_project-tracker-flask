from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/")
def homepage():
    """Show homepage with links to projects and students (github username)."""

    student_rows = hackbright.get_all_students()
    project_rows = hackbright.get_all_projects()

    return render_template("homepage.html",
                            student_rows=student_rows,
                            project_rows=project_rows)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github', 'jhacks')
    first, last, github = hackbright.get_student_by_github(github)
    rows = hackbright.get_grades_by_github(github) #rows returns list of tuples which includes project_title [0], grade [1]

    return render_template("student_info.html",
                            first=first,
                            last=last,
                            github=github,
                            rows = rows)


@app.route("/project")
def find_project():
    """ Show information about a project"""

    title = request.args.get("title")
    project_title, description, max_grade = hackbright.get_project_by_title(title)
    rows = hackbright.get_grades_by_title(title)

    return render_template("project_info.html",
                            project_title=project_title,
                            description=description,
                            max_grade=max_grade,
                            rows=rows)


@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")


@app.route("/student-form")
def student_form():
    """Show form for creating a new record IN DATABASE for a student."""

    return render_template("create_student.html")


@app.route("/student-add", methods=['POST'])
def student_add():
    """Acknowledge student added. Link to student page."""

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    github = request.form.get('github')

    hackbright.make_new_student(first_name, last_name, github)

    return render_template("student_added.html",
                            first_name=first_name,
                            github=github)


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
