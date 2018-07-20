# Installation



##Ubuntu

To compile NGINX from the sources, we first need to install its dependencies: 
PCRE, zlib and OpenSSL.

```shell
sudo apt-get update
sudo apt-get install libpcre3-dev zlib1g-dev libssl-dev
```

Of course, it is also possible to download their tarballs and compile them.

To download and unpack Nginx source files

```shell
wget http://nginx.org/download/nginx-1.14.0.tar.gz
tar xvzf nginx-1.14.0.tar.gz
git clone git@github.com:arut/nginx-rtmp-module.git
```

**Configure build options**
We use a custom script below:
```shell
./configure
  --sbin-path=/usr/local/nginx/nginx
  --conf-path=/usr/local/nginx/nginx.conf
  --pid-path=/usr/local/nginx/nginx.pid
  --with-http_ssl_module
  --with-stream
  --add-module=../nginx-rtmp-module \
```

An example of options to the configure script:
```shell
$ ./configure
--sbin-path=/usr/local/nginx/nginx
--conf-path=/usr/local/nginx/nginx.conf
--pid-path=/usr/local/nginx/nginx.pid
--with-pcre=../pcre-8.41
--with-zlib=../zlib-1.2.11
--with-http_ssl_module
--with-stream
--with-mail=dynamic
--add-module=/usr/build/nginx-rtmp-module
--add-dynamic-module=/usr/build/3party_module
```

After Configure, you can see configure summary:
```shell
Configuration summary
  + using system PCRE library
  + using system OpenSSL library
  + using system zlib library

  nginx path prefix: "/usr/local/nginx"
  nginx binary file: "/usr/local/nginx/nginx"
  nginx modules path: "/usr/local/nginx/modules"
  nginx configuration prefix: "/usr/local/nginx"
  nginx configuration file: "/usr/local/nginx/nginx.conf"
  nginx pid file: "/usr/local/nginx/nginx.pid"
  nginx error log file: "/usr/local/nginx/logs/error.log"
  nginx http access log file: "/usr/local/nginx/logs/access.log"
  nginx http client request body temporary files: "client_body_temp"
  nginx http proxy temporary files: "proxy_temp"
  nginx http fastcgi temporary files: "fastcgi_temp"
  nginx http uwsgi temporary files: "uwsgi_temp"
  nginx http scgi temporary files: "scgi_temp"
```

and then

```shell
make
sudo make install
```

```
sudo ln -s /path/to/dir/nginx /usr/sbin/nginx
sudo nginx -v && sudo nginx -V
```

Create systemd unit file
```shell
sudo vim /etc/systemd/system/nginx.service
```

nginx.service
```
[Unit]
Description=A high performance reverse proxy server
After=network.target

[Service]
Type=forking
PIDFile=/usr/local/nginx/nginx.pid
ExecStartPre=/usr/sbin/nginx -t -q -g 'daemon on; master_process on;'
ExecStart=/usr/sbin/nginx -g 'daemon on; master_process on;'
ExecReload=/usr/sbin/nginx -g 'daemon on; master_process on;' -s reload
ExecStop=-/sbin/start-stop-daemon --quiet --stop --retry QUIT/5 --pidfile /usr/local/nginx/nginx.pid
TimeoutStopSec=5
KillMode=mixed

[Install]
WantedBy=multi-user.target
```

```shell
sudo systemctl start nginx.service && sudo systemctl enable nginx.service
sudo systemctl is-enabled nginx.service
```

UFW profile
```shell
sudo vim /etc/ufw/applications.d/nginx
```

/etc/ufw/applications.d/nginx
```
[Nginx HTTP]
title=Web Server (Nginx, HTTP)
description=Small, but very powerful and efficient web server
ports=80/tcp

[Nginx HTTPS]
title=Web Server (Nginx, HTTPS)
description=Small, but very powerful and efficient web server
ports=443/tcp

[Nginx Full]
title=Web Server (Nginx, HTTP + HTTPS)
description=Small, but very powerful and efficient web server
ports=80,443/tcp
```

verity ufw
```
sudo ufw app list
```





## Docker

sudo 

## Mac

- Install pcre, openssl, zlib
```
curl -O https://www.openssl.org/source/openssl-1.0.2o.tar.gz
curl -O https://www.zlib.net/zlib-1.2.11.tar.gz
curl -O ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-8.42.tar.gz
```

- configure
```
./configure \
--prefix=/usr/local/etc/nginx \
--sbin-path=/usr/local/etc/nginx \
--conf-path=/usr/local/etc/nginx/nginx.conf \
--pid-path=/usr/local/etc/nginx/nginx.pid \
--with-openssl=../openssl-1.0.2o \
--with-openssl-opt=darwin64-x86_64-cc \
--with-pcre=../pcre-8.42 \
--with-zlib=../zlib-1.2.11 \
--with-http_addition_module \
--with-http_auth_request_module \
--with-http_dav_module \
--with-http_flv_module \
--with-http_gunzip_module \
--with-http_gzip_static_module \
--with-http_mp4_module \
--with-http_random_index_module \
--with-http_realip_module \
--with-http_slice_module \
--with-http_ssl_module \
--with-http_sub_module \
--with-http_stub_status_module \
--with-http_v2_module \
--with-http_secure_link_module \
--with-mail \
--with-mail_ssl_module \
--with-stream \
--with-stream_realip_module \
--with-stream_ssl_module \
--with-stream_ssl_preread_module \
--with-debug
```
If you wish to build 64-bit openssl library, then you have to
         invoke './Configure darwin64-x86_64-cc' *manually*.



# References
[Installing NGINX Open Source](https://docs.nginx.com/nginx/admin-guide/installing-nginx/installing-nginx-open-source/)

[How to Compile Nginx From Source on Ubuntu 16.04](https://www.vultr.com/docs/how-to-compile-nginx-from-source-on-ubuntu-16-04)

[Compile nginx with openssl on Mac OS X 64-bit](http://hanoian.com/content/index.php/23-compile-nginx-with-openssl-on-mac-os-x-64-bit)

