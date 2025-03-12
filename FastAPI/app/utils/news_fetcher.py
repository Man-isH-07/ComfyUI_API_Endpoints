from pygooglenews import GoogleNews
from app.models.schemas import Article, NewsResponse
import logging

logger = logging.getLogger(__name__)

def fetch_google_news(category: str, lang: str, country: str, limit: int) -> NewsResponse:
    try:
        logger.info(f"Fetching trends: category={category}, lang={lang}, country={country}, limit={limit}")
        gn = GoogleNews(lang=lang, country=country)
        news_feed = gn.topic_headlines(category.upper())

        articles = [
            Article(
                title=entry["title"],
                link=entry["link"],
                published=entry["published"],
                source=entry["source"]["title"]
            ) for entry in news_feed["entries"][:limit]
        ]

        return NewsResponse(feed_title=news_feed["feed"].title, articles=articles)
    except Exception as e:
        logger.error(f"Error fetching news: {str(e)}")
        raise Exception(f"Error fetching news: {str(e)}")