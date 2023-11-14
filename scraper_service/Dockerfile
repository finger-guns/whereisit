# Use an official Golang runtime as a parent image
FROM golang:1.21.3-alpine as builder

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./scraper/ /app

# Download the dependencies
RUN go mod download

# Install air for hot reloading
RUN go install github.com/cosmtrek/air@latest

# The command to run when this image starts up
CMD ["air"]
