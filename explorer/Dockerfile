FROM node:10-alpine as builder

COPY "./" "/build"
RUN { \
         rm -rf /build/node_modules/ ; \
         cd /build ; \
         npm i && npm run build ; \
#         npm start ; \
     }

#WORKDIR "/build"
#CMD "npm start"

#RUN npm run ng build -- --prod --output-path=dist


## STAGE 2: Setup ###

FROM nginx:1.14.1-alpine

## Copy our default nginx config
COPY ./default.conf /etc/nginx/conf.d/

## Remove default nginx website
RUN rm -rf /usr/share/nginx/html/*

## From ‘builder’ stage copy over the artifacts in dist folder to default nginx public folder
COPY --from=builder /build/www /usr/share/nginx/html

CMD ["nginx", "-g", "daemon off;"]
