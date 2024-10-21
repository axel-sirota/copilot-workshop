# BlogPost class to represent a blog post
class BlogPost:
    """
    A class used to represent a Blog Post.

    Attributes:
    ----------
    id : int
        The unique identifier for the post.
    title : str
        The title of the blog post.
    content : str
        The content of the blog post.
    """
    def __init__(self, id, title, content):
        self.id = id
        self.title = title
        self.content = content