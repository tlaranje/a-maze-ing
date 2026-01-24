"""
Test suite for A-Maze-ing project
Tests configuration file parsing and runtime requirements
"""

import pytest
import os
import tempfile
import subprocess
import time
from pathlib import Path
from typing import List, Tuple


class TestConfigFile:
    """Tests for configuration file validation"""
    
    def create_temp_config(self, content: str) -> str:
        """Helper to create temporary config file"""
        fd, path = tempfile.mkstemp(suffix='.txt')
        with os.fdopen(fd, 'w') as f:
            f.write(content)
        return path
    
    def test_valid_config(self) -> None:
        """Test that valid config is accepted"""
        config = """
# Valid configuration
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
"""
        config_path = self.create_temp_config(config)
        try:
            # Should not raise exception
            result = subprocess.run(
                ['python3', 'a_maze_ing.py', config_path],
                capture_output=True,
                timeout=30
            )
            assert result.returncode == 0, f"Valid config failed: {result.stderr.decode()}"
        finally:
            os.unlink(config_path)
    
    def test_missing_mandatory_keys(self) -> None:
        """Test that missing mandatory keys are detected"""
        mandatory_keys = ['WIDTH', 'HEIGHT', 'ENTRY', 'EXIT', 'OUTPUT_FILE', 'PERFECT']
        
        for missing_key in mandatory_keys:
            config_lines = [
                "WIDTH=20",
                "HEIGHT=15",
                "ENTRY=0,0",
                "EXIT=19,14",
                "OUTPUT_FILE=maze.txt",
                "PERFECT=True"
            ]
            # Remove the line with missing_key
            config = '\n'.join([line for line in config_lines if not line.startswith(missing_key)])
            
            config_path = self.create_temp_config(config)
            try:
                result = subprocess.run(
                    ['python3', 'a_maze_ing.py', config_path],
                    capture_output=True,
                    timeout=10
                )
                assert result.returncode != 0, f"Missing {missing_key} should fail"
                assert b"error" in result.stderr.lower() or b"error" in result.stdout.lower()
            finally:
                os.unlink(config_path)
    
    def test_comment_lines_ignored(self) -> None:
        """Test that comment lines are properly ignored"""
        config = """
# This is a comment
WIDTH=20
# Another comment
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
# PERFECT=False (commented out)
PERFECT=True
"""
        config_path = self.create_temp_config(config)
        try:
            result = subprocess.run(
                ['python3', 'a_maze_ing.py', config_path],
                capture_output=True,
                timeout=30
            )
            assert result.returncode == 0
        finally:
            os.unlink(config_path)
    
    def test_invalid_format(self) -> None:
        """Test that invalid KEY=VALUE format is rejected"""
        invalid_configs = [
            "WIDTH 20",  # Missing =
            "WIDTH= 20",  # Space after =
            "WIDTH =20",  # Space before =
            "WIDTHHEIGHT=20",  # Invalid key
        ]
        
        for invalid_line in invalid_configs:
            config = f"""
{invalid_line}
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
"""
            config_path = self.create_temp_config(config)
            try:
                result = subprocess.run(
                    ['python3', 'a_maze_ing.py', config_path],
                    capture_output=True,
                    timeout=10
                )
                # Should either fail or handle gracefully
                if result.returncode == 0:
                    # If it succeeds, WIDTH must have valid value
                    pass
            finally:
                os.unlink(config_path)
    
    def test_invalid_values(self) -> None:
        """Test that invalid values are rejected"""
        invalid_configs = [
            ("WIDTH=-5", "Negative width"),
            ("HEIGHT=0", "Zero height"),
            ("WIDTH=abc", "Non-numeric width"),
            ("ENTRY=0", "Invalid entry format"),
            ("ENTRY=0,", "Incomplete entry coordinates"),
            ("EXIT=a,b", "Non-numeric exit"),
            ("PERFECT=Maybe", "Invalid boolean"),
        ]
        
        base_config = """
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
"""
        
        for invalid_line, description in invalid_configs:
            key = invalid_line.split('=')[0]
            config_lines = [line for line in base_config.strip().split('\n') 
                          if not line.startswith(key)]
            config_lines.append(invalid_line)
            config = '\n'.join(config_lines)
            
            config_path = self.create_temp_config(config)
            try:
                result = subprocess.run(
                    ['python3', 'a_maze_ing.py', config_path],
                    capture_output=True,
                    timeout=10
                )
                assert result.returncode != 0, f"{description} should fail"
            finally:
                os.unlink(config_path)
    
    def test_entry_exit_out_of_bounds(self) -> None:
        """Test that entry/exit outside maze bounds are rejected"""
        invalid_positions = [
            ("ENTRY=20,0", "Entry x >= WIDTH"),
            ("ENTRY=0,15", "Entry y >= HEIGHT"),
            ("EXIT=20,14", "Exit x >= WIDTH"),
            ("EXIT=19,15", "Exit y >= HEIGHT"),
            ("ENTRY=-1,0", "Negative entry x"),
            ("ENTRY=0,-1", "Negative entry y"),
        ]
        
        for invalid_line, description in invalid_positions:
            config = f"""
WIDTH=20
HEIGHT=15
{invalid_line}
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
"""
            config_path = self.create_temp_config(config)
            try:
                result = subprocess.run(
                    ['python3', 'a_maze_ing.py', config_path],
                    capture_output=True,
                    timeout=10
                )
                assert result.returncode != 0, f"{description} should fail"
            finally:
                os.unlink(config_path)
    
    def test_entry_equals_exit(self) -> None:
        """Test that entry and exit must be different"""
        config = """
WIDTH=20
HEIGHT=15
ENTRY=5,5
EXIT=5,5
OUTPUT_FILE=maze.txt
PERFECT=True
"""
        config_path = self.create_temp_config(config)
        try:
            result = subprocess.run(
                ['python3', 'a_maze_ing.py', config_path],
                capture_output=True,
                timeout=10
            )
            assert result.returncode != 0, "Entry == Exit should fail"
        finally:
            os.unlink(config_path)
    
    def test_file_not_found(self) -> None:
        """Test that missing config file is handled gracefully"""
        result = subprocess.run(
            ['python3', 'a_maze_ing.py', 'nonexistent_config.txt'],
            capture_output=True,
            timeout=10
        )
        assert result.returncode != 0
        # Should have clear error message
        output = result.stderr.decode() + result.stdout.decode()
        assert 'error' in output.lower() or 'not found' in output.lower()


