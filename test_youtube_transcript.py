#!/usr/bin/env python3
"""
Test script to verify YouTube transcript functionality
"""

import sys
import os
sys.path.append('/workspaces/create-notes-agent')

from notes.agent import get_youtube_transcript

def test_youtube_transcript():
    """Test the YouTube transcript function with a sample video."""
    
    # Test with a known public video that should have captions
    test_urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # Rick Roll - famous video
        "https://youtu.be/dQw4w9WgXcQ",  # Short URL format
        "https://www.youtube.com/watch?v=jNQXAC9IVRw",  # Another test video
    ]
    
    print("Testing YouTube Transcript Functionality")
    print("=" * 50)
    
    for i, url in enumerate(test_urls, 1):
        print(f"\nTest {i}: {url}")
        print("-" * 30)
        
        try:
            result = get_youtube_transcript(url)
            
            if result.startswith("Error"):
                print(f"❌ FAILED: {result}")
            else:
                print(f"✅ SUCCESS: Retrieved transcript ({len(result)} characters)")
                print(f"Preview: {result[:200]}...")
                
        except Exception as e:
            print(f"❌ EXCEPTION: {str(e)}")

if __name__ == "__main__":
    test_youtube_transcript()
