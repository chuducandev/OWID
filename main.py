import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from download_charts import extract_meta, wait_and_click_show_chart_button

# from crawl_charts import crawl_charts

chrome_driver_path = "/usr/local/bin/chromedriver"
chrome_executable_path = "/Applications/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"

service = Service(executable_path=chrome_driver_path)
options = webdriver.ChromeOptions()
options.binary_location = chrome_executable_path
driver = webdriver.Chrome(service=service, options=options)
#
# try:
#     crawl_charts(driver, 3308, 1)
# finally:
#     driver.quit()


# from openai import OpenAI
#
# from summarize_charts import summarize_charts
#
# client = OpenAI(api_key="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")
# summarize_charts(client, 0, 200)


def crawl_titles():
    txt_folder = "txt"
    meta_folder = "meta"

    os.makedirs(meta_folder, exist_ok=True)

    txt_files = os.listdir(txt_folder)
    num_charts_crawled = 0

    for i, txt_filename in enumerate(txt_files):
        base_filename, _ = os.path.splitext(txt_filename)
        meta_filepath = os.path.join(meta_folder, base_filename + ".json")

        print()
        print("-" * 80)
        print(f"Crawling meta data for chart {base_filename} ({i+1}/{len(txt_files)})")

        if not os.path.exists(meta_filepath):  # Check if summarization exists
            try:
                driver.get(f"https://ourworldindata.org/grapher/{base_filename}")
                wait_and_click_show_chart_button(driver)
                extract_meta(driver, base_filename, meta_folder)
                print(f"Chart crawled: {txt_filename}")
                num_charts_crawled += 1
            except Exception as e:
                print(f"Error crawling chart {base_filename}: {e}")
        else:
            print(f"Chart already crawled: {txt_filename}")

    print(f"Crawled meta data for {num_charts_crawled} charts")


crawl_titles()
