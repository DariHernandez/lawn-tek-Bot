import os
import csv
import time
import globals
import threading
import random
from log import Log
from config import Config
from scraping_manager.automate import Web_scraping

def bot (headless, packages_num, checkout_data={}, address_list=[]): 
    """Funtion for run a bot in threading with specific range of address
    """

    # Start chrome
    home_page = "https://www.lawn-tek.com/"
    scraper = Web_scraping(headless=headless)

    frame_id = "deeplawn-popup-iframe"
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
        scraper.switch_to_frame (frame_id)

        #   Select continue button
        continue_selector = "#__next div.widget-step-form_buttons__fzKmI > div > button"
        scraper.click(continue_selector)
        time.sleep(2)


        # Select random packages
        scraper.refresh_selenium()
        
        #   Go to internal frame
        scraper.switch_to_main_frame()
        scraper.switch_to_frame(frame_id)

        #   Get all package buttons
        selector_package = "button.MuiButtonBase-root.MuiButton-root.MuiButton-text"
        package_buttons = scraper.get_elems(selector_package)
        valid_button_texts = ["Select Service", "Select Package"]
        package_buttons_filtered = []
        for package_button in package_buttons: 
            if package_button.text in valid_button_texts: 
                package_buttons_filtered.append(package_button)

        #   Click specific number of package buttons
        for _ in range (packages_num): 
            time.sleep (1)
            random_button = random.choice(package_buttons_filtered)
            random_button.click()
            package_buttons_filtered.remove (random_button)

        #   Go to checkout page
        go_checkout_selector = "button.MuiButtonBase-root.MuiButton-root.MuiButton-contained.step-buttons_next__7fM51"
        scraper.click(go_checkout_selector)


        # Fill chekout
        scraper.refresh_selenium()

        #   Go to internal frame
        scraper.switch_to_main_frame()
        scraper.switch_to_frame(frame_id)

        #   Generate random data
        first_name = random.choice(checkout_data["first_names"])
        last_name = random.choice(checkout_data["last_names"])
        name = f"{first_name} {last_name}"
        email = random.choice(checkout_data["emails"])
        phone = random.choice(checkout_data["phones"])

        #   Fill form
        name_selector = 'input[placeholder="Name"]'
        email_selector = 'input[placeholder="Email"]'
        phone_selector = 'input[placeholder="Phone"]'

        scraper.send_data (name_selector, name)
        scraper.send_data (email_selector, email)
        scraper.send_data (phone_selector, phone)

        #   Pay method
        pay_go_selector = "#myTab > li:nth-child(2)"
        scraper.click(pay_go_selector)

        submit_selector = "#__next > div > div > div > div.widget-step-form_content__1i9p6 > "
        submit_selector += "div > div > div.mt-10.lg\:mt-0 > div > div > button"
        scraper.click(submit_selector)
        time.sleep(5)

    # End chrome
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


    # Read address list from file
    address_path = os.path.join (os.path.dirname (__file__), "address.txt")
    with open (address_path) as file: 
        address_list = file.read().splitlines()

    # Get checkout data
    checkout_data_path = os.path.join (os.path.dirname(__file__), "checkout_data.csv")
    with open (checkout_data_path) as csv_file: 
        csv_reader = csv.reader(csv_file)
        csv_data = list(csv_reader)[1:]
        
        # Format csv data
        checkout_data = {
            "first_names": [],
            "last_names": [],
            "emails": [],
            "phones": []
        }

        for row in csv_data: 
            first_name = row[0]
            last_names = row[1]
            emails = row[2]
            phones = row[3]

            checkout_data["first_names"].append(first_name)
            checkout_data["last_names"].append(last_names)
            checkout_data["emails"].append(emails)
            checkout_data["phones"].append(phones)

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
        thread_obj = threading.Thread(target=bot, args=(headless, 
                                                        packages_num, 
                                                        checkout_data,
                                                        address_range))
        thread_obj.start()

        # Update last range
        last_range = range_thread        

    # TODO: Create threads killer
    


    
    
        


if __name__ == "__main__":
    main()