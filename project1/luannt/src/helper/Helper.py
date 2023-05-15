from src.service.Save import CsvSave, JsonSave, GCloudStore
from src.static.CONST import logger, MAX_DIRECTORY
from bullet import Bullet, YesNo, Numbers
from pyfiglet import Figlet
import re

# Function render banner
def render_banner() -> None:
    figlet = Figlet(font = "slant")
    # writterby = Figlet(font = "slant")
    print("\n"*3)
    print(figlet.renderText("CRAWL TIKI"))
    print()

# Function for input crawl keyword 
def input_keyword() -> str:
    try:
        keyword = input("\nEnter keyword you want to crawl:")
        for char in keyword:
            if not(char.isalnum() or char == " "):
                raise ValueError("Invalid keyword")
    except (ValueError) as e:
        logger.exception(f"Error validating input: {str(e)}")
    return keyword

# Function for input path of folder to save file
def input_path() -> str:
    try:
        path = input("\nEnter path you want to save:")
        # Create check path to check output invalid 
        checkpath = path

        # Regex invalid char
        invalid_char_regex = r'[^\w/-]'

        # Replace "\" with "/"
        path = path.replace('\\', '/')

        # Remove invalid characters
        path = re.sub(invalid_char_regex, '', path)  

        # Remove extra "/" characters
        path = re.sub(r'/+', '/', path)

        # Limit the depth of the folder structure
        bucket_path_parts = path.split("/")
        bucket_path_parts = bucket_path_parts[:MAX_DIRECTORY]
        path = "/".join(bucket_path_parts)

        for char in checkpath:
            if not(char.isalnum() or char == " " or char=="/"):
                print("This tool change your path to valid to saving in Linux/Unix OS")
                raise ValueError("Path has invalid characters. Still create and store in GCloudStorage")
    except ValueError as e:
        logger.exception(f"Error validating input: {str(e)}")
    return path

# Function for input limit product to crawl
def limit_input() -> int:
    limit = 100
    try:
        limitcli = Numbers("\nEnter limit of product you want crawl:", type=int)
        limit = limitcli.launch()
        if limit < 100:
            # Default value
            limit = limit
            raise ValueError("Error limit input! Limit must be at least 100 products.")
        elif limit > 2000:
            # Maxium value (for now)
            limit = 2000
            raise ValueError("Error limit input! Limit out of products.##### CRAWL PRODUCT AS MUCH AS POSSIBLE #####")
    except ValueError as e:
        logger.exception(f"ERROR: {str(e)}")
    return limit

# Function for save file follow format
def save_format(format, data:list, path='') -> None:
    # Select format to save and path to save
    saver = None
    try:
        match format:
            case "csv":
                saver = CsvSave()
            case "json":
                saver = JsonSave()
            case _:
                raise Exception("Error when save!")
        GCloudStore().upload(data, saver, path)
    except Exception as e:
        logger.exception(f"ERROR: {str(e)}")

# Function for ask to choose type format saving
def saving_ask():
    try:
        print("\nChoose type of file to saving:")
        savecli = Bullet(choices = ["csv", "json"])
        format = savecli.launch()
        pathcli = YesNo("You want to add path to save or not?", default='n')
        pathans = pathcli.launch()
        if pathans:
            path = input_path()
        else:
            path = ''
    except Exception as e:
        logger.exception(f"ERROR: {str(e)}")
    return format, path;
