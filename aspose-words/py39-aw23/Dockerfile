FROM python:3.9-bullseye

ENV FROM_EXT=pdf
ENV TO_EXT=md

COPY tuna.sources.list /etc/apt/sources.list
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# RUN wget https://dot.net/v1/dotnet-install.sh -O /tmp/dotnet-install.sh && \
#   chmod +x /tmp/dotnet-install.sh && \
#   /tmp/dotnet-install.sh --version latest --runtime aspnetcore && \
#   rm /tmp/dotnet-install.sh

RUN apt-get update -y
RUN apt-get install -y build-essential libpython3.9 pkg-config libicu-dev

RUN pip install "aspose-words>=23.0.0,<24.0.0" natsort

VOLUME [ "/workspace" ]

WORKDIR /workspace

COPY run.py /run.py

CMD [ "python", "/run.py" ]
