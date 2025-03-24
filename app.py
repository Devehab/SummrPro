import os
from flask import Flask, render_template, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled, VideoUnavailable
from youtube_transcript_api.formatters import TextFormatter
import google.generativeai as genai
from dotenv import load_dotenv
import requests
import re

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Initialize the model
model = genai.GenerativeModel('gemini-1.5-pro')

app = Flask(__name__)

def extract_video_id(youtube_url):
    """Extract the video ID from a YouTube URL."""
    if "youtu.be" in youtube_url:
        return youtube_url.split("/")[-1].split("?")[0]
    elif "youtube.com" in youtube_url:
        if "v=" in youtube_url:
            return youtube_url.split("v=")[1].split("&")[0]
    return None

def extract_video_title(youtube_url):
    """Attempt to extract the video title from a YouTube URL."""
    # Try to find title in URL (sometimes present in the URL)
    title_match = re.search(r'title=([^&]+)', youtube_url)
    if title_match:
        return title_match.group(1).replace('+', ' ')
    return None

def get_youtube_transcript(video_id, language=None):
    """
    Get transcript for a YouTube video. Attempt to get transcript in the specified language,
    if not available, attempt to get it in any available language.
    """
    try:
        # First try to get transcript in the specified language
        if language:
            try:
                transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=[language, language[:2]])
                return ' '.join([t['text'] for t in transcript_list])
            except (NoTranscriptFound, TranscriptsDisabled, VideoUnavailable) as e:
                print(f"Could not get transcript in language {language}: {str(e)}")
                # Continue to try other languages
        
        # If no specific language or specific language failed, try to get any transcript
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            
            # Try to get manually created transcript first (usually higher quality)
            for transcript in transcript_list:
                if not transcript.is_generated:
                    full_transcript = transcript.fetch()
                    print(f"Found manually created transcript in {transcript.language_code}")
                    return ' '.join([t['text'] for t in full_transcript])
            
            # If no manual transcript, get any available transcript
            generated_transcript = next(iter(transcript_list)).fetch()
            source_lang = next(iter(transcript_list)).language_code
            print(f"Using generated transcript in {source_lang}")
            return ' '.join([t['text'] for t in generated_transcript])
            
        except (NoTranscriptFound, TranscriptsDisabled, VideoUnavailable) as e:
            print(f"Could not get transcript in any language: {str(e)}")
            return None
            
    except Exception as e:
        print(f"An error occurred while getting transcript: {str(e)}")
        return None

