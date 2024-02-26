from flask import render_template

from nscworklog import app


@app.errorhandler(400)
def page_not_found(error):
    """Defines 404 error."""
    error_page = render_template("404.html")
    return (error_page, 404)


@app.errorhandler(500)
def internal_error(error):
    with app.app_context():
        db.session.rollback()
    error_page = render_template("500.html")
    return (error_page, 500)
