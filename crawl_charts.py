from crawl_chart_pages import crawl_chart_pages
from download_charts import download_charts_and_get_entities
from process_charts import process_csv, process_png


def crawl_chart(driver, url, index, retries=3):
    try:
        print()
        print("-" * 80)
        print(f"Processing index {index}:", url)
        file_name = url.split("/")[-1]
        csv_file_name = file_name + ".csv"
        png_file_name = file_name + ".png"

        entities = download_charts_and_get_entities(driver, url, file_name)
        process_csv(csv_file_name, entities)
        process_png(png_file_name)
    except Exception as e:
        print(e)
        print(f"Error processing index {index}:", url)
        if retries > 0:
            print(f"Retrying {retries} more times")
            crawl_chart(driver, url, index, retries - 1)
        else:
            print("No more retries")
            # write the failed url to error file
            with open("error_urls.txt", "a") as f:
                f.write(f"{index}: {url}\n")


def crawl_charts(driver, start_index, num_chart_pages):
    chart_list_url = "https://ourworldindata.org/charts"
    chart_pages = list(
        filter(
            lambda x: x.startswith("https://ourworldindata.org/grapher/"),
            crawl_chart_pages(chart_list_url),
        )
    )
    print("Total chart pages:", len(chart_pages))
    # write chart pages to a file with their indices
    with open("chart_pages.txt", "w") as f:
        for i, url in enumerate(chart_pages):
            f.write(f"{i}: {url}\n")

    for i, url in enumerate(chart_pages[start_index : start_index + num_chart_pages]):
        crawl_chart(driver, url, i + start_index)
