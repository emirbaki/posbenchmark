import scrapy
import pandas as pd
import re
from scrapy_playwright.page import PageMethod

class hizliyazarkasaSpider(scrapy.Spider):
    name = "hizliyazarkasa"
    allowed_domains = ["hizliyazarkasa.com"]
    start_urls = ["https://hizliyazarkasa.com"]

    pos_models = [
        "Beko 300 TR",
        "Beko 400 TR",
        "Beko X30 TR",
        "Verifone T650P",
        "Pavo N86",
        "Inpos M530",
        "Paygo SP630",
        "Hugin Tiger T300",
        "Profilo S900",
        "Ingenico Move5000F",
        "Ingenico IDE280",
        "Verifone VX 520",
        "Hugin N910",
        "Xiaomi - Sunmi P2"
    ]

    custom_settings = {
        "PLAYWRIGHT_BROWSER_TYPE": "chromium",
        "FEEDS": {
            "hizliyazarkasa_prices.csv": {
                "format": "csv",
                "overwrite": True
            }
        },
        "ROBOTSTXT_OBEY": True,
        "DOWNLOAD_DELAY": 2,  # 2-second delay between requests
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,  # Limit concurrent requests
    }

    def start_requests(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        search_url = self.get_search_url(self.start_urls[0]) # Use the base url for trendyol
        self.logger.info(search_url)
        yield scrapy.Request(
            search_url,
            headers=headers,
            meta={
                "playwright": True,
                "playwright_page_methods": [PageMethod("wait_for_load_state", "domcontentloaded")],
                "site": self.start_urls[0], # Store the base URL
                "search_url": search_url
            }
        )

    def get_search_url(self, base_url):
        return f"{base_url}"

    async def parse(self, response):
        if response.status != 200:  # Skip non-200 responses
            self.logger.error(f"Failed to fetch {response.url}: Status Code {response.status}")
            return
        response = response.replace(encoding='ISO-8-8859-9')
        self.logger.info(response)
        # model = response.meta["model"]
        site = response.meta["site"]
        search_url = response.meta["search_url"]
        # Extract product titles and prices
        for model in self.pos_models:
            for product in response.xpath("//div[@class='container th-container']/div/div/div[@class = 'project-grid']"):
                title = f"{product.css('div.box-content').xpath('.//h3/a/text()').get()}" # Adjust the selector for the title
                price_text = f"{product.css('div.box-content').css('span.price::text').get()}"  # Adjust the selector for the price
                self.logger.info(title.lower())

                if not title or not price_text or title.lower() == "none":
                    continue

                # Clean and parse the price
                price = self.parse_price(price_text)
                self.logger.info(price_text)
            
                if price is None:
                    continue
                badwords = ['pil', 'kablo', 'ekran', 'kılıf', 'kapağı' , 'kapak', 'pinpad','pınpad','pinped','sehpa', 'rulo', 'çanta', 'merdane', 'entegrasyon', 'şarj', 'adaptör']
                truefalselist = [word in title.lower() for word in badwords]
                flagged_as_bad = any(truefalselist)

                self.logger.info(title.strip().lower())
                self.logger.info(model.strip().lower())
                pattern = re.escape(model.strip())
                match = re.search(pattern, title.strip(), re.IGNORECASE)
                # Filter products based on price and title
                if (price > 3000 and ("pos" in title.lower() or match)) and not flagged_as_bad:
                    yield {
                        "Model": model,
                        "Website": site,
                        "Title": title.strip(),
                        "Price (TL)": price,
                        "URL" : search_url
                    }
    def parse_price(self, price_text):
        # Clean the price text (remove currency symbols, commas, etc.)
        try:
            price_text = price_text.replace("TL", "").replace(".", "").replace(",", ".").strip()
            return float(price_text)
        except (ValueError, AttributeError):
            return None
        
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
        try:
            df = pd.read_csv("hizliyazarkasa_prices.csv")
            self.logger.info(f'shape: {df.shape}')
            # Group by Model and Website, then aggregate (e.g., take the first price)
            df_grouped = df.groupby(["Model", "Website"])["Price (TL)"].min().reset_index()  # Or.mean(),.min(),.max()
            # self.logger.info(df_grouped.describe())
            # Create a pivot table to form the price matrix
            price_matrix = df_grouped.pivot(index="Model", columns="Website", values="Price (TL)")

            # Save the price matrix to a new Excel file
            price_matrix.to_excel("price_matrix.xlsx")
        except FileNotFoundError:
            self.logger.warning("hizliyazarkasa_prices.csv not found. No pivot table created.")
        except Exception as e:
            self.logger.error(f"An error occurred during pivot table creation: {e}")
