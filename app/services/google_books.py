import requests



class GoogleBooksService():
    
    
    def retrieve_books(self, q: str) -> dict:
        response = requests.get(f"https://www.googleapis.com/books/v1/volumes?q={q}&maxResults={40}")
        return response.json()