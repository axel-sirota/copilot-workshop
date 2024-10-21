from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
# Import the BlogPost class from blog.py
from final.blog_post import BlogPost

app = Flask(__name__)
CORS(app)

# In-memory storage for posts
posts = []

@app.route('/')
def index():
    
    return render_template('index.html')

# GET: Retrieve all blog posts
@app.route('/posts', methods=['GET'])
def get_posts():
    return jsonify([post.__dict__ for post in posts])

# POST: Create a new blog post
@app.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    # Validate input
    if not data.get('title') or not data.get('content'):
        return jsonify({'error': 'Title and content are required'}), 400
    
    new_post = BlogPost(len(posts) + 1, data['title'], data['content'])
    posts.append(new_post)
    return jsonify(new_post.__dict__), 201

# GET: Retrieve a single blog post by id
@app.route('/posts/<int:id>', methods=['GET'])
def get_post(id):
    post = next((post for post in posts if post.id == id), None)
    if post is None:
        return jsonify({'error': 'Post not found'}), 404
    return jsonify(post.__dict__)

# PUT: Update an existing blog post
@app.route('/posts/<int:id>', methods=['PUT'])
def update_post(id):
    data = request.get_json()
    post = next((post for post in posts if post.id == id), None)
    if post is None:
        return jsonify({'error': 'Post not found'}), 404

    # Validate input
    if not data.get('title') or not data.get('content'):
        return jsonify({'error': 'Title and content are required'}), 400

    post.title = data['title']
    post.content = data['content']
    return jsonify(post.__dict__)

# DELETE: Delete a blog post by id
@app.route('/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    post = next((post for post in posts if post.id == id), None)
    if post is None:
        return jsonify({'error': 'Post not found'}), 404
    posts.remove(post)
    return jsonify({'message': 'Post deleted successfully'})


# Search endpoint (with security vulnerability)
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400
    # This is an insecure implementation as it lacks input sanitization
    result = [post.__dict__ for post in posts if query.lower() in post.title.lower()]
    return jsonify(result)


if __name__ == '__main__':
    # add app.run on 0.0.0.0 to make it accessible from outside on port 5000
    app.run(host='0.0.0.0', port=5000)
