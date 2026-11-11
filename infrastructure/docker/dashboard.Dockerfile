FROM node:20-alpine

WORKDIR /app

COPY apps/dashboard/package.json ./package.json
RUN npm install

COPY apps/dashboard ./

EXPOSE 3000

CMD ["npm", "run", "dev"]

