import requests
from src.static.CONST import HEADER, PRODUCT_FIELDS, logger
from math import ceil

class Crawl:
    def __init__(self):
        self.params = {
            'limit': '100',
            'page': '1',
            'category': None,
            'q': None, 
        }

    def crawl(self):
        pass
    
# The CrawlKeywordCategory class is a subclass of Crawl that crawls Tiki.vn's products based on a
# given category ID and keyword.
class CrawlKeywordCategory(Crawl):
    def __init__(self):
        super().__init__()

    def crawl(self, category_id: int, keyword:str, limit:int) -> list:
        # Add data to dict params
        self.params['category'] = category_id
        self.params['q'] = keyword
        product = []
        limitpage = ceil(limit/100 + 1)        
        try:
            # Crawl data loop for limitpage
            for i in range(1,limitpage):
                self.params['page'] = i
                response = requests.get('https://tiki.vn/api/v2/products', headers=HEADER, params=self.params)#, cookies=cookies)
                if response.status_code == 200:
                    print('request success!!!')
                    for record in response.json().get('data'):
                        field = {}
                        for i in PRODUCT_FIELDS:
                            field[i] = record.get(i)
                        product.append(field)
        except (requests.exceptions.Timeout, requests.exceptions.HTTPError, requests.exceptions.ConnectionError, requests.exceptions.RequestException) as e:
            logger.exception(f'ERROR: {str(e)}')
        except ValueError as e:
            logger.exception(f"Value error: {str(e)}")
        except Exception as e:
            logger.exception(f"Something error: {str(e)}")
        finally:
            return product

# The class `CrawlOnlyKeyword` is a subclass of `Crawl` that crawls Tiki.vn for products based on a
# given keyword and returns a list of product information.
class CrawlOnlyKeyword(Crawl):
    def __init__(self) -> None:
        super().__init__()

    def crawl(self, keyword:str, limit : int) -> list:
        self.params['q'] = keyword
        product = []
        limitpage = ceil(limit/100 + 1)
        try:
            # Crawl data loop for limitpage
            for i in range(1,limitpage):
                self.params['page'] = i
                response = requests.get('https://tiki.vn/api/v2/products', headers=HEADER, params=self.params)#, cookies=cookies)
                if response.status_code == 200:
                    print('request success!!!')
                    for record in response.json().get('data'):
                        field = {}
                        for i in PRODUCT_FIELDS:
                            field[i] = record.get(i)
                        product.append(field)
        except (requests.exceptions.Timeout, requests.exceptions.HTTPError, requests.exceptions.ConnectionError, requests.exceptions.RequestException) as e:
            logger.exception(f'ERROR: {str(e)}')
        except ValueError as e:
            logger.exception(f"Value error: {str(e)}")
        except Exception as e:
            logger.exception(f"Something error: {str(e)}")
        finally:
            return product