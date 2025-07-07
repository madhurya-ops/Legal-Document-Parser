# Build stage
FROM node:20-alpine AS build

WORKDIR /app

# Copy package files and install dependencies
COPY package.json package-lock.json* ./
RUN npm install --legacy-peer-deps --silent

# Copy source code
COPY . .

# Set build arguments and environment variables
ARG REACT_APP_API_URL
ARG REACT_APP_NAME
ARG REACT_APP_VERSION
ARG REACT_APP_DESCRIPTION
ARG GENERATE_SOURCEMAP
ARG REACT_APP_DEBUG
ARG REACT_APP_ENABLE_LAZY_LOADING
ARG REACT_APP_CACHE_DURATION
ARG REACT_APP_ENABLE_CHAT_HISTORY
ARG REACT_APP_ENABLE_DOCUMENT_EXPORT
ARG REACT_APP_ENABLE_ADMIN_PANEL

ENV REACT_APP_API_URL=$REACT_APP_API_URL
ENV REACT_APP_NAME=$REACT_APP_NAME
ENV REACT_APP_VERSION=$REACT_APP_VERSION
ENV REACT_APP_DESCRIPTION=$REACT_APP_DESCRIPTION
ENV GENERATE_SOURCEMAP=$GENERATE_SOURCEMAP
ENV REACT_APP_DEBUG=$REACT_APP_DEBUG
ENV REACT_APP_ENABLE_LAZY_LOADING=$REACT_APP_ENABLE_LAZY_LOADING
ENV REACT_APP_CACHE_DURATION=$REACT_APP_CACHE_DURATION
ENV REACT_APP_ENABLE_CHAT_HISTORY=$REACT_APP_ENABLE_CHAT_HISTORY
ENV REACT_APP_ENABLE_DOCUMENT_EXPORT=$REACT_APP_ENABLE_DOCUMENT_EXPORT
ENV REACT_APP_ENABLE_ADMIN_PANEL=$REACT_APP_ENABLE_ADMIN_PANEL

# Build the application
RUN npm run build

# Production stage (serving static files with Nginx)
FROM nginx:alpine

# Install curl for health checks
RUN apk add --no-cache curl

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Copy built application
COPY --from=build /app/build /usr/share/nginx/html

# Create nginx cache directory
RUN mkdir -p /var/cache/nginx

# Set proper permissions
RUN chown -R nginx:nginx /var/cache/nginx && \
    chown -R nginx:nginx /usr/share/nginx/html && \
    chmod -R 755 /usr/share/nginx/html

EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
