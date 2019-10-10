FROM tutum/lamp

RUN sed -i "s/http:\/\/archive.ubuntu.com/http:\/\/mirrors.tuna.tsinghua.edu.cn/g" /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y lib32z1 xinetd
RUN apt-get -y install openssh-server && \
    apt-get -y install curl

RUN useradd -m ctf
RUN useradd -u 544  -g users -s /bin/bash -m pwn
WORKDIR /home/

#RUN cp -R /lib* /home/ctf && \
#    cp -R /usr/lib* /home/ctf

#RUN mkdir /home/ctf/dev && \
#    mknod /home/ctf/dev/null c 1 3 && \
#    mknod /home/ctf/dev/zero c 1 5 && \
#    mknod /home/ctf/dev/random c 1 8 && \
#    mknod /home/ctf/dev/urandom c 1 9 && \
#    chmod 666 /home/ctf/dev/*

RUN mkdir /home/ctf/bin && \
    cp /bin/sh /home/ctf/bin && \
    cp /bin/ls /home/ctf/bin && \
    cp /bin/cat /home/ctf/bin && \
    cp /bin/bash /home/ctf/bin && \
    cp /bin/nc /home/ctf/bin && \
    cp /usr/bin/git /home/ctf/bin

COPY ./ctf.xinetd /etc/xinetd.d/ctf
COPY ./start.sh /start.sh
COPY ./genflag.sh /genflag.sh

RUN echo "Blocked by ctf_xinetd" > /etc/banner_fail

RUN chmod +x /start.sh

COPY ./html/ /var/www/html/web/
COPY ./bin/ /home/ctf/
COPY ./sshd_config.txt /etc/ssh/sshd_config
RUN chown -R root:ctf /home/ctf && \
    chmod -R 755 /home/ctf && \
    chown -R ctf:ctf /home/ctf/task && \
    chmod 755 /home/ctf/task && \
    chmod 744 /home/ctf/flag && \
    chown -R ctf:ctf /var/www/html/web/*

RUN service ssh start
CMD ["/start.sh"]
CMD ["/genflag.sh"]


EXPOSE 9999