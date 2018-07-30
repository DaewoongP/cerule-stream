FROM ubuntu:16.04
MAINTAINER alifeunfolds@naver.com

RUN apt-get -y update && apt-get install -y \
    apt-utils \
    build-essential \
    git \
    libpcre3-dev \
    zlib1g-dev \
    libssl-dev \
    ffmpeg

WORKDIR /downloads

ADD http://nginx.org/download/nginx-1.14.0.tar.gz /downloads
ADD ./nginx /download/nginx

RUN tar xzf nginx-1.14.0.tar.gz && \
    git clone https://github.com/arut/nginx-rtmp-module.git

WORKDIR /downloads/nginx-1.14.0
RUN ./configure \
    --sbin-path=/sbin/nginx \
    --conf-path=/usr/local/nginx/nginx.conf \
    --pid-path=/usr/local/nginx/nginx.pid \
    --with-http_ssl_module \
    --with-stream \
    --add-module=../nginx-rtmp-module \
    --with-debug

RUN make && make install
RUN mkdir -p /var/www/hls && mkdir -p /var/www/dash
COPY ./nginx/nginx.conf /usr/local/nginx/nginx.conf
COPY ./index.html /var/www/index.html

EXPOSE 80 443 1883 1935


CMD ["nginx", "-g", "daemon off;"]