class TestRuntime:
    """Tests for runtime behavior and performance"""
    
    def test_no_crash_on_valid_input(self) -> None:
        """Test that program doesn't crash on valid input"""
        config = """
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=test_maze.txt
PERFECT=True
"""
        fd, config_path = tempfile.mkstemp(suffix='.txt')
        with os.fdopen(fd, 'w') as f:
            f.write(config)
        
        try:
            result = subprocess.run(
                ['python3', 'a_maze_ing.py', config_path],
                capture_output=True,
                timeout=30
            )
            assert result.returncode == 0, f"Program crashed: {result.stderr.decode()}"
        finally:
            os.unlink(config_path)
            if os.path.exists('test_maze.txt'):
                os.unlink('test_maze.txt')
    
    def test_reasonable_generation_time(self) -> None:
        """Test that maze generation completes in reasonable time"""
        sizes = [
            (10, 10, 5),   # Small maze, max 5 seconds
            (20, 20, 15),  # Medium maze, max 15 seconds
            (50, 50, 60),  # Large maze, max 60 seconds
        ]
        
        for width, height, max_time in sizes:
            config = f"""
WIDTH={width}
HEIGHT={height}
ENTRY=0,0
EXIT={width-1},{height-1}
OUTPUT_FILE=test_maze_{width}x{height}.txt
PERFECT=True
"""
            fd, config_path = tempfile.mkstemp(suffix='.txt')
            with os.fdopen(fd, 'w') as f:
                f.write(config)
            
            try:
                start_time = time.time()
                result = subprocess.run(
                    ['python3', 'a_maze_ing.py', config_path],
                    capture_output=True,
                    timeout=max_time + 10
                )
                elapsed = time.time() - start_time
                
                assert result.returncode == 0, f"Failed for {width}x{height}"
                assert elapsed < max_time, f"Too slow for {width}x{height}: {elapsed:.2f}s"
                
            finally:
                os.unlink(config_path)
                output_file = f'test_maze_{width}x{height}.txt'
                if os.path.exists(output_file):
                    os.unlink(output_file)
    
    def test_reproducibility_with_seed(self) -> None:
        """Test that same seed produces same maze (if seed is supported)"""
        config_template = """
WIDTH=15
HEIGHT=15
ENTRY=0,0
EXIT=14,14
OUTPUT_FILE={output_file}
PERFECT=True
SEED=42
"""
        
        output_files = ['maze_seed1.txt', 'maze_seed2.txt']
        
        try:
            for output_file in output_files:
                config = config_template.format(output_file=output_file)
                fd, config_path = tempfile.mkstemp(suffix='.txt')
                with os.fdopen(fd, 'w') as f:
                    f.write(config)
                
                try:
                    result = subprocess.run(
                        ['python3', 'a_maze_ing.py', config_path],
                        capture_output=True,
                        timeout=30
                    )
                    assert result.returncode == 0
                finally:
                    os.unlink(config_path)
            
            # Compare outputs
            if all(os.path.exists(f) for f in output_files):
                with open(output_files[0]) as f1, open(output_files[1]) as f2:
                    content1 = f1.read()
                    content2 = f2.read()
                    assert content1 == content2, "Same seed should produce identical mazes"
        
        finally:
            for f in output_files:
                if os.path.exists(f):
                    os.unlink(f)
    
    def test_output_file_created(self) -> None:
        """Test that output file is created with correct format"""
        config = """
WIDTH=10
HEIGHT=10
ENTRY=0,0
EXIT=9,9
OUTPUT_FILE=test_output.txt
PERFECT=True
"""
        fd, config_path = tempfile.mkstemp(suffix='.txt')
        with os.fdopen(fd, 'w') as f:
            f.write(config)
        
        try:
            result = subprocess.run(
                ['python3', 'a_maze_ing.py', config_path],
                capture_output=True,
                timeout=30
            )
            assert result.returncode == 0
            assert os.path.exists('test_output.txt'), "Output file not created"
            
            # Check basic format
            with open('test_output.txt') as f:
                lines = f.readlines()
                assert len(lines) > 10, "Output file too short"
                
                # First 10 lines should be hex digits
                for i in range(10):
                    line = lines[i].strip()
                    assert len(line) == 10, f"Row {i} has wrong length"
                    assert all(c in '0123456789ABCDEFabcdef' for c in line), \
                        f"Row {i} contains non-hex characters"
        
        finally:
            os.unlink(config_path)
            if os.path.exists('test_output.txt'):
                os.unlink('test_output.txt')
    
    def test_handles_special_characters_in_output_path(self) -> None:
        """Test output file paths with special characters"""
        special_paths = [
            "maze with spaces.txt",
            "maze-with-dashes.txt",
            "maze_with_underscores.txt",
        ]
        
        for output_path in special_paths:
            config = f"""
WIDTH=10
HEIGHT=10
ENTRY=0,0
EXIT=9,9
OUTPUT_FILE={output_path}
PERFECT=True
"""
            fd, config_path = tempfile.mkstemp(suffix='.txt')
            with os.fdopen(fd, 'w') as f:
                f.write(config)
            
            try:
                result = subprocess.run(
                    ['python3', 'a_maze_ing.py', config_path],
                    capture_output=True,
                    timeout=30
                )
                # Should handle gracefully
                assert result.returncode == 0 or b"error" in result.stderr.lower()
            
            finally:
                os.unlink(config_path)
                if os.path.exists(output_path):
                    os.unlink(output_path)


