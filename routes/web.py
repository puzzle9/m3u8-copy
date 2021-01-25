"""Web Routes."""

from masonite.routes import Get, Post

ROUTES = [
    Get("/", "IndexController@show"),
    Post("/", "IndexController@create"),
]
