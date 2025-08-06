#!/usr/bin/env python3
"""
Usage Example: YouTube Transcript to Notes Pipeline
===================================================

This example shows how to use the modified system that accepts
YouTube transcripts directly instead of YouTube URLs.

Usage:
1. Copy your YouTube transcript text
2. Pass it to the pipeline
3. Get structured notes and PDF output
"""

from notes.agent import root_agent

def process_transcript_to_notes(transcript_text: str) -> dict:
    """
    Process a YouTube transcript into structured notes.
    
    Args:
        transcript_text (str): The YouTube video transcript
        
    Returns:
        dict: Results from the processing pipeline
    """
    try:
        print("🔄 Processing transcript through the pipeline...")
        result = root_agent(transcript_text)
        print("✅ Processing completed!")
        return result
    except Exception as e:
        print(f"❌ Error: {e}")
        return {"error": str(e)}

# Example usage:
if __name__ == "__main__":
    # Example transcript (replace with your actual transcript)
    example_transcript = """
    Welcome to this tutorial on Python programming. Today we'll learn about functions.
    
    A function is a block of code that performs a specific task. Functions help us organize our code
    and make it reusable. To define a function in Python, we use the 'def' keyword.
    
    Here's the basic syntax: def function_name(parameters): and then the function body.
    
    Let's look at a simple example. def greet(name): return f"Hello, {name}!"
    
    Functions can take parameters and return values. Parameters are inputs to the function,
    and the return statement sends a value back to whoever called the function.
    
    You can also have functions with no parameters and no return value. These are useful
    for performing actions like printing messages or saving files.
    
    Remember to call your function after defining it, otherwise it won't execute.
    That's the basics of Python functions. Practice creating your own functions!
    """
    
    print("YouTube Transcript to Notes Converter")
    print("=" * 40)
    print(f"Processing example transcript ({len(example_transcript)} characters)...")
    
    # Process the transcript
    results = process_transcript_to_notes(example_transcript)
    
    # Display results
    if "error" not in results:
        print("\n📊 Pipeline Results:")
        for key, value in results.items():
            print(f"  {key}: {str(value)[:100]}...")
    else:
        print(f"\n❌ Processing failed: {results['error']}")
