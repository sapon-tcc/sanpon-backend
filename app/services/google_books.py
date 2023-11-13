import requests



class GoogleBooksService():
    
    
    def retrieve_books(self, q: str, s: str = "") -> dict:
        base_url = "https://www.googleapis.com/books/v1/volumes"
        params = {
            'q': q,
            'maxResults': 40,
            'langRestrict': "pt"
        }
        
        if s:
            params['q'] = f"{params['q']}+subject:{s}"
        
        response = requests.get(base_url, params=params)
        return response.json()