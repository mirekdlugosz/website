FROM node:lts-alpine as theme
WORKDIR /var/www/pelican-theme
COPY theme/ ./
RUN npm install && npx gulp

FROM python:3-alpine
EXPOSE 8000
RUN apk add --update git make
WORKDIR /var/www/
RUN git clone --recursive https://github.com/getpelican/pelican-plugins
WORKDIR /var/www/pelican
COPY . ./
COPY --from=theme /var/www/pelican-theme/static/ ./theme/static/
RUN pip install -r requirements.txt
ENTRYPOINT ["make"]
