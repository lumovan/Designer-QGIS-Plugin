#!/bin/bash

CP="$(dirname "$0")"
#CP=`pwd`

# build the classpath for the Java command
#set cp=%basedir%
#rem set cp=%cp%;%basedir%\jar_one.jar
#rem set cp=%cp%;%basedir%\jar_two.jar
#rem set cp=%cp%;%basedir%\jar_three.jar

# start your main class
java -cp $CP TestApp $1

exit
