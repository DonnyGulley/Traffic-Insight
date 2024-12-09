# Imports
import json

# File Path for Bookmarks Storage
BOOKMARK_FILE = "bookmarked_routes.json"

# Bookmark Functionality
def load_bookmarked_routes(username):
    """Load bookmarked routes for a specific user."""
    try:
        with open(BOOKMARK_FILE, "r") as file:
            bookmarks = json.load(file)
        return bookmarks.get(username, [])
    except FileNotFoundError:
        return []

def save_bookmarked_routes(username, routes):
    """Save bookmarked routes for a specific user."""
    try:
        with open(BOOKMARK_FILE, "r") as file:
            bookmarks = json.load(file)
    except FileNotFoundError:
        bookmarks = {}

    bookmarks[username] = routes

    with open(BOOKMARK_FILE, "w") as file:
        json.dump(bookmarks, file, indent=4)

def add_bookmarked_route(username, route):
    """Add a route to the user's bookmarks."""
    bookmarks = load_bookmarked_routes(username)
    if route in bookmarks:
        print(f"\nRoute '{route}' is already bookmarked.")
    else:
        bookmarks.append(route)
        save_bookmarked_routes(username, bookmarks)
        print(f"\nRoute '{route}' has been bookmarked!")

def remove_bookmarked_route(username, route):
    """Remove a route from the user's bookmarks."""
    bookmarks = load_bookmarked_routes(username)
    if route not in bookmarks:
        print(f"\nRoute '{route}' is not in your bookmarks.")
    else:
        bookmarks.remove(route)
        save_bookmarked_routes(username, bookmarks)
        print(f"\nRoute '{route}' has been removed from bookmarks.")

def view_bookmarked_routes(username):
    """Display all bookmarked routes for a user."""
    bookmarks = load_bookmarked_routes(username)
    if bookmarks:
        print("\nYour Bookmarked Routes:")
        for idx, route in enumerate(bookmarks, 1):
            print(f"{idx}. {route}")
    else:
        print("\nYou have no bookmarked routes.")
