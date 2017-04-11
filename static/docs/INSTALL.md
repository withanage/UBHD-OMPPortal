# Installation

## Prerequisites
1. Install Open Monograph Press. See [documentation](http://pkp.sfu.ca/omp/README)
2. Install web2py
1. [Download] (http://web2py.com/init/default/download) web2py
2. Unzip it
3. change directory to the the unzipped folder
4. If you have python installed : run ```python2.7 web2py.py```

## Install UBHD-OMPPortal
1. ```cd  web2py_folder/applications/```

2. ```git clone https://github.com/UB-Heidelberg/UBHD-OMPPortal.git press_name```
    - Notice
     - press_name *should* contain only characters, numbers or _
     - Please do not use **-** in the **press_name**

3. Copy appconfig.ini and cahnges the settings accordingly Datails on appconfig.ini are

    ```   mkdir private ```

    ```  cp web2py_folder/application/UBHD_OMPPortal/static/docs/appconfig.ini   web2py_folder/application/UBHD_OMPPortal/private/     ```

4. Change the settings for your local omp installation private/appconfig.ini   [Details](https://github.com/UB-Heidelberg/UBHD-OMPPortal/blob/categories/static/docs/APPCONFIG.md)
    1. **username** and **password** for the OMP database
    2. **press_id** of the local omp press
    3. define the **press_name** you selected when cloning from git

5. Mount or symlink the files folder of the OMP  to **web2py_folder**/applications/**press_name**/static/monographs/

```
ln -s web2py_folder/applications/press_name/static/monographs/ omp_folder/files/presses/press_id/monographs