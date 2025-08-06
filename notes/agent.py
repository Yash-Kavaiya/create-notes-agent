# Part of agent.py --> Follow https://google.github.io/adk-docs/get-started/quickstart/ to learn the setup
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)
from google.adk.agents import LlmAgent, SequentialAgent
import re
from datetime import datetime
import os

GEMINI_MODEL = "gemini-2.0-flash"
import agentops

agentops.init(
    api_key='cc690c1c-f060-4689-a669-f716389fd9b1',
    default_tags=['google adk']
)
# --- Function Definitions ---

def process_provided_transcript(transcript: str):
    """
    Processes and validates a provided YouTube transcript.
    
    Args:
        transcript (str): The YouTube video transcript text.
        
    Returns:
        str: The processed transcript text, or error message if failed.
    """
    try:
        if not transcript or not transcript.strip():
            return "Error: No transcript provided or transcript is empty."
        
        # Basic cleaning and validation
        cleaned_transcript = transcript.strip()
        
        # Check if transcript seems valid (has reasonable length and content)
        if len(cleaned_transcript) < 50:
            return "Warning: Transcript seems very short. Proceeding anyway..."
        
        return cleaned_transcript
        
    except Exception as e:
        return f"Error processing transcript: {str(e)}"


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


def convert_markdown_to_latex_pdf(content: str):
    """
    Converts markdown content to LaTeX and then to PDF, saving in a 'pdfs' folder.
    
    Args:
        content (str): The markdown content to convert.
        
    Returns:
        str: Success message with file path, or error message if failed.
    """
    try:
        import subprocess
        
        # Create pdfs directory if it doesn't exist
        pdf_dir = "pdfs"
        os.makedirs(pdf_dir, exist_ok=True)
        
        # Generate timestamp filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_filename = f"youtube_notes_{timestamp}"
        
        # File paths
        tex_file = os.path.join(pdf_dir, f"{base_filename}.tex")
        pdf_file = os.path.join(pdf_dir, f"{base_filename}.pdf")
        
        # Convert markdown to LaTeX format
        latex_content = markdown_to_latex(content)
        
        # Save LaTeX file
        with open(tex_file, 'w', encoding='utf-8') as f:
            f.write(latex_content)
        
        # Convert LaTeX to PDF using pdflatex
        try:
            # Change to pdf directory for compilation
            current_dir = os.getcwd()
            os.chdir(pdf_dir)
            
            # Run pdflatex twice for proper cross-references
            subprocess.run(['pdflatex', '-interaction=nonstopmode', f"{base_filename}.tex"], 
                         check=True, capture_output=True, text=True)
            subprocess.run(['pdflatex', '-interaction=nonstopmode', f"{base_filename}.tex"], 
                         check=True, capture_output=True, text=True)
            
            # Clean up auxiliary files
            for ext in ['.aux', '.log', '.out', '.toc']:
                aux_file = f"{base_filename}{ext}"
                if os.path.exists(aux_file):
                    os.remove(aux_file)
            
            os.chdir(current_dir)
            
        except subprocess.CalledProcessError as e:
            os.chdir(current_dir)
            return f"Error during PDF compilation: {e}"
        except FileNotFoundError:
            os.chdir(current_dir)
            return "Error: pdflatex not found. Please install LaTeX (e.g., texlive-latex-base texlive-latex-extra)"
        
        # Get absolute path for confirmation
        abs_pdf_path = os.path.abspath(pdf_file)
        abs_tex_path = os.path.abspath(tex_file)
        
        return f"Successfully converted to PDF!\nLaTeX file: {abs_tex_path}\nPDF file: {abs_pdf_path}"
        
    except Exception as e:
        return f"Error converting to PDF: {str(e)}"


