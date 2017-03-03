# Install Solr 


```
sudo apt-get -y install openjdk-7-jdk
mkdir /usr/java
ln -s /usr/lib/jvm/java-7-openjdk-amd64 /usr/java/default
```
## (Ubuntu / Debian Systems)

### Install  JDK, if not installed.
```
sudo apt-get update && apt-get upgrade -y
sudo apt-get install python-software-properties
sudo add-apt-repository ppa:webupd8team/java
sudo apt-get update
sudo apt-get install oracle-java8-installer
java -version
```
## Install Solr
```
cd /tmp/
wget http://archive.apache.org/dist/lucene/solr/6.4.1/solr-6.4.1.tgz
tar xzf solr-6.4.1.tgz solr-6.4.1/bin/install_solr_service.sh --strip-components=2
sudo ./install_solr_service.sh solr-6.4.1.tgz
```
Solr will be installed under /opt/solr and it  start in port 8983
Check with [http://localhost:8983/solr](http://localhost:8983/solr)
