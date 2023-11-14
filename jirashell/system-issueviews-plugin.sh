#!/bin/bash

BASEDIR=$(dirname $0)

curl https://raw.githubusercontent.com/AlexandraS/report/master/target/container/tomcat6x/cargo-jira-home/webapps/jira/WEB-INF/classes/system-issueviews-plugin.xml \
  > "$BASEDIR/system-issueviews-plugin.xml"
