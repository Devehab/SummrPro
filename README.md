# SummrPro 🚀

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![Gemini AI](https://img.shields.io/badge/AI-Gemini%201.5%20Pro-purple.svg)](https://ai.google.dev/)
[![Docker Image](https://img.shields.io/badge/Docker-v1.0.1-blue.svg)](https://hub.docker.com/r/devehab/summrpro)

SummrPro is an AI-powered YouTube content transformer that uses Google's Gemini 1.5 Pro model to generate professional summaries from YouTube videos. It extracts video transcripts and provides clear, concise summaries in either English or Arabic.

<div align="center">
  
  ### 🎬 SummrPro Demo
  
  https://github.com/devehab/summrpro/raw/main/demo.mp4

  <a href="./demo.mp4" title="Download SummrPro Demo Video">
    <img src="https://img.shields.io/badge/🎥_Watch_Demo-Download_MP4-blue?style=for-the-badge" alt="Download Demo Video">
  </a>
  
</div>

## 📋 Table of Contents

- [✨ Features](#-features)
- [🚀 Installation & Usage](#-installation--usage)
  - [Traditional Method](#traditional-method)
  - [Docker Method](#docker-method)
- [📋 How to Use](#-how-to-use)
- [🔧 Requirements](#-requirements)
- [🧰 Development](#-development)
- [📝 Changelog](#-changelog)
- [🤝 Contributing](#-contributing)
- [📜 License](#-license)
- [👨‍💻 Author](#-author)
- [☕ Support My Work](#-support-my-work)

## ✨ Features

- **AI-Powered Summaries**: Leverages Google's Gemini 1.5 Pro model for high-quality content transformation
- **Multiple Summary Styles**: Choose between standard summary, teacher style, or professional article format
- **Bilingual Support**: Generate summaries in English or Arabic with proper RTL formatting
- **Copy to Clipboard**: Easily copy summaries with a single click
- **YouTube Integration**: Direct processing of YouTube video transcripts
- **Clear Section Breakdown**: Well-organized summaries with proper formatting
- **Technical Term Explanations**: AI identifies and explains complex concepts
- **Robust Error Handling**: User-friendly error messages with troubleshooting tips
- **Modern UI**: Responsive design with intuitive visual feedback

## 🚀 Installation & Usage

### Traditional Method

1. Clone the repository:
```bash
git clone https://github.com/devehab/summrpro.git
cd summrpro
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up the environment variables:
```bash
# Create a .env file and add your Gemini API key
echo "GEMINI_API_KEY=your_gemini_api_key_here" > .env
```

5. Run the application:
```bash
python app.py
```

6. Open your browser and navigate to http://localhost:5003

### Docker Method

You can run SummrPro using Docker with our pre-built image:

```bash
# Pull the latest stable Docker image
docker pull devehab/summrpro:v1.0.1

# Run the container
docker run -p 5003:5003 -e GEMINI_API_KEY=$GEMINI_API_KEY devehab/summrpro:v1.0.1
```

Alternatively, you can use Docker Compose:

```bash
# Create a docker-compose.yml file with the following content:
version: '3'
services:
  summrpro:
    image: devehab/summrpro:v1.0.1
    ports:
      - "5003:5003"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
    restart: unless-stopped

# Make sure your .env file contains GEMINI_API_KEY
docker-compose up
```

Or build the image yourself:

```bash
# Build the Docker image
docker build -t devehab/summrpro:latest .

# Run the container
docker run -p 5003:5003 -e GEMINI_API_KEY=$GEMINI_API_KEY devehab/summrpro:latest
```

#### Available Docker Tags
- `v1.0.1` - Latest stable release with enhanced error handling and UI improvements
- `v1.0.0` - Initial stable release with multi-platform support (linux/amd64, linux/arm64)
- `latest` - Latest build from the main branch

## 📋 How to Use

1. Open the application in your web browser
2. Paste a YouTube video URL in the input field
3. Select your preferred language (English or Arabic)
4. Choose your preferred summary style
5. Click "Transform Content" and wait for the AI to process the video
6. View and copy your generated summary

## 🔧 Requirements

- Python 3.9 or higher
- Google Gemini API key (get one from [Google AI Studio](https://ai.google.dev/))
- Internet connection for API calls
- Modern web browser (Chrome, Firefox, Safari, Edge)

## 🧰 Development

SummrPro is built with the following technologies:

- **Backend**: Python with Flask for the web server
- **Frontend**: HTML, CSS (Tailwind), and JavaScript
- **AI**: Google's Gemini 1.5 Pro model via the Google Generative AI Python library
- **API**: youtube_transcript_api for fetching YouTube subtitles
- **Containerization**: Docker for cross-platform deployment

## 📝 Changelog

### v1.0.1 (March 27, 2025)

#### Enhanced Error Handling
- Added structured error codes and messages for various error scenarios
- Improved error handling in the summarize endpoint
- Enhanced error handling in the Gemini API integration
- Added detailed error logging with traceback information

#### UI Improvements
- Redesigned header with modern gradient background and improved layout
- Added user-friendly error messages with troubleshooting tips
- Implemented warning containers for non-critical issues
- Enhanced progress indicators with icons and better status messages
- Improved language selection with culturally relevant icons
- Added proper spacing between UI elements for better readability
- Fixed error message display to prevent confusion

#### Performance Improvements
- Added timeout handling for network requests
- Improved transcript extraction reliability
- Enhanced metadata fallback when transcripts are unavailable

### v1.0.0 (Initial Release)
- Basic summarization functionality
- Multi-language support (English and Arabic)
- Multiple summary styles
- YouTube transcript extraction
- Copy to clipboard functionality
- Docker containerization

## 🤝 Contributing

Contributions are welcome! Feel free to fork the repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.

## 👨‍💻 Author

- **Ehab Kahwati** - [GitHub](https://github.com/Devehab)

## ☕ Support My Work

If you find SummrPro useful in your daily workflow, please consider supporting my work! I'm passionate about creating open-source tools that solve real problems.

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://www.buymeacoffee.com/devehab)
[![PayPal](https://img.shields.io/badge/PayPal-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/EhabKahwati)
[![GitHub Sponsors](https://img.shields.io/badge/GitHub_Sponsors-EA4AAA?style=for-the-badge&logo=github-sponsors&logoColor=white)](https://github.com/sponsors/Devehab)

As an independent developer, I dedicate my time to building and maintaining various open-source web applications and Chrome extensions that are freely available to everyone. Your support helps me:

- ✨ Continue developing new features for SummrPro
- 🐛 Fix bugs and maintain existing projects
- 🚀 Create new open-source tools for the community
- 💡 Explore innovative ideas and technologies

Even a small contribution goes a long way in supporting the development of tools that make the internet more accessible and useful for everyone.

**Thank you for your support!** ❤️

---

Made with ❤️ by Ehab Kahwati
