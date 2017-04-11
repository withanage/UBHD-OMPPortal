
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


[omp]
doi_format_name=PDF
press_id=6
ignore_format=Softcover
monograph_type_id=68
representative_id_type=6
ignore_submissions=0
xml_category_name=XML
vgwort_enable=1
review_type_id=89
editor_id=99
author_ids=98,100

[web]
application=UBHD_OMPPortal
url=http://heiup.uni-heidelberg.de
vgwort_server1=http://vg07.met.vgwort.de/na/
vgwort_server2=http://vg08.met.vgwort.de/na/

[statistik]
enable=0
id=_omphp

piwik_plugin=1



[emails]
notification=1

[plugins]
solr_index =1