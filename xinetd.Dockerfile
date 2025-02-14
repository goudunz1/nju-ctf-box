FROM alpine:3.18 AS builder

#ARG XINETD_VERSION=2.3.15.4

RUN apk add build-base autoconf automake libtool pkgconf git
#RUN git clone -b ${XINETD_VERSION} https://github.com/openSUSE/xinetd
#Use my own fork of xinetd instead, see issue #47
RUN git clone -b main https://github.com/goudunz1/xinetd
RUN cd xinetd && sh ./autogen.sh && ./configure && make

FROM alpine:latest

COPY --from=builder /xinetd/xinetd /usr/sbin
RUN mkdir -p /etc/xinetd.d/

CMD ["sleep", "infinity"]
