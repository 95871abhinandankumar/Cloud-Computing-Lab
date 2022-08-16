FROM python

RUN apt-get update
RUN apt-get install -y default-jdk

RUN wget https://dlcdn.apache.org/hadoop/common/hadoop-3.3.1/hadoop-3.3.1.tar.gz 
RUN tar -xzvf hadoop-3.3.1.tar.gz

ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64/
RUN export JAVA_HOME
RUN mv hadoop-3.3.1 /usr/local/hadoop
ENV PATH /usr/local/hadoop/bin:$PATH
RUN rm -rf hadoop-3*