#!/usr/bin/env python3
"""
Test script for the modified transcript processing system.
This script demonstrates how to use the system with a provided transcript
instead of a YouTube URL.
"""

import sys
import os

# Add the notes module to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'notes'))

from notes.agent import root_agent

def test_transcript_processing():
    """Test the transcript processing functionality with sample transcript."""
    
    # Sample YouTube transcript (you would replace this with actual transcript)
    sample_transcript = """
    Hello everyone and welcome to today's tutorial on machine learning fundamentals. 
    In this video, we're going to cover the basic concepts that every beginner should know.
    
    First, let's talk about what machine learning actually is. Machine learning is a subset of artificial intelligence 
    that enables computers to learn and make decisions from data without being explicitly programmed for every task.
    
    There are three main types of machine learning: supervised learning, unsupervised learning, and reinforcement learning.
    
    Supervised learning is when we train our model with labeled data. For example, if we want to classify emails as spam or not spam,
    we would provide the model with thousands of emails that are already labeled as spam or not spam.
    
    Unsupervised learning is when we don't have labeled data. The algorithm tries to find patterns and structures in the data
    on its own. Clustering is a common example of unsupervised learning.
    
    Reinforcement learning is like training a pet. The algorithm learns through trial and error, receiving rewards for good actions
    and penalties for bad ones.
    
    Now let's talk about some key terms. A dataset is your collection of data. Features are the individual measurable properties
    of the things you're observing. A model is the mathematical representation that makes predictions.
    
    The training process involves feeding your data to an algorithm so it can learn patterns. Once trained, you can use your model
    to make predictions on new, unseen data.
    
    Some popular algorithms include linear regression for prediction, decision trees for classification, and neural networks
    for complex pattern recognition.
    
    Remember, the quality of your data is crucial. Garbage in, garbage out, as they say. Always clean and preprocess your data
    before training your model.
    
    That's it for today's introduction to machine learning. In our next video, we'll dive deeper into supervised learning algorithms.
    Thanks for watching and don't forget to subscribe!
    """
    
    print("Testing Transcript Processing System")
    print("=" * 60)
    print(f"Sample transcript length: {len(sample_transcript)} characters")
    print("\nProcessing transcript through the pipeline...")
    print("-" * 40)
    
    try:
        # Process the transcript through the pipeline
        result = root_agent(sample_transcript)
        
        print("✅ SUCCESS: Pipeline completed successfully!")
        print("\nResult keys:", list(result.keys()) if isinstance(result, dict) else "Not a dictionary")
        
        # Display relevant parts of the result
        if isinstance(result, dict):
            if 'save_status' in result:
                print(f"\n📁 Save Status: {result['save_status']}")
            if 'pdf_status' in result:
                print(f"\n📄 PDF Status: {result['pdf_status']}")
        else:
            print(f"\nFull result: {str(result)[:500]}...")
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        print(f"Error type: {type(e).__name__}")

def test_with_custom_transcript():
    """Allow testing with a custom transcript."""
    print("\nCustom Transcript Test")
    print("=" * 30)
    print("Enter your transcript (press Ctrl+D or Ctrl+Z when done):")
    print("-" * 30)
    
    try:
        # Read multiline input
        lines = []
        while True:
            try:
                line = input()
                lines.append(line)
            except EOFError:
                break
        
        custom_transcript = '\n'.join(lines)
        
        if custom_transcript.strip():
            print(f"\nProcessing custom transcript ({len(custom_transcript)} characters)...")
            result = root_agent(custom_transcript)
            print("✅ Custom transcript processed successfully!")
            
            if isinstance(result, dict):
                if 'save_status' in result:
                    print(f"\n📁 Save Status: {result['save_status']}")
                if 'pdf_status' in result:
                    print(f"\n📄 PDF Status: {result['pdf_status']}")
        else:
            print("No custom transcript provided.")
            
    except Exception as e:
        print(f"❌ ERROR processing custom transcript: {str(e)}")

if __name__ == "__main__":
    print("YouTube Transcript to Notes Pipeline Test")
    print("========================================")
    print("This system now works with PROVIDED TRANSCRIPTS instead of YouTube URLs")
    print()
    
    # Test with sample transcript
    test_transcript_processing()
    
    print("\n" + "="*60)
    
    # Ask if user wants to test with custom transcript
    response = input("\nWould you like to test with your own transcript? (y/n): ").lower().strip()
    if response in ['y', 'yes']:
        test_with_custom_transcript()
    else:
        print("Test completed!")
