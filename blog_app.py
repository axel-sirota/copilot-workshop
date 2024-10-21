# Import Flask and create the app
from flask import Flask, jsonify, request, render_template
from final.blog_post import BlogPost
from flask_cors import CORS  # Import CORS

# Create the Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS

# In-memory storage for posts
posts = []

# Error handling
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# GET: Retrieve all blog posts
@app.route('/posts', methods=['GET'])
def get_posts():
    return jsonify([post.__dict__ for post in posts])

# Add a route to render the index.html template
@app.route('/')
def index():
    return render_template('index.html')

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

# Update a blog post
@app.route('/posts/<int:id>', methods=['PUT'])
"""
Update an existing blog post.
Endpoint: /posts/<int:id>
Method: PUT
Args:
    id (int): The ID of the post to update.
Request Body (JSON):
    title (str): The new title of the post.
    content (str): The new content of the post.
Returns:
    Response (JSON): The updated post data if successful.
    Response (JSON): An error message if the input is invalid or the post is not found.
Status Codes:
    200: Post updated successfully.
    400: Invalid input, title and content are required.
    404: Post not found.
"""
def update_post(id):
    data = request.get_json()
    # Validate input
    if not all(key in data for key in ('title', 'content')):
        return jsonify({'error': 'Title and content are required'}), 400
    
    post = next((post for post in posts if post.id == id), None)
    if post is None:
        return jsonify({'error': 'Post not found'}), 404
    
    post.title = data['title']
    post.content = data['content']
    return jsonify(post.__dict__), 200

# Delete a blog post
@app.route('/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    global posts
    posts = [post for post in posts if post.id != id]
    return jsonify({'message': 'Post deleted'}), 200

# Add searching a blog post
@app.route('/search', methods=['GET'])
def search_posts():
    query = request.args.get('q')
    if query is None:
        return jsonify({"error": "Query parameter is required"}), 400
    
    results = [post.__dict__ for post in posts if query.lower() in post.title.lower()]
    return jsonify(results), 200

if __name__ == '__main__':
    app.run(debug=True)