def summarize_with_gemini(text, language="en", is_transcript=True, video_id=None, style="standard"):
    try:
        model = genai.GenerativeModel(model_name="gemini-1.5-pro")
        
        # Handle case when no text is available
        if not text and video_id:
            # If no text is available, use the video ID to create a minimal prompt
            if language == "ar":
                prompt = f"""
                لم يتم العثور على نص للفيديو ذو المعرف {video_id}.
                
                الرجاء تقديم وصف عام يشرح:
                1. أن المحتوى لا يمكن تلخيصه بدون نص
                2. الأسباب المحتملة لعدم توفر النص (مثل: الفيديو لا يحتوي على ترجمة، أو أن الترجمة غير متاحة، أو أن الفيديو خاص)
                3. نصائح للمستخدم حول كيفية العثور على ملخصات أو معلومات بديلة
                """
            else:
                prompt = f"""
                No transcript could be found for the video with ID {video_id}.
                
                Please provide a general description explaining:
                1. That the content cannot be summarized without a transcript
                2. Possible reasons why the transcript is not available (e.g., video doesn't have captions, captions are disabled, or the video is private)
                3. Tips for the user on how to find alternative summaries or information
                """
        elif language == "ar":
            if is_transcript:
                if style == "teacher":
                    prompt = f"""
                    أنت معلم محترف ومتخصص. قم بشرح نص هذا الفيديو بالتفصيل الكامل كما لو كنت تشرحه لطلابك باللغة العربية، دون اختصار أي محتوى.
                    
                    نص الفيديو (قد يكون بلغة أخرى، قم بترجمته وشرحه بالعربية):
                    {text}
                    
                    يجب أن يتضمن الشرح:
                    1. مقدمة تعريفية شاملة بالموضوع وأهميته
                    2. شرح تفصيلي للأفكار الرئيسية بأسلوب تعليمي واضح
                    3. توضيح المفاهيم المعقدة والمصطلحات التقنية مع أمثلة متعددة سهلة الفهم
                    4. تقسيم المعلومات إلى أقسام منطقية وتسلسلية
                    5. شرح كل نقطة بالتفصيل مع ربطها بالواقع العملي والتطبيقات
                    6. خلاصة تلخص النقاط الأساسية وتربط الموضوع بالواقع العملي
                    
                    استخدم أسلوباً تعليمياً يناسب شرح المعلم للطلاب، مع الحفاظ على المستوى العلمي للمحتوى.
                    هام: لا تقم باختصار المحتوى، بل قدّم شرحاً تفصيلياً كاملاً لكل محتوى الفيديو.
                    """
                elif style == "article":
                    prompt = f"""
                    أنت كاتب محترف ومتخصص في مجال المحتوى المعروض. قم بتحويل نص هذا الفيديو إلى مقالة احترافية تفصيلية باللغة العربية دون اختصار أي محتوى.
                    
                    نص الفيديو (قد يكون بلغة أخرى، قم بترجمته وكتابته كمقالة كاملة بالعربية):
                    {text}
                    
                    يجب أن تتضمن المقالة:
                    1. عنواناً جذاباً وفقرة افتتاحية قوية تمهد للموضوع
                    2. تطوير كامل وشامل للأفكار بأسلوب أدبي رصين
                    3. استخدام لغة احترافية تناسب المتخصصين في المجال
                    4. شرح تفصيلي لكل نقطة مع أمثلة توضيحية
                    5. تنظيم المحتوى في فقرات متماسكة وعناوين فرعية واضحة
                    6. تحليل عميق للمفاهيم والأفكار المطروحة
                    7. خاتمة تستخلص الأفكار الرئيسية وتقدم رؤية مستقبلية أو توصيات
                    
                    اكتب المقالة كخبير متخصص في المجال، مع إظهار عمق المعرفة والخبرة المهنية.
                    هام: قدم تفاصيل كاملة دون اختصار، واشرح كل محتوى الفيديو بشكل شامل.
                    """
                else:  # standard/summary style
                    prompt = f"""
                    أنت مساعد محترف لتلخيص مقاطع الفيديو. قم بتلخيص نص هذا الفيديو بطريقة شاملة ومختصرة باللغة العربية.
                    
                    نص الفيديو (قد يكون بلغة أخرى، قم بترجمته وتلخيصه بالعربية):
                    {text}
                    
                    قدم ملخصًا مختصراً يغطي النقاط الرئيسية والمعلومات المهمة.
                    
                    يجب أن يتضمن الملخص:
                    1. الأفكار والمفاهيم الرئيسية، مع التركيز على النقاط الأساسية
                    2. شرح مختصر للمصطلحات التقنية أو المعقدة إذا وجدت
                    3. تقسيم المعلومات إلى أقسام واضحة لسهولة القراءة
                    4. تغطية مختصرة للمحتوى دون إطالة غير ضرورية
                    
                    قدم الملخص بتنسيق سهل القراءة، باستخدام النقاط والعناوين الفرعية عند الحاجة.
                    """
            else:
                # For metadata, we'll keep the style simpler regardless of selected style
                prompt = f"""
                أنت مساعد محترف لتلخيص مقاطع الفيديو. استنادًا إلى المعلومات المتاحة عن هذا الفيديو، قم بإنشاء ملخص مفيد باللغة العربية.
                
                معلومات الفيديو (قد تكون بلغة أخرى، قم بترجمتها وتلخيصها بالعربية):
                {text}
                
                حاول تقديم معلومات دقيقة وشاملة، مع العلم أن المعلومات المتاحة محدودة.
                
                ضمّن في ملخصك:
                1. الأفكار الرئيسية والمفاهيم المهمة بناءً على المعلومات المتاحة
                2. تحليل لما يبدو أن الفيديو يدور حوله
                3. تقسيم المعلومات إلى أقسام واضحة إن أمكن
                
                قدم الملخص بتنسيق سهل القراءة.
                ملاحظة: هذا الملخص يعتمد على معلومات محدودة وليس على المحتوى الكامل للفيديو.
                """
        else:  # English
            if is_transcript:
                if style == "teacher":
                    prompt = f"""
                    You are a professional educator and subject matter expert. Explain this video transcript in FULL DETAIL as if you were teaching it to your students in English, without summarizing or omitting any content.
                    
                    Video transcript (may be in another language, please translate to English and explain thoroughly):
                    {text}
                    
                    Your explanation should include:
                    1. A comprehensive introduction that frames the topic and its importance
                    2. Detailed explanations of ALL ideas using educational techniques
                    3. Thorough clarification of complex concepts and technical terms with multiple easy-to-understand examples
                    4. Organization of information into logical, sequential sections
                    5. In-depth explanation of each point with practical applications
                    6. A conclusion that connects the topic to practical applications
                    
                    Use a teaching style appropriate for a classroom setting while maintaining the academic integrity of the content.
                    IMPORTANT: Do NOT summarize the content. Provide a COMPLETE and DETAILED explanation of all video content.
                    """
                elif style == "article":
                    prompt = f"""
                    You are a professional writer and subject matter expert in the presented content area. Transform this video transcript into a comprehensive professional article in English, without summarizing or omitting any content.
                    
                    Video transcript (may be in another language, please translate to English and write as a full article):
                    {text}
                    
                    The article should include:
                    1. A compelling headline and strong opening paragraph that introduces the topic
                    2. Full development of ALL ideas in a polished, literary style
                    3. Professional language appropriate for specialists in the field
                    4. Detailed explanation of each point with illustrative examples
                    5. Content organized into cohesive paragraphs with clear subheadings
                    6. In-depth analysis of concepts and ideas presented
                    7. A conclusion that draws out key insights and offers forward-looking perspectives or recommendations
                    
                    Write the article as a domain expert, demonstrating depth of knowledge and professional expertise.
                    IMPORTANT: Provide COMPLETE details without summarizing, and fully explain all video content.
                    """
                else:  # standard/summary style
                    prompt = f"""
                    You are a professional video summarizer. Summarize this video transcript in a clear, concise manner in English.
                    
                    Video transcript (may be in another language, please translate to English and summarize):
                    {text}
                    
                    Provide a concise summary that covers the key points and important information.
                    
                    Your summary should include:
                    1. The main ideas and key concepts, with emphasis on the essential points
                    2. Brief explanations of technical or complex terms if present
                    3. Information broken down into clear sections for readability
                    4. Concise coverage of content without unnecessary verbosity
                    
                    Present the summary in an easy-to-read format, using bullet points and subheadings when needed.
                    """
            else:
                # For metadata, we'll keep the style simpler regardless of selected style
                prompt = f"""
                You are a professional video summarizer. Based on the available information about this video, create a helpful summary in English.
                
                Video information (may be in another language, please translate to English and summarize):
                {text}
                
                Try to provide accurate and comprehensive information, keeping in mind that the available information is limited.
                
                Include in your summary:
                1. The main ideas and important concepts based on the available information
                2. An analysis of what the video appears to be about
                3. Breakdown of information into clear sections if possible
                
                Present the summary in an easy-to-read format.
                NOTE: This summary is based on limited information and not the full video content.
                """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error with Gemini API: {str(e)}")
        return f"Error generating summary: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.json
    youtube_url = data.get('youtube_url')
    language = data.get('language', 'en')
    style = data.get('style', 'standard')
    
    video_id = extract_video_id(youtube_url)
    if not video_id:
        return jsonify({'error': 'Invalid YouTube URL'}), 400
    
    # Try to get the transcript
    transcript = get_youtube_transcript(video_id, language)
    
    if transcript:
        # We have a transcript, summarize it
        summary = summarize_with_gemini(transcript, language, is_transcript=True, style=style)
        return jsonify({
            'summary': summary, 
            'is_transcript': True, 
            'has_minimal_info': False,
            'transcript_source': 'direct'
        })
    
    # No direct transcript available, try to get video metadata
    try:
        # Get video info from YouTube
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        response = requests.get(video_url)
        html_content = response.text
        
        # Extract title
        title_match = re.search(r'<title>(.*?) - YouTube</title>', html_content)
        title = title_match.group(1) if title_match else 'Unknown Title'
        
        # Extract description
        desc_match = re.search(r'"description":{"simpleText":"(.*?)"}', html_content)
        description = desc_match.group(1) if desc_match else ''
        
        # Clean up description (remove escape characters)
        description = description.replace('\\n', '\n').replace('\\', '')
        
        # Removed character limit - use full description
        
        # Build metadata text
        metadata_text = f"Video Title: {title}\n\nVideo Description: {description}"
        
        # Use metadata for summarization if we have enough information
        if len(metadata_text) > 100:  # At least some meaningful content
            summary = summarize_with_gemini(metadata_text, language, is_transcript=False, style=style)
            return jsonify({
                'summary': summary, 
                'is_transcript': False, 
                'has_minimal_info': False
            })
        else:
            # If we don't have enough metadata, generate a minimal info message
            summary = summarize_with_gemini(None, language, is_transcript=False, video_id=video_id, style=style)
            return jsonify({
                'summary': summary, 
                'is_transcript': False, 
                'has_minimal_info': True
            })
            
    except Exception as e:
        print(f"Error gathering video info: {str(e)}")
        # If all else fails, generate a minimal info message
        summary = summarize_with_gemini(None, language, is_transcript=False, video_id=video_id, style=style)
        return jsonify({
            'summary': summary, 
            'is_transcript': False, 
            'has_minimal_info': True
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5003)