def markdown_to_latex(markdown_content: str):
    """
    Converts markdown content to LaTeX format.
    
    Args:
        markdown_content (str): The markdown content to convert.
        
    Returns:
        str: The LaTeX formatted content.
    """
    # Basic LaTeX document structure
    latex_header = r"""\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{geometry}
\usepackage{hyperref}
\usepackage{graphicx}
\usepackage{fancyhdr}
\usepackage{listings}
\usepackage{xcolor}
\usepackage{tcolorbox}
\usepackage{amsmath}
\usepackage{amssymb}

% Page setup
\geometry{margin=1in}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{YouTube Notes}
\fancyhead[R]{\today}
\fancyfoot[C]{\thepage}

% Code block styling
\lstset{
    backgroundcolor=\color{gray!10},
    basicstyle=\ttfamily\footnotesize,
    breaklines=true,
    frame=single,
    rulecolor=\color{gray!30}
}

% Quote styling
\newtcolorbox{myquote}{
    colback=blue!5!white,
    colframe=blue!75!black,
    leftrule=3mm
}

\begin{document}

"""
    
    latex_footer = r"""
\end{document}
"""
    
    # Convert markdown content to LaTeX
    content = markdown_content
    
    # Convert headers
    content = re.sub(r'^# (.+)$', r'\\section{\1}', content, flags=re.MULTILINE)
    content = re.sub(r'^## (.+)$', r'\\subsection{\1}', content, flags=re.MULTILINE)
    content = re.sub(r'^### (.+)$', r'\\subsubsection{\1}', content, flags=re.MULTILINE)
    content = re.sub(r'^#### (.+)$', r'\\paragraph{\1}', content, flags=re.MULTILINE)
    
    # Convert bold text
    content = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', content)
    
    # Convert italic text
    content = re.sub(r'\*(.+?)\*', r'\\textit{\1}', content)
    
    # Convert code inline
    content = re.sub(r'`(.+?)`', r'\\texttt{\1}', content)
    
    # Convert code blocks
    content = re.sub(r'```([^`]+)```', r'\\begin{lstlisting}\n\1\n\\end{lstlisting}', content, flags=re.DOTALL)
    
    # Convert blockquotes
    content = re.sub(r'^> (.+)$', r'\\begin{myquote}\n\1\n\\end{myquote}', content, flags=re.MULTILINE)
    
    # Convert unordered lists
    content = re.sub(r'^- (.+)$', r'\\item \1', content, flags=re.MULTILINE)
    
    # Convert numbered lists
    content = re.sub(r'^\d+\. (.+)$', r'\\item \1', content, flags=re.MULTILINE)
    
    # Wrap consecutive items in itemize/enumerate environments
    lines = content.split('\n')
    in_list = False
    result_lines = []
    
    for line in lines:
        if line.strip().startswith('\\item'):
            if not in_list:
                result_lines.append('\\begin{itemize}')
                in_list = True
            result_lines.append(line)
        else:
            if in_list:
                result_lines.append('\\end{itemize}')
                in_list = False
            result_lines.append(line)
    
    if in_list:
        result_lines.append('\\end{itemize}')
    
    content = '\n'.join(result_lines)
    
    # Escape special LaTeX characters
    special_chars = {
        '&': '\\&',
        '%': '\\%',
        '$': '\\$',
        '#': '\\#',
        '_': '\\_',
        '{': '\\{',
        '}': '\\}',
        '~': '\\textasciitilde{}',
        '^': '\\textasciicircum{}'
    }
    
    for char, replacement in special_chars.items():
        # Don't escape if it's already part of a LaTeX command
        content = re.sub(f'(?<!\\\\){re.escape(char)}', replacement, content)
    
    return latex_header + content + latex_footer


# --- 1. Define Sub-Agents for Each Pipeline Stage ---

# YouTube Transcript Processor Agent
transcript_processor_agent = LlmAgent(
    name="TranscriptProcessorAgent",
    model=GEMINI_MODEL,
    instruction="""You are a YouTube Transcript Processor.
When the user provides a YouTube transcript, use the process_provided_transcript function to validate and process it.
Pass the transcript text directly to the function.
If successful, output the processed transcript.
If there's an error, inform the user about the issue.
""",
    description="Processes and validates provided YouTube transcript using the provided function.",
    tools=[process_provided_transcript],
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

# PDF Converter Agent
pdf_converter_agent = LlmAgent(
    name="PDFConverterAgent",
    model=GEMINI_MODEL,
    instruction="""You are a LaTeX PDF Converter.
Convert the enhanced notes to a LaTeX PDF document and save it in the 'pdfs' folder.

**Enhanced Notes:**
{enhanced_notes}

Use the convert_markdown_to_latex_pdf function to convert these notes to PDF.
The function takes the markdown content and creates both a LaTeX file and a PDF file.
Report the conversion status to the user.
""",
    description="Converts enhanced notes to LaTeX PDF and saves in pdfs folder.",
    tools=[convert_markdown_to_latex_pdf],
    output_key="pdf_status"  # Stores output in state['pdf_status']
)

# --- 2. Create the SequentialAgent ---
youtube_notes_pipeline = SequentialAgent(
    name="YouTubeNotesPipeline",
    sub_agents=[transcript_processor_agent, notes_creator_agent, notes_enhancer_agent, markdown_saver_agent, pdf_converter_agent],
    description="Converts provided YouTube transcripts to comprehensive notes saved as markdown files and PDF documents.",
)

# For ADK tools compatibility, the root agent must be named `root_agent`
root_agent = youtube_notes_pipeline