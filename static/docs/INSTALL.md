# Installation

## Prerequisites
1. Install Open Monograph Press. See [documentation](http://pkp.sfu.ca/omp/README)
2. Install web2py
1. [Download] (http://web2py.com/init/default/download) web2py
2. Unzip it
3. change directory to the the unzipped folder
4. If you have python installed : run ```python web2py.py --nogui -a "mypassword"```

Output should look like this 
```
web2py Web Framework
Created by Massimo Di Pierro, Copyright 2007-2017
Version 2.14.6-stable+timestamp.2016.05.10.00.21.47
Database drivers available: pymysql, imaplib, pg8000, sqlite3, sqlite2, pyodbc, mysqlconnector
please visit:
        http://127.0.0.1:8000/
use "kill -SIGTERM 30529" to shutdown the web2py server

```


## Install UBHD-OMPPortal
1. ```cd  web2py_folder/applications/```

2. ```git clone https://github.com/UB-Heidelberg/UBHD-OMPPortal.git press_name```
    - Notice
        - Please  use  **only** **_**, ascii alphabet and numbers for the  **press_name** 
     
3. Install dependencies
```
cd  web2py_folder/applications/$press_name
sudo pip2 install -r requirements.txt
```     

4. Copy appconfig.ini and cahnges the settings accordingly Datails on appconfig.ini are

    ```   mkdir private ```

    ```  cp web2py_folder/application/$press_name/static/docs/appconfig.ini   web2py_folder/application/$press_name/private/     ```

5. Change the settings for your local omp installation private/appconfig.ini   [Details](https://github.com/UB-Heidelberg/UBHD-OMPPortal/blob/categories/static/docs/APPCONFIG.md)
    1. **username** and **password** for the OMP database
    2. **press_id** of the local omp press
    3. define the **press_name** you selected when cloning from git

6. Mount or symlink the files folder of the OMP  to **web2py_folder**/applications/**press_name**/static/monographs/

```
ln -s web2py_folder/applications/press_name/static/monographs/ omp_folder/files/presses/press_id/monographs
```
7. Test your installation
```
http://127.0.0.1:8000/press_name
```


  
 
