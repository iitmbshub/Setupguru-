# SetupGuru AI Chat Support

Professional AI-powered chat support system for SetupGuru.shop

## Files to Upload:

### Required Files:
- `app.py` - Main Flask application
- `wsgi.py` - WSGI entry point
- `requirements.txt` - Python dependencies
- `my_data.jsonl` - Company knowledge base
- `templates/index.html` - Chat interface
- `.htaccess` - Apache configuration (if using Apache)
- `Procfile` - For Heroku deployment

### Installation:

1. Upload all files to your web server
2. Install dependencies: `pip install -r requirements.txt`
3. Set environment variable: `GEMINI_API_KEY=your_api_key`
4. Run: `python app.py` or use gunicorn for production

### Production Deployment:

**For shared hosting (cPanel):**
- Upload files to public_html or subdirectory
- Use Python app setup in cPanel
- Set environment variables in cPanel

**For VPS/Cloud:**
```bash
pip install -r requirements.txt
gunicorn wsgi:app --bind 0.0.0.0:5000
```

**For Heroku:**
```bash
git init
git add .
git commit -m "Initial commit"
heroku create your-app-name
heroku config:set GEMINI_API_KEY=your_api_key
git push heroku main
```

### Features:
- Professional AI chat interface
- Real-time responses
- Mobile responsive design
- Business-focused conversations
- Automatic sales conversion