<div><a href='https://github.com/github.com/darideveloper/blob/master/LICENSE' target='_blank'>
            <img src='https://img.shields.io/github/license/github.com/darideveloper.svg?style=for-the-badge' alt='MIT License' height='30px'/>
        </a><a href='https://www.linkedin.com/in/francisco-dari-hernandez-6456b6181/' target='_blank'>
                <img src='https://img.shields.io/static/v1?style=for-the-badge&message=LinkedIn&color=0A66C2&logo=LinkedIn&logoColor=FFFFFF&label=' alt='Linkedin' height='30px'/>
            </a><a href='https://t.me/darideveloper' target='_blank'>
                <img src='https://img.shields.io/static/v1?style=for-the-badge&message=Telegram&color=26A5E4&logo=Telegram&logoColor=FFFFFF&label=' alt='Telegram' height='30px'/>
            </a><a href='https://github.com/darideveloper' target='_blank'>
                <img src='https://img.shields.io/static/v1?style=for-the-badge&message=GitHub&color=181717&logo=GitHub&logoColor=FFFFFF&label=' alt='Github' height='30px'/>
            </a><a href='https://www.fiverr.com/darideveloper?up_rollout=true' target='_blank'>
                <img src='https://img.shields.io/static/v1?style=for-the-badge&message=Fiverr&color=222222&logo=Fiverr&logoColor=1DBF73&label=' alt='Fiverr' height='30px'/>
            </a><a href='https://discord.com/users/992019836811083826' target='_blank'>
                <img src='https://img.shields.io/static/v1?style=for-the-badge&message=Discord&color=5865F2&logo=Discord&logoColor=FFFFFF&label=' alt='Discord' height='30px'/>
            </a><a href='mailto:darideveloper@gmail.com?subject=Hello Dari Developer' target='_blank'>
                <img src='https://img.shields.io/static/v1?style=for-the-badge&message=Gmail&color=EA4335&logo=Gmail&logoColor=FFFFFF&label=' alt='Gmail' height='30px'/>
            </a></div><div align='center'><br><br><img src='https://github.com/darideveloper/lawn-tek-Bot/blob/master/logo.jpg?raw=true' alt='Lawn Tek Bot' height='80px'/>

# Lawn Tek Bot

Bot for submit random data for page: lawn-tek

Start date: **2021-09-17**

Last update: **2023-04-12**

Project type: **client's project**

</div><br><details>
            <summary>Table of Contents</summary>
            <ol>
<li><a href='#buildwith'>Build With</a></li>
<li><a href='#media'>Media</a></li>
<li><a href='#details'>Details</a></li>
<li><a href='#install'>Install</a></li>
<li><a href='#settings'>Settings</a></li>
<li><a href='#run'>Run</a></li></ol>
        </details><br>

# Build with

<div align='center'><a href='https://www.python.org/' target='_blank'> <img src='https://cdn.svgporn.com/logos/python.svg' alt='Python' title='Python' height='50px'/> </a><a href='https://www.selenium.dev/' target='_blank'> <img src='https://cdn.svgporn.com/logos/selenium.svg' alt='Selenium' title='Selenium' height='50px'/> </a></div>

# Details

## Workflow\r
\r
Get all addresses from address.txt file (more details in **Settings** section).\r
Open each chrome window with specific address list for each one.\r
\r
## In each bot / Chrome window:\r
\r
1. Go home page\r
2. Type address in search bar\r
3. Select first suggested option\r
4. Wait for page find the address\r
5. Go to packages page\r
6. select the only package.\r
7. Go to checkout\r
8. Fill form with random user data from checkout_data.csv file (more details in Settings section).\r
9. Select option Pay As You Go\r
10. Submit form\r
11. Continue with next address (in the same chrome windows)

# Install

## Third party modules\r
\r
Install all modules from pip:\r
\r
\\`\\`\\`bash\r
$ pip install -r requirements.txt\r
\\`\\`\\`\r
\r
## Programs\r
\r
To run the project, the following programs must be installed:\r
\r
* [Google Chrome](https://www.google.com/intl/es_es/chrome/) last version

# Settings

## address.txt\r
\r
Text file with a list for address for use in the bot.\r
The file should not have empty rows\r
When the program end, all addresses processed will be removed from file.\r
\r
Sample file: \r
\\`\\`\\`txt\r
3100 28th Ave Marion 52302 \r
3230 28th Ave Marion 52302 \r
3350 28th Ave Marion 52302 \r
4110 Waldemar Way Marion 52302 \r
4050 Waldemar Way Marion 52302 \r
\\`\\`\\`\r
\r
## address_finished.txt\r
\r
File where the processed address will be automated saved.\r
\r
Sample file: \r
\\`\\`\\`txt\r
3320 28th Ave Marion 52302 \r
3415 28th Ave Marion 52302 \r
4200 Waldemar Way Marion 52302 \r
\\`\\`\\`\r
\r
## checkout_data.csv\r
\r
CSV file with random data: first_names,last_names, emails,phones\r
For each address, the bot will be select a random value from each column, to fill the checkout form. \r
\r
Sample file: \r
\\`\\`\\`csv\r
first_names,last_names, emails,phones\r
Maria, Brown,myemailsample@gmail.com, +14493247419\r
Joseph, Smith,myemailsample@hotmail.com, +524493247419\r
\\\"John B.\\\", Alister, myemailsample@yahoo.com,+11123657925\r
Elizabeth, Hernande, myemailsample@aol.com,+19986347169\r
\\`\\`\\`\r
Sample data selected for a bot: \r
* name: *Maria Smith*\r
* emails: *myemailsample@aol.com*\r
* phone: *+11123657925*\r
\r
## config.json\r
\r
All **configurations** are saved in the **con fig.json file**, so **you can edit**\r
\r
Sample file: \r
\\`\\`\\`json\r
{\r
 \\\"threads\\\": 2, \r
 \\\"headless\\\": false\r
}\r
\\`\\`\\`\r
\r
### threads\r
(Integer greater or equal to 1)\r
Number of Bots / Chrome windows to open at the same time\r
### headless\r
(Boolean: true or false)\r
Use the browser in headless mode. \r
If the value is *true*, the bots will be executed with hidden window.\r
If the value is *false*, the bots will be executed showing the browser.

# Run

Run the main.py, or the project folder with your python 3.9 interpreter.


