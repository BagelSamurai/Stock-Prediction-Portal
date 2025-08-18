FROM node:20-alpine as builder

WORKDIR /app

COPY package*.json ./

RUN npm install

copy . .

RUN npm run build

FROM nginx:1.27-alpine

COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]