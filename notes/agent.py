# Part of agent.py --> Follow https://google.github.io/adk-docs/get-started/quickstart/ to learn the setup

from google.adk.agents import LlmAgent, SequentialAgent
from youtube_transcript_api import YouTubeTranscriptApi
import re
from datetime import datetime
import os

GEMINI_MODEL = "gemini-2.0-flash"

# --- Function Definitions ---

def get_youtube_transcript(url: str):
    """
    Retrieves the transcript from a YouTube video URL.
    
    Args:
        url (str): The YouTube video URL.
        
    Returns:
        str: The full transcript text, or error message if failed.
    """
    try:
        # Extract video ID from various YouTube URL formats
        video_id_match = re.search(r'(?:v=|youtu\.be/|/v/|/embed/|/watch\?v=|shorts/)([a-zA-Z0-9_-]{11})', url)
        
        if not video_id_match:
            return f"Error: Could not extract video ID from URL: {url}"
        
        video_id = video_id_match.group(1)
        
        # Fetch transcript
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Combine all text segments
        full_transcript = " ".join([segment['text'] for segment in transcript_list])
        
        return full_transcript
        
    except Exception as e:
        return f"Error retrieving transcript: {str(e)}"


def save_markdown_file(content: str):
    """
    Saves content to a markdown file with auto-generated timestamp filename.
    
    Args:
        content (str): The markdown content to save.
        
    Returns:
        str: Success message with file path, or error message if failed.
    """
    try:
        # Generate timestamp filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"youtube_notes_{timestamp}.md"
        
        # Save the file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Get absolute path for confirmation
        abs_path = os.path.abspath(filename)
        
        return f"Successfully saved notes to: {abs_path}"
        
    except Exception as e:
        return f"Error saving file: {str(e)}"


# --- 1. Define Sub-Agents for Each Pipeline Stage ---

# YouTube Transcript Extractor Agent
youtube_transcript_agent = LlmAgent(
    name="YouTubeTranscriptAgent",
    model=GEMINI_MODEL,
    instruction="""You are a YouTube Transcript Extractor.
When the user provides a YouTube URL, use the get_youtube_transcript function to fetch the transcript.
Pass the URL directly to the function.
If successful, output the transcript.
If there's an error, inform the user about the issue.
""",
    description="Extracts transcript from YouTube video using the provided function.",
    tools=[get_youtube_transcript],
    output_key="transcript"  # Stores output in state['transcript']
)

# Notes Creator Agent
notes_creator_agent = LlmAgent(
    name="NotesCreatorAgent",
    model=GEMINI_MODEL,
    instruction="""You are an expert Note Creator.
Create comprehensive study notes from the provided transcript.

**Transcript:**
{transcript}

**Create structured notes including:**

# [Video Title - infer from content]

## 📝 Summary
[2-3 sentence overview of the main topic]

## 🎯 Key Concepts
- **Concept 1**: Brief explanation
- **Concept 2**: Brief explanation
- **Concept 3**: Brief explanation

## 📚 Detailed Notes

### [Main Topic 1]
- Important point
- Supporting detail
- Example or application

### [Main Topic 2]
- Key insight
- Explanation
- Practical application

## 💡 Important Quotes
> "Notable quote from the video"

## 🔑 Key Takeaways
1. Main learning point
2. Actionable insight
3. Important conclusion

## 📋 Action Items
- [ ] Task or follow-up
- [ ] Further research topic
- [ ] Practice exercise

**Output:**
Output the complete notes in Markdown format.
""",
    description="Creates comprehensive notes from transcript.",
    output_key="notes"  # Stores output in state['notes']
)

# Notes Enhancer Agent
notes_enhancer_agent = LlmAgent(
    name="NotesEnhancerAgent",
    model=GEMINI_MODEL,
    instruction="""You are a Notes Enhancement Specialist.
Enhance the notes with visual elements and better organization.

**Notes to Enhance:**
{notes}

**Add these enhancements:**

1. **Table of Contents** - Add at the beginning with links
2. **Tables** - Convert appropriate lists to tables
3. **Visual Diagrams** - Add ASCII diagrams where helpful
4. **Quick Reference** - Add a summary card at the end
5. **Metadata** - Add creation date and tags

**Example Table:**
| Topic | Key Point | Application |
|-------|-----------|-------------|
| Item  | Detail    | Usage       |

**Example Diagram:**
```
┌─────────┐     ┌─────────┐     ┌─────────┐
│  Input  │ --> │ Process │ --> │ Output  │
└─────────┘     └─────────┘     └─────────┘
```

**Output:**
Output the enhanced notes in Markdown format with all improvements.
""",
    description="Enhances notes with visual elements and organization.",
    output_key="enhanced_notes"  # Stores output in state['enhanced_notes']
)

# Markdown File Saver Agent
markdown_saver_agent = LlmAgent(
    name="MarkdownSaverAgent",
    model=GEMINI_MODEL,
    instruction="""You are a File System Manager.
Save the enhanced notes to a markdown file using the save_markdown_file function.

**Enhanced Notes:**
{enhanced_notes}

Use the save_markdown_file function to save these notes.
The function only takes one parameter - the content to save.
Report the save status to the user.
""",
    description="Saves the enhanced notes to a local markdown file.",
    tools=[save_markdown_file],
    output_key="save_status"  # Stores output in state['save_status']
)

# --- 2. Create the SequentialAgent ---
youtube_notes_pipeline = SequentialAgent(
    name="YouTubeNotesPipeline",
    sub_agents=[youtube_transcript_agent, notes_creator_agent, notes_enhancer_agent, markdown_saver_agent],
    description="Converts YouTube videos to comprehensive notes saved as markdown files.",
)

# For ADK tools compatibility, the root agent must be named `root_agent`
root_agent = youtube_notes_pipeline