# Busca a ultima versao estável e minimizada do node
FROM node:alpine
WORKDIR /usr/app

COPY package*.json ./
RUN npm install

COPY ..

EXPOSE 3000

CMD ["npm" , "start"]