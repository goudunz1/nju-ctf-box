FROM goudunz1/xinetd:alpine AS builder

FROM python:alpine

COPY --from=builder /usr/sbin/xinetd /usr/sbin/xinetd
RUN mkdir -p /etc/xinetd.d/

RUN pip --no-cache install pycryptodome

COPY --chmod=755 init.sh app.py /
COPY xinetd.conf /etc/xinetd.conf

CMD ["xinetd", "-stayalive", "-dontfork"]
