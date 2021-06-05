EXECUTION
- Run the Executable file in the 'dist' folder
- If you have the correct dependencies, you can run the script itself

---------------------------------------------------------------------------------------------------

OPTIONS FILE
You can save predefined settings so you don't have to type them out every time you run the
program, check out the file 'dist/options.json'. Below, there are some settings that can
be changed, or left alone 

---Main Options---
refresh_delay: How long the program waits before checking the prices again
default value is '5'

autoload: Make the autoload prompt show up
default value is 'none

---Specific Coins Monitor Settings---
name: If you want to assign a name
default value is 'none'

static_link: If you want to check the same coin every time, change this field to the link
default value is 'none'

static_direction: If you want to check above or below every time, change this field to the check criteria
default value is 'none'

static_price: If you want to check the same price every time, change this field to the price
default value is 'none'

emails: If you want emails to be sent when the price passes the thresholds you put, change this field to your email address
default value is 'none'
NOTE: You might have to set 'pythonautosend@gmail.com' as a trusted sender on your email account since it might get flagged as spam

---------------------------------------------------------------------------------------------------

AUTHOR
Remus Calugarescu
2021-04-25

---------------------------------------------------------------------------------------------------

LAST MODIFIED
2021-04-30

---------------------------------------------------------------------------------------------------

OTHER
- If you have the correct libraries installed, you can run $pyinstaller --onefile poomonitor.py to recreate the executable
- If you're getting issues loading the chrome driver, you need to get the correct version (google it, its easy)
- If you're getting issues loading the webpage, the website may have started to ignore your requests, try again a bit later
- If webpage doesn't load, run the 'killallchrome.bat' file, note that it kills ALL chrome tasks (even regular browser ones)
- Don't be a douchebag and mess with the pythonautosend@gmail.com password >_>
