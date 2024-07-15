# Use an official node runtime as a parent image
FROM node:16-alpine

# Set the working directory in the container
WORKDIR /usr/src/app

COPY --chown=node:node package.json .

# Install dependencies
COPY package*.json ./


RUN npm install

COPY --chown=node:node . .

USER node

# Copy the rest of the application's code
COPY . .

# Expose the port the app runs on
EXPOSE 3000

# Command to run the application
CMD ["npm", "start"]
