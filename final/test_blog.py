import pytest
from final.blog_app import app
from final.blog_post import BlogPost

# Sample test for BlogPost class
def test_create_post():
    post = BlogPost(1, 'My First Post', 'This is the content of my first post')
    assert post.id == 1
    assert post.title == 'My First Post'
    assert post.content == 'This is the content of my first post'

# Test API endpoints using the Flask test client
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_posts(client):
    response = client.get('/posts')
    assert response.status_code == 200

def test_create_post_via_api(client):
    response = client.post('/posts', json={
        'title': 'New Post',
        'content': 'This is a new blog post'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['title'] == 'New Post'
    assert data['content'] == 'This is a new blog post'

def test_update_post(client):
    client.post('/posts', json={
        'title': 'Post to Update',
        'content': 'Old content'
    })
    response = client.put('/posts/1', json={
        'title': 'Updated Title',
        'content': 'Updated content'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['title'] == 'Updated Title'
    assert data['content'] == 'Updated content'

def test_delete_post(client):
    client.post('/posts', json={
        'title': 'Post to Delete',
        'content': 'To be deleted'
    })
    response = client.delete('/posts/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Post deleted successfully'

def test_search_posts(client):
    client.post('/posts', json={
        'title': 'Searchable Post',
        'content': 'Content that is searchable'
    })
    response = client.get('/search?q=Searchable')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) > 0
    assert 'Searchable Post' in data[0]['title']
