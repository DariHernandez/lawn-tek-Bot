# lawn-tek Bot
**python version: 3.9**

Bot for submit random data for page: [lawn-tek](https://www.lawn-tek.com/)

## Workflow
1. Get all addresses from *address.txt* file (more details in **Settings** section). 
2. Open each chrome window with specific address list for each one.

### In each bot / Chrome window: 

4. Go home page
5. Type address in search bar
6. Select first suggested option
7. Wait for page find the address
8. Go to packages page
9. Select specific number of random packages (more details in **Settings** section). 
10. Go to checkout
11. Fill form with random user data from *checkout_data.csv* file (more details in **Settings** section). 
12. Select option *Pay As You Go*
13. Submit form
14. Continue with next address (in the same chrome windows)


# Install
## Third party modules

Install all modules from pip: 

``` bash
$ pip install -r requirements.txt
```

## Programs

To run the project, the following programs must be installed:

* [Google Chrome](https://www.google.com/intl/es/chrome) last version

# Run the program

Run the *__main__.py*, or the *project folder* with your python 3.9 interpreter. 

# Settings

## address.txt

Text file with a list for address for use in the bot.
The file should not have empty rows
When the program end, all addresses processed will be removed from file.

Sample file: 
```txt
3100 28th Ave Marion 52302 
3230 28th Ave Marion 52302 
3350 28th Ave Marion 52302 
4110 Waldemar Way Marion 52302 
4050 Waldemar Way Marion 52302 
```

## address_finished.txt

File where the processed address will be automated saved.

Sample file: 
```txt
3320 28th Ave Marion 52302 
3415 28th Ave Marion 52302 
4200 Waldemar Way Marion 52302 
```

## checkout_data.csv

CSV file with random data: first_names,last_names, emails,phones
For each address, the bot will be select a random value from each column, to fill the checkout form. 

Sample file: 
```csv
first_names,last_names, emails,phones
Maria, Brown,myemailsample@gmail.com, +14493247419
Joseph, Smith,myemailsample@hotmail.com, +524493247419
"John B.", Alister, myemailsample@yahoo.com,+11123657925
Elizabeth, Hernande, myemailsample@aol.com,+19986347169
```
Sample data selected for a bot: 
* name: *Maria Smith*
* emails: *myemailsample@aol.com*
* phone: *+11123657925*

## con fig.json

All **configurations** are saved in the **con fig.json file**, so **you can edit**

Sample file: 
```json
{
 "threads": 2, 
 "packages": 3, 
 "headless": false
}
```

* ### threads
(Integer greater or equal to 1)
* ### packages
(Integer greater or equal to 1 and smaller or equal than 15)
Number of random packages or services, for select in packages page 
* ### headless
(Boolean: true or false)
Use the browser in headless mode. 
If the value is *true*, the bots will be executed with hidden window.
If the value is *false*, the bots will be executed showing the browser.