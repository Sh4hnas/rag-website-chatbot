import requests
from bs4 import BeautifulSoup

class WebsiteScraperError(Exception):
    """Base exception for website scraper errors."""
    pass

class NetworkError(WebsiteScraperError):
    """Raised when network-related errors occur."""
    pass

class ContentExtractionError(WebsiteScraperError):
    """Raised when content extraction fails."""
    pass

def get_website_text(url):
    """
    Fetch and extract text content from a website URL.
    
    Args:
        url: The website URL to scrape
        
    Returns:
        str: Extracted text content from the website
        
    Raises:
        NetworkError: If network-related errors occur (connection, timeout, SSL)
        ContentExtractionError: If content extraction fails or no content found
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

        # Make request with timeout
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()  # Raise exception for bad status codes
        except requests.exceptions.Timeout:
            raise NetworkError("The website took too long to respond. Please try again.")
        except requests.exceptions.ConnectionError:
            raise NetworkError("Unable to reach the website. Please check the URL and your internet connection.")
        except requests.exceptions.SSLError:
            raise NetworkError("SSL certificate error. The website may have security issues.")
        except requests.exceptions.HTTPError as e:
            if response.status_code == 403:
                raise NetworkError("Access forbidden. The website is blocking automated access.")
            elif response.status_code == 404:
                raise NetworkError("Page not found. Please check the URL.")
            elif response.status_code >= 500:
                raise NetworkError("The website server is experiencing issues. Please try again later.")
            else:
                raise NetworkError(f"HTTP error {response.status_code}: {str(e)}")
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Network error: {str(e)}")

        # Parse HTML content
        try:
            soup = BeautifulSoup(response.text, "html.parser")
        except Exception as e:
            raise ContentExtractionError(f"Failed to parse website HTML: {str(e)}")

        # Remove scripts and styles
        for script in soup(["script", "style", "nav", "footer"]):
            script.extract()

        # Extract text
        text = soup.get_text(separator=" ")
        
        # Clean up whitespace
        text = " ".join(text.split())
        
        # Validate that we got meaningful content
        if not text or len(text.strip()) < 100:
            raise ContentExtractionError("Unable to extract sufficient content from this website. The site may be empty or blocking automated access.")

        return text

    except (NetworkError, ContentExtractionError):
        # Re-raise our custom exceptions
        raise
    except Exception as e:
        # Catch any unexpected errors
        raise ContentExtractionError(f"Unexpected error while processing website: {str(e)}")