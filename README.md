# ELK\n
Installing ELK and pushing log. 

Commands to remember:  

[ELASTICSEARCH]. 
Test Elasticsearch. 
  curl -X GET ‘localhost:9200/[INDEX]/_search?pretty’. 

Check index. 
  curl 'localhost:9200/_cat/indices?v'  


[LOGSTASH]. 
Testing config:   
  /usr/share/logstash/bin/logstash -f [CONFIGFILE] –config.test_and_exit. 
  
Run with log and reload automatically when modifying the logstash configuration file:  
  /usr/share/logstash/bin/logstash -f [CONFIGFILE] –config.reload.automatic. 


[FILEBEAT]. 
Run with log display on a specific configuration. 
  Filebeat -e -c [CONFIGFILE.yml] -d publish. 
  
Data path already locked by another beat. 
  rm /var/lib/filebeat/filbeat.lock:  
  
[KIBANA]. 
Create new index. 
  Management settings => [Kibana Section] Index Pattern => Create Index Pattern => logstash to match the pipeline. 


