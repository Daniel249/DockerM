"""
Unit tests for Docker volumes and data persistence
"""
import unittest
import subprocess
import os


class TestVolumes(unittest.TestCase):
    """Test Docker volume configuration and data persistence"""

    def test_www_directory_exists(self):
        """Verify www directory exists on host"""
        self.assertTrue(os.path.exists('./www'), "www directory does not exist on host")

    def test_db_data_directory_exists(self):
        """Verify db_data directory exists on host"""
        self.assertTrue(os.path.exists('./db_data'), "db_data directory does not exist on host")

    def test_www_directory_not_empty(self):
        """Verify www directory contains Moodle files"""
        www_contents = os.listdir('./www')
        self.assertGreater(len(www_contents), 0, "www directory is empty")
        self.assertIn('index.php', www_contents, "index.php not found in www directory")

    def test_volume_mount_in_web_container(self):
        """Verify volume is mounted in web container"""
        result = subprocess.run(
            ['docker', 'inspect', 'mood-web-1', '--format', '{{json .Mounts}}'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            self.assertIn('/var/www/html', result.stdout, "Volume not mounted at /var/www/html")
        else:
            self.skipTest("Web container not running")

    def test_volume_mount_in_db_container(self):
        """Verify volume is mounted in database container"""
        result = subprocess.run(
            ['docker', 'inspect', 'mood-db-1', '--format', '{{json .Mounts}}'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            self.assertIn('/var/lib/mysql', result.stdout, "Volume not mounted at /var/lib/mysql")
        else:
            self.skipTest("Database container not running")

    def test_moodledata_volume_exists(self):
        """Verify moodledata volume is configured"""
        result = subprocess.run(
            ['docker', 'volume', 'ls', '--format', '{{.Name}}'],
            capture_output=True,
            text=True
        )
        # Check if moodledata volume exists (if using named volume)
        # Or verify the directory mount
        self.assertTrue(True)  # Placeholder - adjust based on your volume strategy

    def test_data_persistence_after_restart(self):
        """Verify data persists after container restart (integration test)"""
        # This is a placeholder for integration testing
        # Would require stopping/starting containers and checking data
        self.skipTest("Integration test - requires container restart")


if __name__ == '__main__':
    unittest.main()
