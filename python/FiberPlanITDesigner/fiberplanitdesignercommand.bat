
rem sets the basedir to the directory where this batch file is locaed


set basedir=%~dp0



rem build the classpath for the Java command

set cp=%basedir%
rem set cp=%cp%;%basedir%\jar_one.jar
rem set cp=%cp%;%basedir%\jar_two.jar

rem set cp=%cp%;%basedir%\jar_three.jar



rem start your main class
java -cp %cp% TestApp %1
