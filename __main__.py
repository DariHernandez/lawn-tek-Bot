import os
import csv
import sys
import time
import globals
import threading
import random
from log import Log
from config import Config
from scraping_manager.automate import Web_scraping

# Logs instance
logs = Log(os.path.basename(__file__))

def bot_killer (threads_num):
    """Send end status for each thread / bot

    Args:
        threads_num (int): number of threads runing
    """

    time.sleep (5)
    print ("All threads / bots running")
    while True:
        exit_key = input ('\nPress "q" to quit\n')
        if exit_key.lower().strip() == 'q':
            break
    
    print ("Killing threads...")
    for thread_num in range (1, threads_num+1): 
        globals.status[thread_num] = "end"
     

def bot (thread_counter, headless, packages_num, checkout_data, address_list): 
    """Funtion for run a bot in threading with specific range of address

    Args:
        thread_counter (int): Number of the current bot thread
        headless (bool): Hide (true) or show (false) the chrome window
        packages_num (int): number of packages and service for random select
        checkout_data (dict): Lists of user data: names, phone and emails
        address_list (list): List of addresses
    """

    logs.info("Starting thread {thread_counter}...")

    # Start chrome
    home_page = "https://www.lawn-tek.com/"
    scraper = Web_scraping(headless=headless)

    frame_id = "deeplawn-popup-iframe"
    for address in address_list:
        
        address_num = address_list.index (address) + 1

        # Validate status
        if globals.status[thread_counter] == "end": 
            message = f"Thread {thread_counter} killed."
            logs.info (message, print_text=True)
            break

        # Status
        message = f"Thread {thread_counter}, address: {address_num} / {len(address_list)}"
        logs.info(message, print_text=True)
    
        # Go to gome page
        scraper.set_page(home_page)

        # Search address and select first element
        address_selector = "#address-input"
        first_address_selector = "body > div.pac-container.pac-logo > div"
        selector_submit = "#lawn-container-div > div > button"

        scraper.send_data(address_selector, address)
        time.sleep(2)
        try:
            scraper.click(first_address_selector)
        except: 
            pass
        time.sleep(2)
        scraper.click(selector_submit)
        try:
            scraper.click(selector_submit)
        except: 
            pass
        time.sleep(5)


        # Continue page
        scraper.refresh_selenium()

        #   Go to internal frame
        scraper.switch_to_frame (frame_id)

        #   Wait to page load
        selector_spinner = "#__next > div > div > div > div.widget-step-form_content__1i9p6 > div > div > div > div:nth-child(4) > div.mx-auto > div"
        scraper.wait_die(selector_spinner, time_out=300)

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


        # Chekout
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
        time.sleep(3)

        submit_selector = "#__next > div > div > div > div.widget-step-form_content__1i9p6 > "
        submit_selector += "div > div > div.mt-10.lg\:mt-0 > div > div > button"

        scraper.click_js(submit_selector)
        time.sleep(5)

    # End chrome
    scraper.end_browser()
    sys.exit()

def main (): 
    """Main flow of the program
    """

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
    range_threads = list(range(0, end_range+1, skip_values)[1:])
    range_threads [-1] = len(address_list)

    # Debug lines
    # range_threads = [1]

    # Create threads
    last_range = 0
    for range_thread in range_threads:

        # Get sublist of address
        thread_num = range_threads.index (range_thread) + 1
        address_range = address_list[last_range:range_thread]

        # Debug lines
        message = f"Starting thread {thread_num}: {last_range}:{range_thread}"
        logs.info(message, print_text=True)

        # Create thread
        globals.status[thread_num] = "Running"
        thread_obj = threading.Thread(target=bot, args=(thread_num, 
                                                        headless, 
                                                        packages_num, 
                                                        checkout_data,
                                                        address_range))
        thread_obj.start()

        # Update last range
        last_range = range_thread       


    # Create thread killer
    thread_obj = threading.Thread(target=bot_killer, args=(len(range_threads),))
    thread_obj.start()


if __name__ == "__main__":
    main()