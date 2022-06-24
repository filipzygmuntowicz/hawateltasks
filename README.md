# hawateltasks
# PREQUISITES
Install required libraries via:
```
pip3 install -r requirements.txt
```
# USAGE:

Run the script via cmd, this will both update the database and generate Excel with  Products table columns. If you want to input your own database credentials, you can do it via optional args listed below. If you're not using a password then use only `--username`, `--host` and `--db_name`.
```
python3 app.py [--username USERNAME] [--password PASSWORD] [--host HOST] [--db_name NAME OF YOUR DATABASE] 
```
