PROJECT_NAME := scraper
BUILD_DIR := ./out
SOURCE_DIR := ./cmd/$(PROJECT_NAME)

# Default target
all: build

# Ensure BUILD_DIR exists
$(BUILD_DIR):
	@mkdir -p $(BUILD_DIR)

# Build the project
build: $(BUILD_DIR)
	@echo "Building..."
	@cd scraper && go build -o ../$(BUILD_DIR)/$(PROJECT_NAME) $(SOURCE_DIR)

# Run the project
run: build
	@echo "Running..."
	@./out/$(PROJECT_NAME)

# Run tests
test:
	@echo "Testing..."
	@cd scraper && go run gotest.tools/gotestsum@latest -- -v ./...

# Clean up build artifacts
clean:
	@echo "Cleaning..."
	@rm -rf out

# Phony targets ensure that make doesn't get confused by files with the same name as the target.
.PHONY: all build run test clean
