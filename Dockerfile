FROM rust:latest

WORKDIR /l3x

COPY . .

RUN cargo build --release
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install requests

ENTRYPOINT ["/l3x/entrypoint.sh"]
