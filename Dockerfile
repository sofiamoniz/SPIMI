FROM python:3-onbuild

RUN echo "alias ..='cd ..'" >> ~/.bashrc && \
    echo "alias ...='cd ../..'" >> ~/.bashrc && \
    echo "alias ....='cd ../../..'" >> ~/.bashrc && \
    echo "alias grep='grep --colour=auto'" >> ~/.bashrc && \
    echo "alias l='ls -ltr'" >> ~/.bashrc && \
    echo "alias ll='ls -ltr'" >> ~/.bashrc && \
    apt-get update && \
    apt-get install -y vim

RUN python -m nltk.downloader punkt && \
    python -m nltk.downloader stopwords

# Had this before because the python:3-onbuild image was copying everything.
# But that's because the base image copies everything.
# So I created a .dockerignore file.

#FROM python:3.6
#
#RUN mkdir -p /usr/src/app
#WORKDIR /usr/src/app
#
#COPY requirements.txt main.py definitions.py /usr/src/app/
#COPY classes /usr/src/app/classes/
## -r specifies file in which packages are
#RUN pip install --no-cache-dir -r requirements.txt
#
#RUN python -m nltk.downloader punkt && \
#    python -m nltk.downloader stopwords
