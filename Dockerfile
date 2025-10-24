# Use official lightweight Node.js base image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package definitions and install dependencies
COPY package*.json ./
RUN npm install --production

# Copy all framework files
COPY . .

# Expose app port
EXPOSE 3000

# Start command
CMD ["npm", "start"]
