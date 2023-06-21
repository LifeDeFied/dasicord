FROM golang:1.16-alpine as builder

# Set working directory
WORKDIR /app

# Copy source code to container
COPY . .

# Build the application
RUN go build -o /app/newchain ./cmd/newchain

# Create a new container from scratch
FROM alpine:latest

# Set working directory
WORKDIR /app

# Copy the binary from the builder container
COPY --from=builder /app/newchain .

# Expose ports
EXPOSE 26657 1317 4500

# Run the binary
CMD ["./newchain"]
