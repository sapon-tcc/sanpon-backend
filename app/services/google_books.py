import requests



class GoogleBooksService():
    
    
    def retrieve_books(self, q: str, s: str = "") -> dict:
        response = requests.get(f"https://www.googleapis.com/books/v1/volumes?q={q}:subject:{s}&maxResults={40}&langRestrict=pt")
        return response.json()