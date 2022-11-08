import requests
from requests import HTTPError
from bs4 import BeautifulSoup as Bs


def get_page_from_url(url: str):
    """
    Checks if there is connection to a URL and retrieves the page
    :param url: URL as a string
    :return: the response object if returned 200-400 (some response was given), raises an exception otherwise
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'A HTTP error occurred: {http_err}, {url} returned code {response}')
    except Exception as err:
        print(f'A non-HTTP error occurred: {err}')
    else:
        print(f"Connection to {url} returns 200 - OK")
        return response


def return_html(url: str):
    """turns the response object into a readable html file"""
    response = get_page_from_url(url)
    html_result = Bs(response.text, "html.parser")
    print("HTML fetched")
    return html_result


def save_html_locally(url: str, location: str = 'ali.html'):
    """saves retried html locally"""
    html_result = return_html(url)
    with open(location, 'w', encoding='utf8') as htmlwriter:
        htmlwriter.write(str(html_result))
    print("file saved")


if __name__ == '__main__':
    #assert get_page_from_url("https://www.aliexpress.com") is True
    save_html_locally("https://www.aliexpress.us/?gatewayAdapt=glo2usa")
