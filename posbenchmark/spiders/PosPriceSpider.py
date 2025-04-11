import scrapy
from scrapy_playwright.page import PageMethod
import pandas as pd

class PosPriceSpider(scrapy.Spider):
    name = "pos_price"
    start_urls = [
        # "https://www.kontorpos.com",
        # "https://www.ikasa.com.tr",
        # "https://www.hizliyazarkasa.com",
        "https://www.hepsiburada.com",
        "https://www.trendyol.com",
        "https://www.akakce.com",
        "https://www.n11.com",
        "https://www.ciceksepeti.com",
        # "https://www.amazon.com.tr",
        "https://www.pazarama.com"
    ]
    
    pos_models = [
        "Beko 300 TR",
        "Inpos M530",
        "Paygo SP630",
        "Hugin Tiger T300",
        "Profilo S900",
        "Ingenico Move 5000F"
    ]
    
    custom_settings = {
        "PLAYWRIGHT_BROWSER_TYPE": "chromium",
        "FEEDS": {
            "pos_prices.xlsx": {
                "format": "xlsx",
                "overwrite": True
            }
        },
        "ROBOTSTXT_OBEY": True,  # Respect robots.txt
        "HTTPERROR_ALLOWED_CODES": [403, 404],  # Allow 403 and 404 status codes
    }

    def start_requests(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
        }
        for url in self.start_urls:
            for model in self.pos_models:
                search_url = self.get_search_url(url, model)
                yield scrapy.Request(
                    search_url,
                    headers=headers,
                    meta={
                        "playwright": True,
                        "playwright_page_methods": [PageMethod("wait_for_load_state", "domcontentloaded")],
                        "model": model,
                        "site": url
                    }
                )

    def get_search_url(self, base_url, model):
        # if "kontorpos.com" in base_url:
        #     return f"{base_url}/search?q={model.replace(' ', '+')}"
        # elif "ikasa.com.tr" in base_url:
        #     return f"https://ikasa.com.tr/Product/ProductPriceList/6"
        # if "hizliyazarkasa.com" in base_url:
        #     return f"{base_url}/urunler?search={model.replace(' ', '+')}"
        if "hepsiburada.com" in base_url:
            return f"{base_url}/ara?q={model.replace(' ', '%20')}&siralama=artanfiyat"
        elif "trendyol.com" in base_url:
            return f"{base_url}/sr?q={model.replace(' ', '%20')}&qt={model.replace(' ', '%20')}&st={model.replace(' ', '%20')}"
        elif "akakce.com" in base_url:
            return f"{base_url}/arama/?q={model.replace(' ', '+')}"
        elif "n11.com" in base_url:
            return f"{base_url}/arama?q={model.replace(' ', '+')}"
        elif "ciceksepeti.com" in base_url:
            return f"{base_url}/arama?query={model.replace(' ', '%20')}"
        elif "pazarama.com" in base_url:
            return f"{base_url}/arama?q={model.replace(' ', '%20')}&siralama=artan-fiyat"
        else:
            return base_url

    async def parse(self, response):
        if response.status != 200:  # Skip non-200 responses
            self.logger.error(f"Failed to fetch {response.url}: Status Code {response.status}")
            return

        model = response.meta["model"]
        site = response.meta["site"]
        prices = response.xpath("//*[contains(@class, 'price')]").getall()
        
        if not prices:
            self.logger.warning(f"No prices found for {model} on {site}")
            return
        
        for price in prices:
            yield {
                "Model": model,
                "Website": site,
                "Price (TL)": price.strip()
            }

    def handle_error(self, failure):
        # Log the error and yield a placeholder result
        self.logger.error(f"Request failed: {failure.value}")
        yield {
            "Model": failure.request.meta["model"],
            "Website": failure.request.meta["site"],
            "Price (TL)": "N/A"
        }

    def closed(self, reason):
        # Read the scraped data into a DataFrame
        df = pd.read_excel("pos_prices.xlsx")
        
        # Create a pivot table to form the price matrix
        price_matrix = df.pivot(index="Model", columns="Website", values="Price (TL)")
        
        # Save the price matrix to a new Excel file
        price_matrix.to_excel("price_matrix.xlsx")