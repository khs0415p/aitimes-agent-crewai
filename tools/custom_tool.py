import requests
from datetime import datetime
from bs4 import BeautifulSoup
from crewai.tools import tool


DATE_FORMAT = "%Y.%m.%d %H:%M"
BASE_URL = "https://www.aitimes.com"


@tool
def get_today_newslink():
    """오늘 날짜로 업로드 된 뉴스 link 리스트들을 추출하는 함수입니다."""
    url = "{}/news/articleList.html?page={}&total=21482&box_idxno=&view_type=sm"
    page = 1
    flag = True
    while flag:
        response = requests.get(url.format(BASE_URL, page))
        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.select("section#section-list ul.type2 li")

        news_list = []
        for article in articles:
            title_tag = article.select_one("h4.titles a")
            if title_tag and title_tag.has_attr("href"):
                link = BASE_URL + title_tag["href"]
            else:
                continue
            byline_tags = article.select("span.byline em")
            if len(byline_tags) > 1:
                date_string = byline_tags[1].get_text(strip=True)
            else:
                continue

            news_date = datetime.strptime(date_string, DATE_FORMAT)
            if news_date.date() == datetime.today().date():
                news_list.append((link))
            else:
                flag = False
                break
        page += 1

    return news_list

@tool
def get_detail_news(link_list: list):
    """주어진 link_list를 통해 뉴스의 정보를 추출하는 함수입니다."""

    contents = []
    for link in link_list:
        response = requests.get(link)
        soup = BeautifulSoup(response.text, "html.parser")
        title_tag = soup.find("h3", "heading")
        title = title_tag.text

        content_tags = soup.select("article#article-view-content-div p")
        content = " ".join([content_tag.text for content_tag in content_tags])
        contents.append(title + content)

    return contents