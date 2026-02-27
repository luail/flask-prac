import re

import requests
from bs4 import BeautifulSoup

from dto import RepoDTO

TRENDING_URL = "https://github.com/trending"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; GithubTrendingBot/1.0)"}


def _parse_stars(text: str) -> int:
    """쉼표가 포함된 스타 수 문자열을 int로 변환한다."""
    return int(text.strip().replace(",", ""))


def _parse_stars_today(text: str) -> int:
    """'362 stars today' 형태의 문자열에서 숫자만 추출한다."""
    match = re.search(r"([\d,]+)", text)
    if match:
        return int(match.group(1).replace(",", ""))
    return 0


def fetch_trending(language: str | None = None) -> list[RepoDTO]:
    """GitHub 트렌딩 페이지를 크롤링하여 저장소 목록을 반환한다.

    Args:
        language: 언어 필터 (예: "python"). None이면 전체 트렌딩.

    Returns:
        RepoDTO 리스트

    Raises:
        requests.RequestException: 네트워크 에러
        ValueError: HTML 파싱 실패
    """
    url = f"{TRENDING_URL}/{language}" if language else TRENDING_URL
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("article", class_="Box-row")

    if not articles:
        raise ValueError("트렌딩 저장소를 찾을 수 없습니다. 페이지 구조가 변경되었을 수 있습니다.")

    repos = []
    for article in articles:
        # 저장소 이름 (owner/repo)
        h2 = article.find("h2")
        a_tag = h2.find("a") if h2 else None
        if not a_tag:
            continue
        name = a_tag.text.strip().replace("\n", "").replace(" ", "")
        repo_url = f"https://github.com{a_tag['href']}"

        # 설명
        p_tag = article.find("p")
        description = p_tag.text.strip() if p_tag else ""

        # 언어
        lang_span = article.find("span", attrs={"itemprop": "programmingLanguage"})
        repo_language = lang_span.text.strip() if lang_span else "Unknown"

        # 전체 스타 수
        star_links = article.find_all("a", href=re.compile(r"/stargazers"))
        stars = _parse_stars(star_links[0].text) if star_links else 0

        # 오늘 획득 스타
        today_span = article.find("span", class_="d-inline-block float-sm-right")
        stars_today = _parse_stars_today(today_span.text) if today_span else 0

        repos.append(RepoDTO(
            name=name,
            description=description,
            language=repo_language,
            stars=stars,
            stars_today=stars_today,
            url=repo_url,
        ))

    return repos
