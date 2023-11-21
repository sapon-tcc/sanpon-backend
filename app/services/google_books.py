import requests



class GoogleBooksService():
    
    
    def retrieve_books(self, q: str, s: str = "") -> dict:
        base_url = "https://www.googleapis.com/books/v1/volumes"

        if q and not s:
            url = f"{base_url}?q={q}"
        
        elif s:
            url = f"{base_url}?q={q}+subject:{s}"
            
        url = f"{url}&maxResults=40&langRestrict=pt"
        
        response = requests.get(url)
        return response.json()