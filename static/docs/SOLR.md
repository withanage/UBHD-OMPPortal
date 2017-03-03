# Install Solr 

### Install  JDK, if not installed.
```
sudo apt-get -y install openjdk-7-jdk
mkdir /usr/java
ln -s /usr/lib/jvm/java-7-openjdk-amd64 /usr/java/default
```
## (Ubuntu / Debian Systems)

### from binaries
```
sudo apt-get -y install solr-tomcat
```
## From Source
cd /opt
wget http://archive.apache.org/dist/lucene/solr/6.4.1/solr-6.4.1-src.tgz
tar -xvf solr-6.4.1-src.tgz
cp -R solr-6.4.1-src.tgz/example /opt/solr
cd /opt/solr
java -jar start.jar




