FROM ubuntu:20.04

ENV TO_EXT=md

RUN apt update -y && apt install -y ca-certificates
COPY tuna.sources.list /etc/apt/sources.list

RUN apt-get update -y
RUN DEBIAN_FRONTEND=noninteractive \
  TZ=Asia/Shanghai \
  apt-get install -y openjdk-11-jre python3 python3-pip

RUN pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

RUN pip3 install \
  natsort \
  "aspose-words>=23.0.0,<24.0.0" \
  "aspose-cells>=23.0.0,<24.0.0" \
  "Aspose.Slides>=23.0.0,<24.0.0"

VOLUME [ "/workspace" ]

WORKDIR /workspace

COPY run.py /run.py

CMD [ "python3", "/run.py" ]
