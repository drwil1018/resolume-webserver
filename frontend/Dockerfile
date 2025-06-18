# Build stage
FROM node:20-alpine as build

# Accept API URL as build argument
ARG API_URL

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy the rest of the code
COPY . .

# Create env file with dynamic API URL at build time
RUN echo "VITE_API_URL=${API_URL}" > .env.production

# Build the app (production build)
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy the build output to replace the default nginx contents
COPY --from=build /app/dist /usr/share/nginx/html

# Copy the entrypoint script and make it executable
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Copy a custom nginx config if needed for SPA routing
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Use entrypoint script to set runtime configuration
# Expose port 80
EXPOSE 80

# Set entrypoint script and start nginx
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]
