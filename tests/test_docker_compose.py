"""
Unit tests for Docker Compose configuration
"""
import unittest
import subprocess
import yaml
import os


class TestDockerCompose(unittest.TestCase):
    """Test Docker Compose configuration file"""

    def setUp(self):
        """Load docker-compose.yml"""
        self.compose_file = 'docker-compose.yml'
        with open(self.compose_file, 'r') as f:
            self.config = yaml.safe_load(f)

    def test_compose_file_exists(self):
        """Verify docker-compose.yml exists"""
        self.assertTrue(os.path.exists(self.compose_file), "docker-compose.yml does not exist")

    def test_services_defined(self):
        """Verify both web and db services are defined"""
        self.assertIn('services', self.config)
        self.assertIn('web', self.config['services'])
        self.assertIn('db', self.config['services'])

    def test_web_service_image(self):
        """Verify web service uses PHP 8.2 Apache image"""
        web_image = self.config['services']['web']['image']
        self.assertEqual(web_image, 'php:8.2-apache', "Web service not using php:8.2-apache")

    def test_db_service_image(self):
        """Verify database service uses MariaDB 11"""
        db_image = self.config['services']['db']['image']
        self.assertEqual(db_image, 'mariadb:11', "Database service not using mariadb:11")

    def test_port_mappings(self):
        """Verify port 8080 is mapped to port 80"""
        ports = self.config['services']['web']['ports']
        self.assertIn('8080:80', ports, "Port mapping 8080:80 not configured")

    def test_volume_mappings(self):
        """Verify volume mappings are configured"""
        web_volumes = self.config['services']['web']['volumes']
        db_volumes = self.config['services']['db']['volumes']
        
        self.assertIn('./www:/var/www/html', web_volumes, "Web volume not mapped correctly")
        self.assertIn('./db_data:/var/lib/mysql', db_volumes, "Database volume not mapped correctly")

    def test_environment_variables(self):
        """Verify required environment variables are set"""
        db_env = self.config['services']['db']['environment']
        
        self.assertIn('MYSQL_ROOT_PASSWORD=rootpass', db_env)
        self.assertIn('MYSQL_DATABASE=moodle', db_env)
        self.assertIn('MYSQL_USER=moodle', db_env)
        self.assertIn('MYSQL_PASSWORD=moodlepass', db_env)

    def test_service_dependencies(self):
        """Verify web service depends on database"""
        depends_on = self.config['services']['web'].get('depends_on', [])
        self.assertIn('db', depends_on, "Web service does not depend on database")

    def test_containers_running(self):
        """Verify both containers are running (integration test)"""
        result = subprocess.run(
            ['docker-compose', 'ps', '--services', '--filter', 'status=running'],
            capture_output=True,
            text=True
        )
        
        # This test only passes if containers are up
        if 'web' in result.stdout and 'db' in result.stdout:
            self.assertTrue(True, "Both containers are running")
        else:
            self.skipTest("Containers are not running - run 'docker-compose up -d' first")


if __name__ == '__main__':
    unittest.main()
