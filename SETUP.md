# ADR Analysis Engine - Complete Setup & Deployment Guide

## 🚀 Quick Start (5 Minutes)

### Prerequisites
- Python 3.8+ 
- Node.js 16+
- PostgreSQL or SQLite

### Step 1: Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

### Step 2: Frontend Setup  
```bash
cd frontend
npm install
npm run dev
```

Visit `http://localhost:3000`

---

## 📋 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     React Frontend                          │
│  (Vite, Axios, Tailwind CSS + Custom Styles)               │
│  ├── Analyze Tab (Upload/Paste ADR)                        │
│  └── Generate Tab (Create from JIRA)                       │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP/REST
                       │
┌──────────────────────┴──────────────────────────────────────┐
│           FastAPI Backend (Python)                          │
│  ├── Analysis Router (9-phase engine)                       │
│  ├── Templates Router (ADR generation)                      │
│  └── JIRA Router (Ticket integration)                       │
└──────────────────────┬──────────────────────────────────────┘
                       │
           ┌───────────┼───────────┐
           │           │           │
           ▼           ▼           ▼
        ┌─────┐    ┌──────┐    ┌──────┐
        │ DB  │    │ Files│    │JIRA  │
        │     │    │      │    │API   │
        └─────┘    └──────┘    └──────┘
```

---

## 🔧 Detailed Configuration

### Backend Environment Variables

Create `.env` file in `backend/` directory:

```env
# ===== OPENAI CONFIGURATION =====
# Get from https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-proj-xxxxxxxxxx
OPENAI_MODEL=gpt-4

# ===== DATABASE CONFIGURATION =====
# PostgreSQL (Production)
DATABASE_URL=postgresql://user:password@localhost:5432/adr_analyzer

# SQLite (Development) - uncomment to use
# DATABASE_URL=sqlite:///./adr_analyzer.db

DATABASE_POOL_SIZE=5
DATABASE_MAX_OVERFLOW=10

# ===== JIRA CONFIGURATION (OPTIONAL) =====
# Only needed if using JIRA integration
JIRA_API_URL=https://your-jira-instance.atlassian.net
JIRA_API_TOKEN=your_pat_token_here
JIRA_USERNAME=your-email@company.com

# ===== SERVER CONFIGURATION =====
DEBUG=False  # Set to False in production
LOG_LEVEL=INFO
CORS_ORIGINS=["http://localhost:3000","https://yourdomain.com"]
```

### Frontend Environment Variables

Create `.env.local` in `frontend/` directory:

```env
VITE_API_URL=http://localhost:8000/api
```

---

## 📦 Installation Details

### Backend Dependencies

All dependencies installed via `pip install -r requirements.txt`:

```
fastapi==0.104.1          # Web framework
uvicorn==0.24.0           # ASGI server
pydantic==2.5.0           # Data validation
python-dotenv==1.0.0      # Config management
openai==1.3.0             # OpenAI API
requests==2.31.0          # HTTP library
sqlalchemy==2.0.23        # ORM
psycopg2-binary==2.9.9    # PostgreSQL driver
alembic==1.12.1           # Database migrations
python-multipart==0.0.6   # File uploads
markdown==3.5.1           # Markdown parsing
PyPDF2==3.0.1             # PDF parsing
```

### Frontend Dependencies

All dependencies installed via `npm install`:

```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "axios": "^1.6.0",
    "react-markdown": "^9.0.0"
  },
  "devDependencies": {
    "vite": "^5.0.0",
    "@vitejs/plugin-react": "^4.2.0",
    "tailwindcss": "^3.4.0"
  }
}
```

---

## 🗄️ Database Setup

### PostgreSQL Setup

```bash
# Create database
createdb adr_analyzer

# Create user (optional)
createuser -P adr_user

# Update DATABASE_URL in .env
DATABASE_URL=postgresql://adr_user:password@localhost:5432/adr_analyzer
```

### Initialize Database Tables

```bash
cd backend
python -c "from models import init_db; init_db()"
```

Tables created:
- `adr_analyses` - Analysis results
- `adr_templates` - Generated templates  
- `jira_integrations` - Cached JIRA issues

---

## 🚀 Production Deployment

### Docker Deployment

#### Backend Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Frontend Dockerfile
```dockerfile
FROM node:18-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

