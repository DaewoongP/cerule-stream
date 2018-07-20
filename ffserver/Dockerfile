FROM opencoconut/ffmpeg:3.0.2
MAINTAINER DAEWOONGP <qsc1432@gmail.com>

COPY ./ffserver.conf /etc/ffserver.conf

EXPOSE 8090 5454

ENTRYPOINT ["ffserver", "-f", "/etc/ffserver.conf", "RTSP", "enable"]