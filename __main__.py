import os
import time
import globals
import threading
import random
from log import Log
from config import Config
from scraping_manager.automate import Web_scraping

def bot (headless, packages_num, address_list=[]): 
    """Funtion for run a bot in threading with specific range of address
    """

    # Start chrome
    home_page = "https://www.lawn-tek.com/"
    scraper = Web_scraping(headless=headless)

    for address in address_list:

        # Go to gome page
        scraper.set_page(home_page)

        # Search address and select first element
        address_selector = "#address-input"
        first_address_selector = "body > div.pac-container.pac-logo > div"
        selector_submit = "#lawn-container-div > div > button"

        scraper.send_data(address_selector, address)
        time.sleep(2)
        scraper.click(first_address_selector)
        time.sleep(2)
        scraper.click(selector_submit)
        time.sleep(5)

        # Continue page
        scraper.refresh_selenium()

        #   Go to internal frame
        frame_id = "deeplawn-popup-iframe"
        scraper.switch_to_frame (frame_id)

        #   Select continue button
        continue_selector = "#__next div.widget-step-form_buttons__fzKmI > div > button"
        scraper.click(continue_selector)
        time.sleep(2)

        # Select random packages
        scraper.refresh_selenium()
        
        #   Go to internal frame
        scraper.switch_to_main_frame()
        frame_id = "deeplawn-popup-iframe"
        scraper.switch_to_frame(frame_id)

        #   Get all package buttons
        selector_package = "button.MuiButtonBase-root.MuiButton-root.MuiButton-text"
        package_buttons = scraper.get_elems(selector_package)
        valid_button_texts = ["Select Service", "Select Package"]
        package_buttons_filtered = []
        for package_button in package_buttons: 
            if package_button.text in valid_button_texts: 
                package_buttons_filtered.append(package_button)

        #   Debug lines
        # for package_button in package_buttons_filtered: 
        #     print (package_button.text)

        #   Click specific number of package buttons
        for _ in range (packages_num): 
            time.sleep (1)
            random_button = random.choice(package_buttons_filtered)
            random_button.click()
            package_buttons_filtered.remove (random_button)

        # TODO: Go to checkout page



        # TODO: Fill chekout

    # End chrome
    input ("End")
    scraper.end_browser()

def main (): 
    """Main flow of the program
    """
    
    # Logs instance
    logs = Log(os.path.basename(__file__))

    # Get project settings
    credentials = Config()
    threads_num = credentials.get_credential("threads")
    packages_num = credentials.get_credential("packages")
    headless = credentials.get_credential("headless")

    # Read address from file
    address_path = os.path.join (os.path.dirname (__file__), "address.txt")
    with open (address_path) as file: 
        address_list = file.read().splitlines()
    
    # Calculate address for each thread
    end_range = len(address_list)
    skip_values = int(len(address_list)/threads_num)
    range_threads = list(range(0, end_range, skip_values)[1:])
    range_threads [-1] = len(address_list)

    # Debug lines
    range_threads = [1]

    # Create threads
    last_range = 0
    for range_thread in range_threads:

        # Get sublist of address
        thread_num = range_threads.index (range_thread)
        address_range = address_list[last_range:range_thread]

        # Debug lines
        message = f"Starting thread {thread_num}: {last_range}:{range_thread}"
        logs.info(message, print_text=True)

        # Create thread
        globals.status[thread_num] = "Running"
        thread_obj = threading.Thread(target=bot, args=(headless, packages_num, address_range))
        thread_obj.start()

        # Update last range
        last_range = range_thread        

    # TODO: Create threads killer
    


    
    
        


if __name__ == "__main__":
    main()