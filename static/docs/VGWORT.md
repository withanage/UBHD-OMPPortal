##  VGWort Pixel Import
### Description
 This tool imports royalty information for germany's vgwort using a Excel File
### Installation
- Requires python xlrd  library

  ```sudo pip2 install xlrd```


#### Configuration
 - Add new VGWORT keys to  UBHD_OMPPortal/static/utils/vgwort.xls


#### Run program
- Change directory in to web2py folder

  ``` cd /usr/local/web2py/  ```
- Execute

 ```python web2py.py -R  applications/UBHD_OMPPortal/static/utils/vgwortInsertBySubmission.py -M  --shell UBHD_OMPPortal ```

