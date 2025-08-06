# YouTube Transcript to Notes Pipeline

A system that converts YouTube video transcripts into comprehensive study notes, saving them as both Markdown and PDF files.

## 🔄 Recent Changes

**IMPORTANT UPDATE**: This system has been modified to work with **provided transcripts** instead of YouTube URLs.

### What Changed:
- ❌ **Removed**: YouTube URL processing and transcript extraction
- ✅ **Added**: Direct transcript input processing
- ✅ **Modified**: Pipeline now starts with transcript validation instead of URL fetching

## 🚀 How It Works

### Input
Instead of providing a YouTube URL, you now provide the **transcript text directly**.

### Pipeline Stages
1. **Transcript Processor** - Validates and processes the provided transcript
2. **Notes Creator** - Converts transcript into structured notes
3. **Notes Enhancer** - Adds visual elements and better organization
4. **Markdown Saver** - Saves notes as timestamped `.md` file
5. **PDF Converter** - Converts to LaTeX and generates PDF in `pdfs/` folder

## 📋 Usage

### Basic Usage
```python
from notes.agent import root_agent

# Your transcript text (copy from YouTube or other source)
transcript = """
Your video transcript content goes here...
This can be multiple paragraphs and any length.
"""

# Process through the pipeline
result = root_agent(transcript)

# Check results
print(result['save_status'])  # Markdown file path
print(result['pdf_status'])   # PDF file path
```

### Test Scripts

#### 1. Run the test script:
```bash
python test_transcript_processing.py
```

#### 2. Run the example:
```bash
python example_usage.py
```

## 📁 Output Files

### Markdown Files
- Saved in root directory
- Filename format: `youtube_notes_YYYYMMDD_HHMMSS.md`
- Contains structured notes with headers, bullet points, quotes, etc.

### PDF Files
- Saved in `pdfs/` directory
- Filename format: `youtube_notes_YYYYMMDD_HHMMSS.pdf`
- Professional LaTeX formatting with proper typography

## 📝 Notes Structure

The generated notes include:

```markdown
# [Video Title - inferred from content]

## 📝 Summary
Brief overview of the main topic

## 🎯 Key Concepts
- **Concept 1**: Explanation
- **Concept 2**: Explanation

## 📚 Detailed Notes
### [Main Topic 1]
- Important points
- Supporting details

## 💡 Important Quotes
> "Notable quotes from the video"

## 🔑 Key Takeaways
1. Main learning points
2. Actionable insights

## 📋 Action Items
- [ ] Follow-up tasks
- [ ] Further research topics
```

## 🔧 How to Get YouTube Transcripts

Since this system now requires transcript input, here's how to get YouTube transcripts:

### Method 1: YouTube Website
1. Go to the YouTube video
2. Click the three dots menu below the video
3. Select "Show transcript"
4. Copy the transcript text
5. Paste into your script

### Method 2: Using the improved_transcript.py Script
```bash
python improved_transcript.py
# Or use the functions directly to get transcripts from URLs
```

### Method 3: Browser Extensions
- Use transcript extraction browser extensions
- Copy the extracted text

## 🛠️ Dependencies

```bash
# Core dependencies
pip install google-adk-agents
pip install agentops

# For PDF generation (optional)
apt-get install texlive-latex-base texlive-latex-extra
```

## 📊 System Architecture

```
Input: Transcript Text
         ↓
[Transcript Processor] → Validates input
         ↓
[Notes Creator] → Generates structured notes
         ↓
[Notes Enhancer] → Adds visual elements
         ↓
[Markdown Saver] → Saves .md file
         ↓
[PDF Converter] → Generates PDF
         ↓
Output: .md file + .pdf file
```

## 🔍 Troubleshooting

### Common Issues:

1. **Empty transcript error**
   - Make sure your transcript text is not empty
   - Check that you're passing the actual transcript content

2. **PDF generation fails**
   - Install LaTeX: `apt-get install texlive-latex-base texlive-latex-extra`
   - Check that `pdflatex` is available in PATH

3. **File save errors**
   - Check write permissions in the current directory
   - Ensure `pdfs/` directory can be created

## 📧 Support

If you encounter issues, check:
1. The transcript text is properly formatted
2. All dependencies are installed
3. File permissions are correct
4. The `agentops` API key is valid

## 🔄 Migration from URL-based System

If you were using the old URL-based system:

**Before:**
```python
result = root_agent("https://www.youtube.com/watch?v=VIDEO_ID")
```

**Now:**
```python
# First get the transcript (manually or using improved_transcript.py)
transcript = "Your transcript text here..."
result = root_agent(transcript)
```
