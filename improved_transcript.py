#!/usr/bin/env python3
"""
Improved YouTube transcript functionality with comprehensive error handling
"""

import re
import logging
from typing import Optional, List, Dict, Any
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_video_id(url: str) -> Optional[str]:
    """
    Extract video ID from various YouTube URL formats.
    
    Args:
        url (str): YouTube URL
        
    Returns:
        Optional[str]: Video ID if found, None otherwise
    """
    patterns = [
        r'(?:v=|/)([0-9A-Za-z_-]{11}).*',  # Standard watch URL
        r'(?:embed/)([0-9A-Za-z_-]{11})',  # Embed URL
        r'(?:youtu\.be/)([0-9A-Za-z_-]{11})',  # Short URL
        r'(?:shorts/)([0-9A-Za-z_-]{11})',  # YouTube Shorts
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None

def get_available_transcripts(video_id: str) -> List[Dict[str, Any]]:
    """
    Get list of available transcripts for a video.
    
    Args:
        video_id (str): YouTube video ID
        
    Returns:
        List[Dict]: Available transcript information
    """
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        available = []
        
        for transcript in transcript_list:
            available.append({
                'language': transcript.language,
                'language_code': transcript.language_code,
                'is_generated': transcript.is_generated,
                'is_translatable': transcript.is_translatable
            })
            
        return available
    except Exception as e:
        logger.error(f"Error getting transcript list: {e}")
        return []

def get_youtube_transcript_improved(url: str, language_codes: List[str] = None) -> str:
    """
    Enhanced version of YouTube transcript retrieval with better error handling.
    
    Args:
        url (str): YouTube video URL
        language_codes (List[str]): Preferred language codes (default: ['en', 'en-US'])
        
    Returns:
        str: Full transcript text or error message
    """
    if language_codes is None:
        language_codes = ['en', 'en-US', 'en-GB']
    
    try:
        logger.info(f"Processing URL: {url}")
        
        # Extract video ID
        video_id = extract_video_id(url)
        if not video_id:
            return f"Error: Could not extract video ID from URL: {url}"
        
        logger.info(f"Extracted video ID: {video_id}")
        
        # Get available transcripts
        available_transcripts = get_available_transcripts(video_id)
        if not available_transcripts:
            return f"Error: No transcripts available for video {video_id}"
        
        logger.info(f"Available transcripts: {available_transcripts}")
        
        # Try to get transcript in preferred languages
        for lang_code in language_codes:
            try:
                transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang_code])
                logger.info(f"Successfully retrieved transcript in {lang_code}")
                
                # Format transcript
                formatter = TextFormatter()
                transcript_text = formatter.format_transcript(transcript_list)
                
                return transcript_text.strip()
                
            except Exception as lang_error:
                logger.warning(f"Failed to get transcript in {lang_code}: {lang_error}")
                continue
        
        # If no preferred language worked, try the first available transcript
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            logger.info("Retrieved transcript in default language")
            
            formatter = TextFormatter()
            transcript_text = formatter.format_transcript(transcript_list)
            
            return transcript_text.strip()
            
        except Exception as e:
            logger.error(f"Failed to get any transcript: {e}")
            
            # Try getting manually created transcripts only
            try:
                transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
                manual_transcripts = [t for t in transcript_list if not t.is_generated]
                
                if manual_transcripts:
                    transcript = manual_transcripts[0].fetch()
                    formatter = TextFormatter()
                    transcript_text = formatter.format_transcript(transcript)
                    return transcript_text.strip()
                else:
                    return f"Error: Only auto-generated transcripts available, but they couldn't be retrieved for video {video_id}"
                    
            except Exception as manual_error:
                logger.error(f"Failed to get manual transcripts: {manual_error}")
                return f"Error: Could not retrieve any transcript for video {video_id}. Available transcripts: {available_transcripts}"
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return f"Error retrieving transcript: {str(e)}"

def test_transcript_functionality():
    """Test the improved transcript functionality."""
    test_videos = [
        {
            'url': 'https://www.youtube.com/watch?v=jNQXAC9IVRw',
            'description': 'Test video 1'
        },
        {
            'url': 'https://youtu.be/dQw4w9WgXcQ',
            'description': 'Rick Astley - Never Gonna Give You Up'
        },
        {
            'url': 'https://www.youtube.com/watch?v=9bZkp7q19f0',
            'description': 'Gangnam Style'
        }
    ]
    
    print("Testing Enhanced YouTube Transcript Functionality")
    print("=" * 60)
    
    for i, video in enumerate(test_videos, 1):
        print(f"\nTest {i}: {video['description']}")
        print(f"URL: {video['url']}")
        print("-" * 50)
        
        result = get_youtube_transcript_improved(video['url'])
        
        if result.startswith("Error"):
            print(f"❌ FAILED: {result}")
        else:
            print(f"✅ SUCCESS: Retrieved transcript ({len(result)} characters)")
            print(f"Preview: {result[:300]}...")
        
        print()

if __name__ == "__main__":
    test_transcript_functionality()
