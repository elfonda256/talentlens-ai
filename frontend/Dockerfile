FROM node:22-alpine
WORKDIR /srv
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
# BACKEND_URL and BACKEND_API_KEY are read at runtime by the server-side relay, never at build.
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
