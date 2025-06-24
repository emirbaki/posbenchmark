from py2exe import freeze


freeze(
    windows=['interface.py'],
    options={'includes' : ['scrapy', 'pandas', 'scrapy.crawler', 'scrapy.utils.project', 'scrapy_playwright.page', 'matriks'
                           ,'time', 'os', 'threading', 'tkinter'] ,
                            'bundle_files': 1,
                            'packages': ['posbenchmark', 'posbenchmark.spiders'], },
    data_files= [('scrapy', ['C:/Users/emir.demirci/Desktop/posbenchmark/posbenchmark/scrapy.cfg']),],
    zipfile=None,
)

