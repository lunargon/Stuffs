import logging

logger = logging.getLogger()

HEADER = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'vi-VN,vi;q=0.8,en-US;q=0.5,en;q=0.3',
    'Referer': 'https://tiki.vn/?src=header_tiki',
    'x-guest-token': '2uD4i5dbjOIz6WKXBlR1Sr8YeQ0CV9TN',
    'Connection': 'keep-alive',
    'TE': 'Trailers',
}
URL_CATEGORY = "https://api.tiki.vn/raiden/v2/menu-config"
URL_PRODUCT = "https://tiki.vn/api/v2/products"
PRODUCT_FIELDS = ["id", "sku", "name", "url_key", "url_path", "type", "author_name", "book_cover", "brand_name",
                  "short_description", "price", "list_price", "badges", "badges_new", "discount", "discount_rate",
                  "rating_average", "review_count", "order_count", "favourite_count", "thumbnail_url", "thumbnail_width",
                  "thumbnail_height", "freegift_items", "has_ebook", "inventory_status", "is_visible", "productset_id",
                  "productset_group_name", "seller", "is_flower", "is_gift_card", "inventory",
                  "url_attendant_input_form", "option_color", "stock_item", "salable_type", "seller_product_id",
                  "installment_info", "url_review", "bundle_deal", "quantity_sold", "video_url", "tiki_live",
                  "original_price", "shippable"]

BUCKET_NAME = 'project1-luannt'
MAX_DIRECTORY = 3
