FROM node:12-buster-slim
EXPOSE 8000
ENV PATH="${HOME}/.local/bin/:${PATH}"
RUN apt-get update \
	&& apt-get install -y ca-certificates python3 python3-pip python3-setuptools python3-wheel --no-install-recommends \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/* \
	&& pip3 install --user --upgrade pip

WORKDIR /var/www/pelican/
COPY . ./

RUN cd theme && npm install
RUN python3 -m pip install -r requirements.txt

ENTRYPOINT ["invoke"]
