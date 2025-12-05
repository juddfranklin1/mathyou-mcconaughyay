"""Main application file for the math learning web application."""

from flask import Flask, render_template
from werkzeug.routing import BaseConverter
from routes import init_routes

class RegexConverter(BaseConverter):
    """Permits regular expressions in routes."""
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

app = Flask(__name__, static_folder='static', static_url_path='/static')

# Register the custom 'regex' converter for use in routes.
app.url_map.converters['regex'] = RegexConverter

# Custom 404 error handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Initialize all routes
init_routes(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)