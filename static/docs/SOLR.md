
Table of Contents
=================

  * [Table of Contents](#table-of-contents)
  * [Installation](#installation)
      * [Install  JDK](#install--jdk)
      * [Install Solr](#install-solr)
      * [Install Python modules](#install-python-modules)
  * [Configuration](#configuration)
      * [Create OMP Collection and schema file](#create-omp-collection-and-schema-file)
      * [Copy solr schema.xml in to your solr directory](#copy-solr-schemaxml-in-to-your-solr-directory)
  * [Run solr](#run-solr)


# Installation

Cut and paste for (Ubuntu / Debian Systems) for other systems, plese see relevent  docucmentation
### Install  JDK

```
sudo apt-get -y install openjdk-7-jdk
mkdir /usr/java
ln -s /usr/lib/jvm/java-7-openjdk-amd64 /usr/java/default
```


```
sudo apt-get update && apt-get upgrade -y
sudo apt-get install python-software-properties
sudo add-apt-repository ppa:webupd8team/java
sudo apt-get update
sudo apt-get install oracle-java8-installer
java -version
```




### Install Solr
```
cd /tmp/
wget http://archive.apache.org/dist/lucene/solr/6.4.1/solr-6.4.1.tgz
tar xzf solr-6.4.1.tgz solr-6.4.1/bin/install_solr_service.sh --strip-components=2
sudo ./install_solr_service.sh solr-6.4.1.tgz
```


Solr will be installed under /opt/solr and it  start in port 8983
Check with [http://localhost:8983/solr](http://localhost:8983/solr)

### Stop Solr
```
 sudo /opt/solr/bin/solr stop
```



### Install Python modules

```
sudo pip install pysolr

```

# Configuration


### Set folder rights (if necessary)
Set solr to run under local user
```
sudo chown -R my-user:my-group /opt/solr
```

# Run solr

 ```
  /opt/solr/bin/solr -p 8983
  ```


### Create OMP Collection and schema file

Change /opt/solr  to your custom path
##### As current user

```
/opt/solr/bin/solr create -c presss_portal -n omp
```
##### As root
```
 sudo su - solr -c "/opt/solr/bin/solr create -c presss_portal -n omp"
 ```


### Copy solr schema.xml in to your solr directory

```
 cp $WEB2PY_HOME/applications/$MyApplicationName/static/utils/solr/schema.xml /opt/solr/server/solr/presss_portal/conf/
 ```
### Activate SOLR Plugin in $WEB2PY_HOME/applications/$MyApplicationName/private/appconfig.ini
```
[plugins]
solr =1
```

###  Configure solr properties in $WEB2PY_HOME/applications/$MyApplicationName/private/appconfig.ini
```
[solr_plugin]
url = "http://localhost:8983/solr/presss_portal/"
````

# Update solr index
python web2py.py -R  applications/UBHD_OMPPortal/static/utils/solr/updateSolrIndex.py -M  --shell UBHD_OMPPortal 


