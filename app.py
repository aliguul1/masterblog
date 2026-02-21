# from flask import Flask
#
# app = Flask(__name__)
#
#
# @app.route('/')
# def hello_world():
#     return 'Hello, World!'
#
#
# if __name__ == '__main__':
#     app.run(host="0.0.0.0", port=5000, debug=True)
# import json
# from flask import Flask, render_template
#
# app = Flask(__name__)
#
# STORAGE_FILE = "posts.json"
#
#
# def load_posts():
#     """Load blog posts from the JSON storage file."""
#     with open(STORAGE_FILE, "r", encoding="utf-8") as file:
#         return json.load(file)
#
#
# @app.route("/")
# def index():
#     blog_posts = load_posts()
#     return render_template("index.html", posts=blog_posts)
#
#
# if __name__ == "__main__":
#     app.run(debug=True)
import json
import os
from flask import Flask, render_template

app = Flask(__name__)

# Define the storage path as a constant for easy changes later
POSTS_FILE = 'posts.json'

def load_json_data(file_path):
    """
    Generic JSON loader.
    Checks if the file exists and handles potential errors gracefully.
    """
    # Generic file check
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' was not found.")
        return []

    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        print(f"Error: The file '{file_path}' contains invalid JSON formatting.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred while reading '{file_path}': {e}")
        return []

@app.route('/')
def index():
    """
    Index route: Fetches blog posts using generic handler and renders the template.
    """
    blog_posts = load_json_data(POSTS_FILE)
    # Pass the list of dictionaries to the template as 'posts'
    return render_template('index.html', posts=blog_posts)

if __name__ == '__main__':
    # Run the Flask app in debug mode for easier development
    app.run(debug=True)