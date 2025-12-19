FROM ghcr.io/cirruslabs/flutter:stable AS build

WORKDIR /app

COPY pubspec.yaml pubspec.lock* ./
RUN flutter pub get

COPY . .

ARG BACKEND_BASE_URL
RUN flutter pub get
RUN flutter build web --release --base-href / \
  --dart-define=BACKEND_BASE_URL=${BACKEND_BASE_URL}

FROM nginx:alpine

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf.template /etc/nginx/templates/default.conf.template
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

COPY --from=build /app/build/web /usr/share/nginx/html


EXPOSE 8080

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]
