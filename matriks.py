import pandas as pd 
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from posbenchmark.spiders.akakce import AkakceSpider
from posbenchmark.spiders.hepsiburada import HepsiburadaSpider
from posbenchmark.spiders.n11 import N11Spider
from posbenchmark.spiders.trendyol import TrendyolPriceSpider
from posbenchmark.spiders.pazarama import PazaramaSpider
from posbenchmark.spiders.amazon import AmazonSpider
from posbenchmark.spiders.ikasa import ikasaSpider
from posbenchmark.spiders.hizliyazarkasa import hizliyazarkasaSpider

dataframes =  ["./n11_prices.csv", "./hepsiburada_prices.csv",
                "./pazarama_prices.csv", "./akakce_prices.csv",
                "./trendyol_prices.csv", "./hizliyazarkasa_prices.csv",
                "./ikasa_prices.csv", "./amazon_prices.csv"]

spiders = [AkakceSpider, HepsiburadaSpider, N11Spider, TrendyolPriceSpider, PazaramaSpider, AmazonSpider, ikasaSpider, hizliyazarkasaSpider]

def run_spider(spiders):
    process = CrawlerProcess(get_project_settings())

    for spider in spiders:

        # Run the spider programmatically
        process.crawl(spider)
    process.start()

run_spider(spiders)

df_empty = pd.DataFrame()
for df_url in dataframes:
    df = pd.read_csv(df_url)

    df_empty = pd.concat([df_empty, df])
    # Group by Model and Website, then aggregate (e.g., take the first price)
df_grouped = df_empty.groupby(["Model", "Website"])["Price (TL)"].min().reset_index()  # Or.mean(),.min(),.max()
# self.logger.info(df_grouped.describe())
# Create a pivot table to form the price matrix
price_matrix = df_grouped.pivot(index="Model", columns="Website", values="Price (TL)")

# Save the price matrix to a new Excel file
price_matrix.to_excel("price_matrix.xlsx")