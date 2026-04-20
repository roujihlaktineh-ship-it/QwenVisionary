# 🎨 Qwen Visionary

A powerful AI-powered chatbot application built with Streamlit that leverages the Qwen vision model to enable seamless image-to-text and text-to-image conversions.

## ✨ Features

### 📝 Image to Text (Vision Analysis)
- Upload any image (JPG, PNG, GIF, WebP format)
- Get detailed AI-powered descriptions and analysis
- Real-time streaming responses
- Maintains conversation history

### 🎨 Text to Image (Image Generation)
- Describe any image concept in natural language
- Generate images using Stable Diffusion models
- Choose between different generation models
- Fast and efficient image synthesis

### 💬 Chat Interface
- Intuitive Streamlit-based UI
- Real-time conversation history
- Easy model selection
- One-click session clearing

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Hugging Face API Token ([Get one here](https://huggingface.co/settings/tokens))

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/roujihlaktineh-ship-it/QwenVisionary.git
cd QwenVisionary
```

2. **Create a virtual environment:**
```bash
# Windows
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Linux/Mac
python -m venv .venv
source .venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Create a `.env` file in the project root:**
```env
HF_TOKEN=your_huggingface_api_token_here
```

### Run the Application

```bash
streamlit run streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`

## 📋 Project Structure

```
QwenVisionary/
├── app.py                 # Original Qwen vision script
├── streamlit_app.py       # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (add your HF_TOKEN)
├── .gitignore            # Git ignore file
└── README.md             # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxx
```

Get your token from [Hugging Face](https://huggingface.co/settings/tokens)

### Requirements

All dependencies are listed in `requirements.txt`:
- **huggingface-hub** - Access to Hugging Face models and inference API
- **python-dotenv** - Environment variable management
- **streamlit** - Web UI framework
- **pillow** - Image processing
- **requests** - HTTP library

## 💡 Usage Examples

### Image to Text
1. Open the app and select "📝 Image to Text" from the sidebar
2. Upload an image file
3. Click "🔍 Analyze Image"
4. Get detailed AI-generated description

### Text to Image
1. Select "🎨 Text to Image" from the sidebar
2. Describe what image you want to generate
3. Choose a Stable Diffusion model version
4. Click "🎨 Generate Image"
5. View the generated image

## 🤖 Models Used

- **Vision Analysis**: Qwen/Qwen3.5-9B:together
- **Text-to-Image**: Stable Diffusion v1.5 and v2.1

## ⚙️ Technical Details

### Image Processing
- Converts uploaded images to base64 format for API transmission
- Supports multiple image formats (JPG, PNG, GIF, WebP)
- Real-time streaming responses from Qwen model

### Image Generation
- Uses Hugging Face Inference API for stable diffusion models
- Handles API responses and converts to PIL Images
- Includes error handling for quota limits and permissions

### State Management
- Streamlit session state for maintaining chat history
- Persistent conversation within the session
- Easy chat history reset

## 🐛 Troubleshooting

### "HF_TOKEN not found in .env"
- Ensure `.env` file exists in the project root
- Check that `HF_TOKEN=your_token` is properly formatted
- No spaces around the `=` sign

### "Error generating image"
- Free image generation models may have rate limits
- Check Hugging Face account status and available credits
- Some models may not be available in your region
- Ensure your HF_TOKEN has the necessary permissions

### SSL Certificate Errors
- Update Python certificates: `pip install --upgrade certifi`
- Check your internet connection

## 🔐 Security

⚠️ **Important**: Never commit your `.env` file to version control. It's already listed in `.gitignore`.

## 📝 API Notes

- Qwen Model: Available through Together AI partnership
- Image Generation: Uses free Stable Diffusion models
- Rate limits may apply based on your Hugging Face account tier

## 🤝 Contributing

Contributions are welcome! Feel free to:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Push to your fork
5. Create a pull request

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

**Rooji Hlaktineh**
- GitHub: [@roujihlaktineh-ship-it](https://github.com/roujihlaktineh-ship-it)

## 🙏 Acknowledgments

- [Hugging Face](https://huggingface.co) for hosting models and inference API
- [Streamlit](https://streamlit.io) for the amazing web framework
- [Alibaba](https://www.alibabacloud.com/) for the Qwen model
- [Stability AI](https://stability.ai/) for Stable Diffusion models

## 📞 Support

For issues, questions, or suggestions:
1. Check existing GitHub issues
2. Create a new issue with detailed description
3. Include error messages and steps to reproduce

## 🎯 Roadmap

- [ ] Add video frame analysis
- [ ] Implement batch image processing
- [ ] Support for more image generation models
- [ ] Custom model fine-tuning options
- [ ] Export chat history as PDF
- [ ] Multi-language support

---

**Enjoy creating with Qwen Visionary!** 🚀
