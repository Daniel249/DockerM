# Moodle Docker Tests

This directory contains unit tests for the Moodle Docker setup.

## Test Files

- **test_database_connection.py** - Tests for MariaDB database connectivity, charset, and user configuration
- **test_web_container.py** - Tests for Apache/PHP web server configuration and extensions
- **test_moodle_installation.py** - Tests for Moodle application files and installation
- **test_docker_compose.py** - Tests for Docker Compose configuration
- **test_volumes.py** - Tests for Docker volumes and data persistence

## Prerequisites

```bash
pip install -r requirements.txt
```

## Running Tests

### Run all tests:
```bash
python -m unittest discover tests
```

### Run a specific test file:
```bash
python -m unittest tests.test_database_connection
```

### Run a specific test class:
```bash
python -m unittest tests.test_web_container.TestWebContainer
```

### Run a specific test:
```bash
python -m unittest tests.test_moodle_installation.TestMoodleInstallation.test_moodle_accessible
```

## Before Running Tests

1. Start the containers:
   ```bash
   docker-compose up -d
   ```

2. Wait for containers to be fully running (especially for PHP extension installation)

3. Run the tests

## Notes

- Some tests require containers to be running (`docker-compose up -d`)
- Some tests will be skipped if Moodle installation hasn't been completed via web interface
- Integration tests may require additional setup

## Test Coverage

- ✅ Database container status
- ✅ Database UTF-8 configuration
- ✅ Web server accessibility
- ✅ PHP version and extensions
- ✅ File permissions
- ✅ Docker Compose configuration
- ✅ Volume mappings
- ✅ Moodle files installation
