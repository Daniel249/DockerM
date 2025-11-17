"""
Unit tests for database connection and configuration
"""
import unittest
import subprocess
import json


class TestDatabaseConnection(unittest.TestCase):
    """Test database connectivity and configuration"""

    def test_database_container_running(self):
        """Verify the database container is running"""
        result = subprocess.run(
            ['docker', 'ps', '--filter', 'name=mood-db', '--format', '{{.Status}}'],
            capture_output=True,
            text=True
        )
        self.assertIn('Up', result.stdout, "Database container is not running")

    def test_database_port_exposed(self):
        """Verify database port 3306 is accessible internally"""
        result = subprocess.run(
            ['docker', 'inspect', 'mood-db-1'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            ports = data[0]['Config']['ExposedPorts']
            self.assertIn('3306/tcp', ports, "Database port 3306 not exposed")

    def test_database_charset_configuration(self):
        """Verify database is configured with UTF-8"""
        result = subprocess.run(
            ['docker', 'exec', 'mood-db-1', 'mysql', '-u', 'root', '-prootpass',
             '-e', 'SHOW VARIABLES LIKE "character_set_server"'],
            capture_output=True,
            text=True
        )
        self.assertIn('utf8mb4', result.stdout, "Database not configured with utf8mb4")

    def test_moodle_database_exists(self):
        """Verify the Moodle database exists"""
        result = subprocess.run(
            ['docker', 'exec', 'mood-db-1', 'mysql', '-u', 'root', '-prootpass',
             '-e', 'SHOW DATABASES LIKE "moodle"'],
            capture_output=True,
            text=True
        )
        self.assertIn('moodle', result.stdout, "Moodle database does not exist")

    def test_moodle_user_exists(self):
        """Verify the Moodle database user exists"""
        result = subprocess.run(
            ['docker', 'exec', 'mood-db-1', 'mysql', '-u', 'root', '-prootpass',
             '-e', "SELECT User FROM mysql.user WHERE User='moodle'"],
            capture_output=True,
            text=True
        )
        self.assertIn('moodle', result.stdout, "Moodle database user does not exist")


if __name__ == '__main__':
    unittest.main()
