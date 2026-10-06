FROM golang:1.21-alpine AS builder
RUN apk add --no-cache git build-essential
RUN git clone https://github.com/build
WORKDIR /build
RUN go build

FROM alpine:latest
WORKDIR /app
COPY --from=builder /build/packetcrypt /app/packetcrypt
CMD ["./packetcrypt", "ann", "http://pool.io", "--paymentAddress", "0x0130D5fb99cb4A39bAA527898A19e82dD86741b1"]
