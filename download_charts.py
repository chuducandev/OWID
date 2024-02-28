import os
import shutil
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def wait_and_move_file(
    source_directory, extension, destination_path, start_time, timeout=30
):
    file_found = False

    while not file_found and time.time() - start_time < timeout:
        for filename in os.listdir(source_directory):
            mtime = os.path.getmtime(os.path.join(source_directory, filename))
            if mtime > start_time and filename.endswith(extension):
                source_path = os.path.join(source_directory, filename)
                shutil.move(source_path, destination_path)
                file_found = True
                break  # Exit inner loop once a matching file is found

        if not file_found:
            time.sleep(0.1)

    if not file_found:
        raise TimeoutError(
            f"No file with extension '{extension}' found within {timeout} seconds."
        )


def get_element(driver, selector, timeout=10):
    print("Waiting for", selector)
    element = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
    )
    print("Found", selector)
    return element


def wait_and_click(driver, selector, delay=0.5, timeout=10):
    element = get_element(driver, selector, timeout)
    time.sleep(delay)
    element.click()
    time.sleep(delay)
    print("Clicked", selector)


def download_charts(
    driver, file_name, csv_output_folder="plain_csv", png_output_folder="plain_png"
):
    try:
        show_chart_button = get_element(
            driver, 'button[data-track-note="chart_click_chart"]'
        )
        time.sleep(1)
        show_chart_button_parent = show_chart_button.find_element(By.XPATH, "..")
        show_chart_button_parent_class = show_chart_button_parent.get_attribute("class")
        print(show_chart_button_parent_class)

        if "active" not in show_chart_button_parent_class:
            print("Clicking show chart button")
            show_chart_button.click()
    except Exception as e:
        print(e)
        print("No chart found")
        raise e

    wait_and_click(driver, 'button[data-track-note="chart_click_download"]', delay=1.5)

    original_url = driver.current_url
    csv_start_time = time.time()
    wait_and_click(driver, 'button[data-track-note="chart_download_csv"]')
    if original_url != driver.current_url:
        raise Exception("The page has changed")

    png_start_time = time.time()
    wait_and_click(driver, 'button[data-track-note="chart_download_png"]')

    downloads_folder = os.path.expanduser("~/Downloads")
    os.makedirs(csv_output_folder, exist_ok=True)
    os.makedirs(png_output_folder, exist_ok=True)

    csv_file_name = file_name + ".csv"
    csv_destination_path = os.path.join(csv_output_folder, csv_file_name)

    png_file_name = file_name + ".png"
    png_destination_path = os.path.join(png_output_folder, png_file_name)

    wait_and_move_file(downloads_folder, "csv", csv_destination_path, csv_start_time)
    wait_and_move_file(downloads_folder, "png", png_destination_path, png_start_time)

    wait_and_click(driver, 'button[class="modalDismiss"]', delay=0.1)


def get_entities(driver):
    try:
        wait_and_click(
            driver, 'button[data-track-note="chart_add_entity"]', delay=0.1, timeout=2
        )
    except Exception as e:
        print("No selected entities found")
        return []
    entities_div = get_element(driver, 'div[class="entities"]')
    selected_entities = entities_div.find_elements(By.CLASS_NAME, "selectedData")
    if selected_entities:
        selected_entities = selected_entities[0]
        entities = selected_entities.find_elements(By.CLASS_NAME, "label")
        entity_list = [entity.text for entity in entities]
        print("Entities found:", entity_list)
        return entity_list
    else:
        search_results = entities_div.find_elements(By.CLASS_NAME, "searchResults")
        if search_results:
            # get all li tags with class "clickable selected"
            entities = search_results[0].find_elements(
                By.CLASS_NAME, "clickable.selected"
            )
            entity_list = [entity.text for entity in entities]
            print("Entities found:", entity_list)
            return entity_list
        else:
            raise Exception("No entities found")


def download_charts_and_get_entities(driver, url, file_name):
    driver.get(url)
    download_charts(driver, file_name)
    return get_entities(driver)
