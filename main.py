# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
#
# from crawl_charts import crawl_charts
#
# chrome_driver_path = "/usr/local/bin/chromedriver"
# chrome_executable_path = "/Applications/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"
#
# service = Service(executable_path=chrome_driver_path)
# options = webdriver.ChromeOptions()
# options.binary_location = chrome_executable_path
# driver = webdriver.Chrome(service=service, options=options)
#
# try:
#     crawl_charts(driver, 3308, 1)
# finally:
#     driver.quit()
from openai import OpenAI

from summarize_charts import summarize_charts

client = OpenAI(api_key="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")
summarize_charts(client, 0, 200)
