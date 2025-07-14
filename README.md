# 🧠 X Mention Tracker + Auto Responder

A powerful Streamlit-based application that monitors Twitter (X) for specific keywords or mentions and automatically generates AI-powered replies using OpenAI's GPT-4 model.

## 🚀 Features

- 🔍 **Real-time Tweet Monitoring** - Track recent tweets based on keywords or @mentions
- 🤖 **AI-Powered Responses** - Generate contextual replies using OpenAI's GPT-4
- 🎭 **Multiple Response Tones** - Choose from Friendly, Professional, or Funny tones
- 🛑 **Start/Stop Control** - Easy monitoring controls with session persistence
- 💬 **Interactive UI** - Clean Streamlit interface with real-time updates
- 💾 **Tweet Storage** - Automatically saves fetched tweets to JSON for persistence

## 📁 Project Structure

```
x-mention-tracker/
├── app.py              # Main Streamlit application
├── x_api.py            # Twitter API wrapper using Tweepy
├── tweets.json         # Saved recent tweets (auto-generated)
├── llm_utils.py        # Generating replies for tweets
├── requirements.txt    # Python dependencies
├── .env               # API keys (create this file)
└── README.md          # This file
```

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/x-mention-tracker.git
cd x-mention-tracker
```

### 2. Create Environment File

Create a `.env` file in the project root and add your API keys:

```env
BEARER_TOKEN=your_twitter_bearer_token
OPENAI_API_KEY=your_openai_api_key
ACCESS_TOKEN=your_twitter_access_token
ACCESS_TOKEN_SECRET=""
CLIENT_ID=""
CLIENT_SECRET=""
CONSUMER_KEY=""
CONSUMER_SECRET=""
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install tweepy streamlit openai python-dotenv
```

### 4. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 🔑 API Keys Setup

### Twitter (X) API
1. Go to [Twitter Developer Portal](https://developer.twitter.com/)
2. Create a new app or use existing one
3. Provide oAuth2.0 Permissions for the app by going to User Authentication Settings.
4. Generate a Bearer Token, Consumer Key, Consumer Key Secret, Access Token, Access Token Secret, Client Id, Client Secret
5. Add it to your `.env` file as `BEARER_TOKEN`, `CONSUMER_KEY`, `CONSUMER_KEY_SECRET`, `ACCESS_TOKEN`, `ACCESS_TOKEN_SECRET`, `CLIENT_ID`, `CLIENT_SECRET`

### OpenAI API
1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Create an API key
3. Add it to your `.env` file as `OPENAI_API_KEY`

## 📋 Requirements

- Python 3.7+
- Twitter Developer Account
- OpenAI API Account
- Active internet connection

## 💡 Usage

1. **Start the Application**: Run `streamlit run app.py`
2. **Enter Search Terms**: Input keywords or @mentions to track
3. **Select Response Tone**: Choose from Friendly, Professional, or Funny
4. **Start Monitoring**: Click "Start Monitoring" to begin tracking tweets
5. **View Results**: See real-time tweets and AI-generated responses
6. **Stop When Needed**: Use "Stop Monitoring" to pause tracking

## 🔧 Configuration

The application uses the following configuration:
- **Tweet Limit**: Fetches up to 10 recent tweets per search
- **Response Model**: OpenAI GPT-4
- **Update Interval**: Real-time monitoring with manual refresh
- **Storage**: JSON file for tweet persistence

## 🚨 Important Notes

- Keep your API keys secure and never commit them to version control
- Monitor your API usage to avoid exceeding rate limits
- The application respects Twitter's API rate limits
- OpenAI API usage will incur costs based on your plan

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🐛 Troubleshooting

### Common Issues

**API Authentication Errors**
- Verify your API keys are correctly set in the `.env` file
- Check that your Twitter app has the necessary permissions
- Ensure your OpenAI API key is active and has sufficient credits

**Rate Limit Exceeded**
- Twitter API has rate limits; wait before making new requests
- Consider implementing exponential backoff for production use

**Dependencies Issues**
- Ensure all packages are installed: `pip install -r requirements.txt`
- Check Python version compatibility (3.7+)

## 📞 Support

For issues and questions:
- Create an issue in the GitHub repository
- Check the Twitter Developer documentation
- Review OpenAI API documentation

---

**Made with ❤️ and AI**