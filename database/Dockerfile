FROM flyway/flyway:latest

# Set working directory
WORKDIR /flyway

# Copy migration scripts
COPY ./database/flyway/sql ./sql

# Default command to run migrations
CMD [ "migrate" ]