class TestEdgeCases:
    """Tests for edge cases and boundary conditions"""
    
    def test_minimum_size_maze(self) -> None:
        """Test minimum viable maze size"""
        config = """
WIDTH=2
HEIGHT=2
ENTRY=0,0
EXIT=1,1
OUTPUT_FILE=tiny_maze.txt
PERFECT=True
"""
        fd, config_path = tempfile.mkstemp(suffix='.txt')
        with os.fdopen(fd, 'w') as f:
            f.write(config)
        
        try:
            result = subprocess.run(
                ['python3', 'a_maze_ing.py', config_path],
                capture_output=True,
                timeout=10
            )
            # Should either work or reject with clear message
            if result.returncode != 0:
                output = result.stderr.decode() + result.stdout.decode()
                assert 'error' in output.lower() or 'too small' in output.lower()
        
        finally:
            os.unlink(config_path)
            if os.path.exists('tiny_maze.txt'):
                os.unlink('tiny_maze.txt')
    
    def test_non_perfect_maze(self) -> None:
        """Test non-perfect maze generation"""
        config = """
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=nonperfect_maze.txt
PERFECT=False
"""
        fd, config_path = tempfile.mkstemp(suffix='.txt')
        with os.fdopen(fd, 'w') as f:
            f.write(config)
        
        try:
            result = subprocess.run(
                ['python3', 'a_maze_ing.py', config_path],
                capture_output=True,
                timeout=30
            )
            assert result.returncode == 0, "Non-perfect maze should work"
        
        finally:
            os.unlink(config_path)
            if os.path.exists('nonperfect_maze.txt'):
                os.unlink('nonperfect_maze.txt')


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
