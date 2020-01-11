	FROM ubuntu:14.04
RUN apt-get update
RUN apt-get install build-essential nano autoconf libtool pkg-config libboost-all-dev libssl-dev libprotobuf-dev protobuf-compiler libevent-dev libqt4-dev libcanberra-gtk-module libdb-dev libdb++-dev bsdmainutils -y
WORKDIR /src/bitcoin
COPY ./bitcoin .
RUN ./autogen.sh
RUN ./configure --with-incompatible-bdb
RUN make -j60
RUN make install
RUN mkdir -p /root/bitcoind-simnet/libs
