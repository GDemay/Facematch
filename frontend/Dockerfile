# Use an official node runtime as a parent image
FROM node:16-alpine

# Set the working directory in the container
WORKDIR /usr/src/app

# Install dependencies
COPY package*.json ./
RUN npm install

# Create .eslintcache file with correct permissions
RUN mkdir -p /usr/src/app/.eslintcache && \
    touch /usr/src/app/.eslintcache && \
    chmod 777 /usr/src/app/.eslintcache

# Copy the rest of the application's code
COPY . .

# Change ownership of the app directory to the node user
RUN chown -R node:node /usr/src/app

# Switch to the node user
USER node

# Expose the port the app runs on
EXPOSE 3000

# Command to run the application
CMD ["npm", "start"]