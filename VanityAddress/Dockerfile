FROM alpine:3.18

# Installazione delle dipendenze necessarie
RUN apk add --no-cache \
    build-base \
    cmake \
    openssl-dev \
    linux-headers

# Creazione della directory di lavoro
WORKDIR /app

# Copia dei file necessari per la compilazione
COPY CMakeLists.txt /app/
COPY vanity.cpp /app/

# Compilazione del programma
RUN mkdir -p build && cd build && \
    cmake .. && \
    cmake --build . --config Release

CMD ["/app/build/vanity"]