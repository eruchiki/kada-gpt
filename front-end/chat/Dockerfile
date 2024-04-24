FROM node:20.12.2

WORKDIR /src

COPY package.json ./
RUN yarn install

EXPOSE 3000
CMD ["next", "start"]
