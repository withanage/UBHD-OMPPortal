
## appconfig variables

### db configuration

#### [db]

##### database url : path to mysql database
 ```
uri       = mysql://mysql-user:mysql-password@localhost:3306/omp_database
```

##### table migration
enables automatic table migration using web2py database layer,  only set 1, if you want to add tables, which are not defined in OMP., otherwise let defaults
```
migrate   = 0
```

##### Used for Connection Pooling
[more Details](http://www.web2py.com/books/default/chapter/29/06/the-database-abstraction-layer#Connection-pooling)
```
pool_size = 1
```

### smtp address and credentials
Necessary, if you want to send emails using the press web-site

#### [smtp]

##### mail server
```
server = smtp.gmail.com:587
```

##### Sender email Address
```
sender = you@gmail.com
```

##### Login username and password
```
login  = username:password
```



### form styling
Only change if you  do not use bootstrap themes. [More details](http://www.web2py.com/books/default/chapter/29/07/forms-and-validators?search=formstyle#Custom-forms)

#### [forms]

```
formstyle = bootstrap3_inline
```
```
separator =
```



## read omp settings

SQL examples assume the OMP database name is omp1_2 and the press_id =6 , please change accordingly

###[omp]

###  id of the current press
```sql 
SELECT press_id FROM omp1_2.presses where path ='my_press'
```

press_id=6

### default format for doi generation (recommended type PDF)
doi_format_name=PDF

### set the book monograph type for the press

```sql 
SELECT genres.genre_id FROM genres ,genre_settings where genres.context_id=6 and  genre_settings.setting_value='Book Manuscript' and genres.genre_id= genre_settings.genre_id
```

monograph_type_id=0

only needed if you have epubs in your press

```sql 
SELECT genres.genre_id FROM genres ,genre_settings where genres.context_id=6 and  genre_settings.setting_value='EPUB Book Manuscript' and genres.genre_id= genre_settings.genre_id
```

epub_monograph_type_id=0

###  ignore a certain submission

ignore_submissions=0

default =0,  enable =1 [see vgwort](http://www.vgwort.de/)
```
vgwort_enable=0
```

### get authors and chapter autor ids

For more details: omp backend http://MYSERVER/omp/index.php/MYPRESS/management/settings/access [sample image]( * [Installation](https://github.com/UB-Heidelberg/UBHD-OMPPortal/blob/master/static/docs/user_settings_dialaog.png)
)) 



```sql 
SELECT  distinct s.user_group_id FROM user_group_stage st, user_group_settings s where st.context_id=6 and st.user_group_id = s.user_group_id and  (s.setting_value='CA'  or s.setting_value='AU')
```

author_ids=98,100

### get editor id

```sql 
SELECT  distinct s.user_group_id FROM user_group_stage st, user_group_settings s where st.context_id=6 and st.user_group_id = s.user_group_id and  (s.setting_value='VE')
```

editor_id=99

### review_type

this is used to enable reviewer comments from backend. e.g. [book](http://heiup.uni-heidelberg.de/catalog/book/122) (Rezensionen und Presse)

First set a review type for your press in

http://MYSERVER/omp/index.php/MYPRESS/management/settings/publication 
e.g name=Prospectus  designation=88P


```sql 
SELECT * FROM genre_settings gs, genres g where gs.setting_value='88P' and gs.genre_id=g.genre_id and g.context_id=6 and g.entry_key='Prospectus' 
```

review_type_id=89



##[web]

### name of the press

application=UBHD_OMPPortal

### url of the  server

url=http://heiup.uni-heidelberg.de

###  vgwort server with an additional fail-over 

do not change

```
vgwort_server1=http://vg07.met.vgwort.de/na/
vgwort_server2=http://vg08.met.vgwort.de/na/
```


### oastatistik server

[oa-statistik](https://dini.de/projekte/oa-statistik/) please contact dulip.withanageATgmail.com for more details. e.g. output click statistic [see here](http://heiup.uni-heidelberg.de/catalog/book/122)


###[statistik]
```
enable=0
id=_omphp
```
### piwik configuration
 
if a piwik server is available, please enable it 
paste piwik code into  views/layout.html under line if int(piwik) == 1: [see example](https://github.com/UB-Heidelberg/UBHD-OMPPortal/blob/master/views/layout.html#L60:L72)


```
piwik_plugin=1
```



### solr plugin 

in development, please leave to 0

#### [plugins]
```
solr_index =0
```