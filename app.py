import json
import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
POSTS_FILE = 'posts.json'


def load_posts(file_path):
    """Generic loader: prints error to console if file is missing."""
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' was not found.")
        return []
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error reading '{file_path}': {e}")
        return []


def save_posts(file_path, data):
    """Generic saver: writes to file and logs errors."""
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Error: Could not save to '{file_path}': {e}")


@app.route('/')
def index():
    """Displays all blog posts."""
    posts = load_posts(POSTS_FILE)
    return render_template('index.html', posts=posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """Handles adding a new blog post with 0 initial likes."""
    if request.method == 'POST':
        posts = load_posts(POSTS_FILE)
        new_id = max([p['id'] for p in posts], default=0) + 1
        new_post = {
            'id': new_id,
            'author': request.form.get('author'),
            'title': request.form.get('title'),
            'content': request.form.get('content'),
            'likes': 0
        }
        posts.append(new_post)
        save_posts(POSTS_FILE, posts)
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """Pre-fills form with existing data and saves changes."""
    posts = load_posts(POSTS_FILE)
    post = next((p for p in posts if p['id'] == post_id), None)

    if post is None:
        print(f"Update Error: ID {post_id} not found.")
        return "Post not found", 404

    if request.method == 'POST':
        post['author'] = request.form.get('author')
        post['title'] = request.form.get('title')
        post['content'] = request.form.get('content')
        save_posts(POSTS_FILE, posts)
        return redirect(url_for('index'))

    return render_template('update.html', post=post)


@app.route('/delete/<int:post_id>')
def delete(post_id):
    """Removes a post from storage."""
    posts = load_posts(POSTS_FILE)
    posts = [p for p in posts if p['id'] != post_id]
    save_posts(POSTS_FILE, posts)
    return redirect(url_for('index'))


@app.route('/like/<int:post_id>')
def like(post_id):
    """Bonus: Increments the like count for a specific post."""
    posts = load_posts(POSTS_FILE)
    post = next((p for p in posts if p['id'] == post_id), None)

    if post:
        post['likes'] = post.get('likes', 0) + 1
        save_posts(POSTS_FILE, posts)
    else:
        print(f"Like Error: ID {post_id} not found.")

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