#### docker-compose.yml
```yaml
version: '3.8'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: adr_analyzer
      POSTGRES_USER: adr_user
      POSTGRES_PASSWORD: secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://adr_user:secure_password@postgres:5432/adr_analyzer
      OPENAI_API_KEY: ${OPENAI_API_KEY}
      DEBUG: "False"
    depends_on:
      - postgres

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend

volumes:
  postgres_data:
```

### Deploy with Docker Compose
```bash
docker-compose up -d
```

---

## 🧪 Testing

### Backend Tests
```bash
cd backend
pip install pytest pytest-httpx
pytest -v
```

### Frontend Tests
```bash
cd frontend
npm test
```

---

## 🔍 API Testing

### Using cURL

#### Analyze Text
```bash
curl -X POST http://localhost:8000/api/analyze/text \
  -F "content=# ADR Title..." \
```

#### Analyze File
```bash
curl -X POST http://localhost:8000/api/analyze/markdown \
  -F "file=@adr.md"
```

#### Generate Template
```bash
curl -X POST http://localhost:8000/api/templates/generate-from-jira \
  -F "jira_ticket_id=PROJ-123" \
  -F "user_context=Additional context..."
```

### Using Postman

1. Import API collection from Postman
2. Set `API_URL` environment variable to `http://localhost:8000/api`
3. Run requests

---

## 📊 Monitoring & Logging

### Check Logs

Backend:
```bash
# View live logs
tail -f backend.log

# Filter by level
grep ERROR backend.log
```

Frontend:
```bash
# Browser console (Press F12)
# Network tab shows all API calls
```

### API Health Check
```bash
curl http://localhost:8000/health
# Response: {"status": "healthy", "service": "ADR Analysis Engine"}
```

---

## 🔐 Security Checklist

- [ ] Set `DEBUG=False` in production
- [ ] Use strong database passwords
- [ ] Enable HTTPS/SSL
- [ ] Restrict CORS_ORIGINS
- [ ] Store OpenAI API key securely
- [ ] Use environment variables for secrets
- [ ] Implement rate limiting
- [ ] Add authentication/authorization
- [ ] Regular security audits
- [ ] Keep dependencies updated

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check Python version
python --version  # Should be 3.8+

# Check dependencies
pip list | grep -E "fastapi|sqlalchemy"

# Check port availability
lsof -i :8000
```

### Frontend won't load
```bash
# Check npm version
npm --version  # Should be 8+

# Clear cache
rm -rf node_modules package-lock.json
npm install

# Check port 3000
lsof -i :3000
```

### Database connection errors
```bash
# Test connection
psql -h localhost -U adr_user -d adr_analyzer

# Check DATABASE_URL format
# Format: postgresql://user:password@host:port/database
```

### JIRA API errors
```bash
# Test JIRA connection
curl http://localhost:8000/api/jira/test-connection

# Check credentials in .env
# Format: Basic base64(username:token)
```

---

## 📚 API Documentation

Interactive API docs available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🎯 Next Steps

1. **Complete Setup**
   - [ ] Clone repository
   - [ ] Configure .env files
   - [ ] Setup database
   - [ ] Run backend & frontend

2. **Test Features**
   - [ ] Test text analysis
   - [ ] Test file uploads
   - [ ] Test template generation
   - [ ] Test JIRA integration

3. **Customize**
   - [ ] Add your logo
   - [ ] Customize colors
   - [ ] Add custom analysis rules
   - [ ] Integrate with your systems

4. **Deploy**
   - [ ] Setup production database
   - [ ] Configure reverse proxy (nginx)
   - [ ] Setup SSL certificates
   - [ ] Deploy with Docker/K8s

---

## 📞 Support

- Check logs for detailed error messages
- Review API documentation at `/docs`
- Submit issues on GitHub
- Contact development team

---

**Last Updated**: February 2026
