import os

FAVORITES_FILE = "favorites.txt"


class FavoriteManager:
    @staticmethod
    def add_favorite(stock_code):
        """Adds a stock code to the favorites list."""
        favorites = FavoriteManager.load_favorites()
        if stock_code not in favorites:
            favorites.append(stock_code)
            FavoriteManager.save_favorites(favorites)

    @staticmethod
    def remove_favorite(stock_code):
        """Removes a stock code from the favorites list."""
        favorites = FavoriteManager.load_favorites()
        if stock_code in favorites:
            favorites.remove(stock_code)
            FavoriteManager.save_favorites(favorites)

    @staticmethod
    def load_favorites():
        """Loads the favorites list from a file."""
        if not os.path.exists(FAVORITES_FILE):
            return []
        with open(FAVORITES_FILE, "r") as f:
            return [line.strip() for line in f.readlines()]

    @staticmethod
    def save_favorites(favorites):
        """Saves the favorites list to a file."""
        with open(FAVORITES_FILE, "w") as f:
            f.write("\n".join(favorites))
