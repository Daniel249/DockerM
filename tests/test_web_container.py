"""
Unit tests for web container and Apache/PHP configuration
"""
import unittest
import subprocess
import requests
import json


class TestWebContainer(unittest.TestCase):
    """Test web server container and PHP configuration"""

    def test_web_container_running(self):
        """Verify the web container is running"""
        result = subprocess.run(
            ['docker', 'ps', '--filter', 'name=mood-web', '--format', '{{.Status}}'],
            capture_output=True,
            text=True
        )
        self.assertIn('Up', result.stdout, "Web container is not running")

    def test_apache_responding(self):
        """Verify Apache is responding on port 8080"""
        try:
            response = requests.get('http://localhost:8080', timeout=5)
            self.assertEqual(response.status_code, 200, "Apache not responding with 200 OK")
        except requests.exceptions.RequestException as e:
            self.fail(f"Apache is not accessible: {e}")

    def test_php_version(self):
        """Verify PHP 8.2 is installed"""
        result = subprocess.run(
            ['docker', 'exec', 'mood-web-1', 'php', '-v'],
            capture_output=True,
            text=True
        )
        self.assertIn('PHP 8.2', result.stdout, "PHP 8.2 not installed")

    def test_php_extensions_installed(self):
        """Verify required PHP extensions are installed"""
        required_extensions = ['mysqli', 'pdo_mysql', 'gd', 'zip', 'intl', 'soap', 'opcache', 'exif']
        
        result = subprocess.run(
            ['docker', 'exec', 'mood-web-1', 'php', '-m'],
            capture_output=True,
            text=True
        )
        
        for ext in required_extensions:
            self.assertIn(ext, result.stdout, f"PHP extension '{ext}' not installed")

    def test_www_directory_permissions(self):
        """Verify /var/www/html has correct permissions"""
        result = subprocess.run(
            ['docker', 'exec', 'mood-web-1', 'stat', '-c', '%a', '/var/www/html'],
            capture_output=True,
            text=True
        )
        permissions = result.stdout.strip()
        self.assertEqual(permissions, '775', f"Incorrect permissions on /var/www/html: {permissions}")

    def test_moodledata_directory_exists(self):
        """Verify Moodle data directory exists"""
        result = subprocess.run(
            ['docker', 'exec', 'mood-web-1', 'test', '-d', '/var/moodledata'],
            capture_output=True
        )
        self.assertEqual(result.returncode, 0, "/var/moodledata directory does not exist")

    def test_port_mapping(self):
        """Verify port 8080 is mapped correctly"""
        result = subprocess.run(
            ['docker', 'port', 'mood-web-1'],
            capture_output=True,
            text=True
        )
        self.assertIn('0.0.0.0:8080->80/tcp', result.stdout, "Port mapping 8080:80 not configured")


if __name__ == '__main__':
    unittest.main()
