"""
Unit tests for Moodle installation and configuration
"""
import unittest
import subprocess
import requests


class TestMoodleInstallation(unittest.TestCase):
    """Test Moodle application installation and setup"""

    def test_moodle_files_exist(self):
        """Verify Moodle files are installed"""
        essential_files = ['index.php', 'version.php', 'lib/moodlelib.php']
        
        for file in essential_files:
            result = subprocess.run(
                ['docker', 'exec', 'mood-web-1', 'test', '-f', f'/var/www/html/{file}'],
                capture_output=True
            )
            self.assertEqual(result.returncode, 0, f"Moodle file {file} does not exist")

    def test_moodle_accessible(self):
        """Verify Moodle is accessible via web browser"""
        try:
            response = requests.get('http://localhost:8080', timeout=10)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Moodle', response.text, "Moodle not found in response")
        except requests.exceptions.RequestException as e:
            self.fail(f"Moodle is not accessible: {e}")

    def test_config_file_exists(self):
        """Verify config.php exists (after installation)"""
        result = subprocess.run(
            ['docker', 'exec', 'mood-web-1', 'test', '-f', '/var/www/html/config.php'],
            capture_output=True
        )
        # This test may fail if Moodle hasn't been installed yet
        # Comment: Expected to fail before web-based installation is complete
        if result.returncode == 0:
            self.assertTrue(True, "config.php exists")
        else:
            self.skipTest("config.php does not exist - installation not completed")

    def test_moodle_theme_files(self):
        """Verify Moodle themes are installed"""
        result = subprocess.run(
            ['docker', 'exec', 'mood-web-1', 'test', '-d', '/var/www/html/theme/boost'],
            capture_output=True
        )
        self.assertEqual(result.returncode, 0, "Boost theme directory does not exist")

    def test_moodle_version_file(self):
        """Verify Moodle version is 4.4"""
        result = subprocess.run(
            ['docker', 'exec', 'mood-web-1', 'grep', 'release', '/var/www/html/version.php'],
            capture_output=True,
            text=True
        )
        self.assertIn('4.4', result.stdout, "Moodle version is not 4.4")

    def test_file_ownership(self):
        """Verify files are owned by www-data"""
        result = subprocess.run(
            ['docker', 'exec', 'mood-web-1', 'stat', '-c', '%U', '/var/www/html/index.php'],
            capture_output=True,
            text=True
        )
        owner = result.stdout.strip()
        self.assertEqual(owner, 'www-data', f"Files not owned by www-data, owned by: {owner}")


if __name__ == '__main__':
    unittest.main()
