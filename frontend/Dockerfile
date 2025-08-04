# Use an official lightweight Node.js image
FROM node:18-alpine

# Set working directory inside container
WORKDIR /app

# Copy package definition files
COPY package.json ./

# Install dependencies
RUN npm install

# Copy the rest of the app source code
COPY . .

# Expose the Vite dev server port
EXPOSE 5173

# Start Vite dev server
CMD ["npm", "run", "dev"]