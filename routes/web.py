"""Web Routes."""

from masonite.routes import Get, Post

ROUTES = [
    Get("/", "IndexController@show"),
    Post("/", "IndexController@create"),
    Get("/play/@list_id:int", "IndexController@play").name('play'),
]
