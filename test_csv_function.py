#!/usr/bin/env python3
"""
Test script for the CSV loading function
"""

import pandas as pd
import tempfile
import os
from datetime import datetime, timezone
from data_utils import get_data_from_csv

def create_test_csv():
    """Create a test CSV file with timestamp and some data columns"""
    # Create sample data
    timestamps = pd.date_range(
        start='2024-01-01 10:00:00', 
        end='2024-01-01 12:00:00', 
        freq='1min'
    )
    
    data = {
        'timestamp': timestamps,
        'cur1': [10 + i * 0.1 for i in range(len(timestamps))],
        'cur2': [15 + i * 0.05 for i in range(len(timestamps))],
        'cur3': [12 + i * 0.08 for i in range(len(timestamps))],
        'vol1': [220 + i * 0.5 for i in range(len(timestamps))],
        'vol2': [225 + i * 0.3 for i in range(len(timestamps))],
        'vol3': [218 + i * 0.4 for i in range(len(timestamps))]
    }
    
    df = pd.DataFrame(data)
    
    # Create temporary file
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
    df.to_csv(temp_file.name, index=False)
    temp_file.close()
    
    return temp_file.name

def test_csv_function():
    """Test the CSV loading function"""
    print("Testing CSV loading function...")
    
    # Create test CSV file
    csv_file_path = create_test_csv()
    print(f"Created test CSV file: {csv_file_path}")
    
    try:
        # Test with default timestamp column
        with open(csv_file_path, 'rb') as f:
            # Simulate StreamlitUploadedFile
            class MockUploadedFile:
                def __init__(self, file_path):
                    self.file_path = file_path
                
                def read(self):
                    with open(self.file_path, 'rb') as f:
                        return f.read()
            
            uploaded_file = MockUploadedFile(csv_file_path)
            
            # Test the function
            df = get_data_from_csv(uploaded_file, "timestamp")
            
            print("✅ CSV loading successful!")
            print(f"DataFrame shape: {df.shape}")
            print(f"Columns: {list(df.columns)}")
            print(f"Index type: {type(df.index)}")
            print(f"Index timezone: {df.index.tz}")
            print(f"First few rows:")
            print(df.head())
            
    except Exception as e:
        print(f"❌ Error testing CSV function: {str(e)}")
    
    finally:
        # Clean up
        os.unlink(csv_file_path)
        print(f"Cleaned up test file: {csv_file_path}")

if __name__ == "__main__":
    test_csv_function() 