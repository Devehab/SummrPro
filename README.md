# SummrPro 🚀

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![Gemini AI](https://img.shields.io/badge/AI-Gemini%201.5%20Pro-purple.svg)](https://ai.google.dev/)

SummrPro is an AI-powered YouTube content transformer that uses Google's Gemini 1.5 Pro model to generate professional summaries from YouTube videos. It extracts video transcripts and provides clear, concise summaries in either English or Arabic.

<p align="center">
  <img src="https://i.imgur.com/placeholder-image.png" alt="SummrPro Screenshot" width="80%">
</p>

## 📋 Table of Contents

- [Features](#-features)
- [Installation & Usage](#-installation--usage)
  - [Traditional Method](#traditional-method)
  - [Docker Method](#docker-method)
- [How to Use](#-how-to-use)
- [Requirements](#-requirements)
- [Development](#-development)
- [Contributing](#-contributing)
- [License](#-license)
- [Author](#-author)
- [Support My Work](#-support-my-work)

## ✨ Features

- **AI-Powered Summaries**: Leverages Google's Gemini 1.5 Pro model for high-quality content transformation
- **Multiple Summary Styles**: Choose between standard summary, teacher style, or professional article format
- **Bilingual Support**: Generate summaries in either English or Arabic
- **Interactive UI**: Modern, responsive interface with real-time progress tracking
- **Copy to Clipboard**: One-click copying of generated summaries
- **YouTube Integration**: Seamlessly extracts transcripts from YouTube videos
- **Clear Section Breakdown**: Well-organized summaries with proper formatting
- **Technical Term Explanations**: AI identifies and explains complex concepts

## 🚀 Installation & Usage

### Traditional Method

1. Clone the repository:
```bash
git clone https://github.com/Devehab/subtube.git
cd subtube
```

2. Create and activate a virtual environment (optional but recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required dependencies:
```bash
pip3 install -r requirements.txt
```

4. Run the application:
```bash
python3 app.py
```

### Docker Method

#### Using Docker directly:
1. Build the Docker image:
```bash
docker build -t summrpro:latest .
```

2. Run the container:
```bash
docker run -p 5003:5003 summrpro:latest
```

3. Access the application: Open your browser and navigate to http://localhost:5003

#### Using Docker Compose:
1. Start the service:
```bash
docker-compose up -d
```

2. Access the application: Open your browser and navigate to http://localhost:5003

3. Stop the service:
```bash
docker-compose down
```

## 📋 How to Use

1. Open the application in your web browser
2. Paste a YouTube video URL in the input field
3. Select your preferred language (English or Arabic)
4. Choose a content style (Summary, Teacher Style, or Professional Article)
5. Click "Transform Content" and wait for the AI to process the video
6. View and copy your generated summary

## 🔧 Requirements

- Python 3.9 or higher
- Google Gemini API key (stored in .env file)
- Internet connection for accessing YouTube and the Gemini API
- Modern web browser (Chrome, Firefox, Safari, Edge)

## 🧰 Development

SummrPro is built with the following technologies:

- **Backend**: Python with Flask framework
- **AI**: Google's Gemini 1.5 Pro model
- **Frontend**: HTML, JavaScript, and Tailwind CSS
- **API**: youtube_transcript_api for fetching YouTube subtitles
- **Containerization**: Docker for cross-platform deployment

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

<p align="center">
  <a href="https://www.buymeacoffee.com/ehabkahwati" target="_blank">
    <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" height="50px">
  </a>
</p>

As an independent developer, I dedicate my time to building and maintaining various open-source web applications and Chrome extensions that are freely available to everyone. Your support helps me:

- ✨ Continue developing new features for SummrPro
- 🐛 Fix bugs and maintain existing projects
- 🚀 Create new open-source tools for the community
- 💡 Explore innovative ideas and technologies

Even a small contribution goes a long way in supporting the development of tools that make the internet more accessible and useful for everyone.

**Thank you for your support!** ❤️

---

Made with ❤️ by Ehab Kahwati
