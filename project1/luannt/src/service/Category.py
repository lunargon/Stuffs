import requests
from src.static.CONST import URL_CATEGORY,HEADER

class Category:
    def __init__(self, name, id):
        self.name = name
        self.id_category = id

# The FetchCategory class has methods to fetch and retrieve category data from a specified URL.
class FetchCategory:
    @staticmethod
    def get_categories() -> list:
        categories = []
        catagories_data = requests.get(url = URL_CATEGORY,headers = HEADER).json()
        for category in catagories_data.get('menu_block').get('items'):
            name = category.get('text')
            link_category = category.get('link')
            link_category = link_category.split('/c')
            categories.append(Category(name, link_category[-1]))
        return categories

    def get_id(self, name):
        for catagory in self.get_categories():
            if name == catagory.name:
                return catagory.id_category