FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

# Build for production
RUN npm run build

# Install serve to run the application
RUN npm install -g serve

CMD ["serve", "-s", "dist", "-l", "5173"]
