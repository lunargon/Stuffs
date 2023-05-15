import click
from bullet import Bullet, YesNo
from src.static.CONST import logger
from src.service.Crawl import CrawlKeywordCategory, CrawlOnlyKeyword
from src.service.Category import FetchCategory
from src.helper.Helper import input_keyword, limit_input, save_format, saving_ask, render_banner

@click.command()
def crawl():
    """
    Choose options by Enter to select
    """
    render_banner()
    print("Choose type you want to crawl:")
    # Create type of crawl
    crawl_cli = Bullet(choices = ["By categories (and keyword)", "By keyword"])
    crawl_type = crawl_cli.launch()
    try:
        match crawl_type:
            case "By categories (and keyword)":
                # Create and store data to result
                category_choice = [category.name for category in FetchCategory.get_categories()]
                category_cli = Bullet(choices = category_choice)
                result = category_cli.launch()
                id = FetchCategory().get_id(result)
                # Add keyword to categories (Optional)
                answercli= YesNo("Are you want add keyword to crawl with?", default='n')
                answer = answercli.launch()
                if answer:
                    keyword = input_keyword()
                else:
                    keyword = ''
                # Get limit from helper
                limit = limit_input()
                product = CrawlKeywordCategory().crawl(id, keyword, limit)
                format, path = saving_ask()
                save_format(format, product, path)
            case "By keyword":
                keyword = input_keyword()
                limit = limit_input()
                product = CrawlOnlyKeyword().crawl(keyword, limit)
                format, path = saving_ask()
                save_format(format, product, path)
            case _:
                raise Exception("Something error!")
    except Exception as e:
        logger.exception(f"ERROR: {str(e)}")