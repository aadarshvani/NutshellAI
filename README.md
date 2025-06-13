# 🥜 Nutshell - AI Content Summarizer

A modular Streamlit application that summarizes YouTube videos and web articles using AI.

## 🚀 Features

- **Multi-source Support**: YouTube videos and web articles
- **Multiple AI Models**: Gemma2, Llama3.1, Mixtral via Groq API
- **Various Summary Formats**: Structured, bullet points, paragraph, executive
- **Configurable Word Limits**: 100-1000 words
- **Caching**: Improved performance with content caching
- **History**: Track recent summaries
- **Modern UI**: Clean, responsive Streamlit interface

## 📁 Project Structure

```
nutshell/
├── main.py                 # Main application entry point
├── requirements.txt        # Python dependencies
├── config/
│   └── settings.py        # App configuration
├── core/
│   ├── validators.py      # Input validation
│   ├── content_loader.py  # Content loading logic
│   └── summarizer.py      # AI summarization
└── ui/
    └── components.py      # UI components
```

## 🛠️ Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd nutshell
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up API key** (Optional)
Create `.streamlit/secrets.toml`:
```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

4. **Run the application**
```bash
streamlit run main.py
```

## 🔧 Usage

1. **Get Groq API Key**: Visit [console.groq.com](https://console.groq.com/keys)
2. **Enter API Key**: In the sidebar configuration
3. **Choose Settings**: Select AI model, format, and word limit
4. **Enter URL**: Paste YouTube video or article URL
5. **Generate Summary**: Click "Summarize" button

## 🏗️ Architecture

### Modular Design
- **Separation of Concerns**: UI, business logic, and configuration are separated
- **Easy Maintenance**: Each module has a specific responsibility
- **Scalable**: Easy to add new features or modify existing ones

### Key Components
- **Config**: Centralized settings and constants
- **Validators**: Input validation and sanitization
- **Content Loader**: Handles YouTube and web content loading
- **Summarizer**: AI-powered summarization using LangChain
- **UI Components**: Reusable UI elements

## 🔄 Improvements Made

### Fixed Issues from Original Code:
1. **Deprecated Methods**: Replaced `chain.run()` with `chain.invoke()`
2. **Security**: Proper API key handling with secrets
3. **URL Validation**: Better YouTube URL detection
4. **Error Handling**: Specific error messages for different scenarios
5. **SSL Security**: Enabled SSL verification
6. **Performance**: Added caching for content loading
7. **Code Organization**: Modular structure with separated concerns

## 📝 License

MIT License - Feel free to use and modify as needed.