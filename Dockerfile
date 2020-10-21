FROM node:12-buster-slim
EXPOSE 8000
RUN apt-get update \
	&& apt-get install -y ca-certificates git make python3 python3-pip python3-setuptools python3-wheel --no-install-recommends \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /var/www/
RUN git clone --depth 1 --recursive https://github.com/getpelican/pelican-plugins

WORKDIR /var/www/pelican/
COPY . ./

RUN cd theme && npm install
RUN pip3 install -r requirements.txt
RUN make theme

ENTRYPOINT ["make"]
