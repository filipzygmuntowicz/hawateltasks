# hawateltasks
# PREQUISITES
Install required libraries via:
```
pip3 install -r requirements.txt
```
# USAGE:

Run the script via cmd, this will both update the database and generate Excel with  Products table columns. By default the app uses default credentials from xampp with mydb as name of the datbase. If you want to input your own database credentials, you can do it via optional args listed below.
If you're not using a password then use only `--username`, `--host` and `--db_name`. Also you can choose the task with `--task` arg from: update, excel and both (default value).
```
python3 app.py [--task NAME OF THE TASK OR BOTH] [--username USERNAME] [--password PASSWORD] [--host HOST] [--db_name NAME OF YOUR DATABASE] 
```
