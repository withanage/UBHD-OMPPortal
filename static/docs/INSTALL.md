# Installation

## Prerequisites
* Open Monograph Press. 
  * See [documentation](http://pkp.sfu.ca/omp/README)
* Python 2 
   * Check `python --version`
* Python Package manager
  * [pip](https://pypi.python.org/pypi/pip) in debian/ubuntu `sudo apt install python-pip` 
* Web2py Python Framework
  * [Download](http://web2py.com/init/default/download)
  * Unzip it
  * change directory to the the unzipped folder
  * run ```python web2py.py --nogui -a "mypassword"```
  * Output should look like this 
        
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
* ```cd  web2py_folder/applications/```

:bookmark: if you are familiar with  github , please fork the repository to your account
 
:notebook_with_decorative_cover:[doc]()https://guides.github.com/activities/forking/)

* `git clone https://github.com/UB-Heidelberg/UBHD-OMPPortal.git press_name`

or 

 `git clone https://github.com/MY-INSTITUTE/UBHD-OMPPortal.git press_name`  
 
 if you forked.

 :red_circle: Please  use  **only** **_**, ascii alphabet and numbers for the  **press_name** 

* Install dependencies

```bash
cd  web2py_folder/applications/$press_name
sudo pip2 install -r requirements.txt
git checkout clean
git submodule init
git submodule update
```     
* Create Config file

```   bash
cd  web2py_folder/applications/$press_name
mkdir private 
cp web2py_folder/application/$press_name/static/docs/appconfig.ini   web2py_folder/application/$press_name/private/      
```

* Change the settings for your local omp installation private/appconfig.ini   
:warning: Change your settings as in [appconfig.ini ](https://github.com/UB-Heidelberg/UBHD-OMPPortal/blob/categories/static/docs/APPCONFIG.md)
  

* Mount or symlink the files folder of the OMP  to **web2py_folder**/applications/**press_name**/static/monographs/

```
ln -s  /omp_folder/presses/ /web2py_folder/applications/press_name/static/files/presses
```

* Test your installation
```
http://127.0.0.1:8000/press_name
```


  
 
