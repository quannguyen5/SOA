FROM node:18-alpine as build

WORKDIR /app

# Copy package.json và package-lock.json
COPY package*.json ./

# Cài đặt dependencies
RUN npm install

# Copy source code
COPY . .

# Tạo file .env với biến môi trường
RUN echo "VITE_BE_URL=${VITE_BE_URL:-http://localhost:3000}" > .env

# Start development server
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]