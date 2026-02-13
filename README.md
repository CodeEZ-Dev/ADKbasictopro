# 🏗️ ADR Analysis Engine

> **Comprehensive Architecture Decision Records Analysis & Template Generation Platform**

A sophisticated full-stack application that performs **9-phase analysis** of Architecture Decision Records (ADRs), generates professional ADR templates from JIRA, detects AI-generated content, and provides TOGAF-aligned enterprise architecture recommendations.

[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/)
[![React 18+](https://img.shields.io/badge/react-18%2B-61dafb)](https://react.dev)
[![FastAPI](https://img.shields.io/badge/fastapi-0.104%2B-009688)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## ✨ Key Features

### 🔬 9-Phase Analysis Engine
Comprehensive multi-dimensional analysis of ADRs:

| Phase | Focus | Outputs |
|-------|-------|---------|
| 1️⃣ **Structural** | Section validation & completeness | Structural quality score, missing sections |
| 2️⃣ **Quality** | 5 quality dimensions | Clarity, completeness, traceability, consistency, justification scores |
| 3️⃣ **LLM Detection** | AI-generated content patterns | Confidence score, indicators list |
| 4️⃣ **Improvements** | Actionable suggestions | Prioritized recommendations with examples |
| 5️⃣ **Enterprise** | TOGAF-aligned architecture | 6 strategic categories with guidance |
| 6️⃣ **Design Patterns** | Applicable patterns | 6 pattern categories with 25+ specific patterns |
| 7️⃣ **Tech Debt** | Debt identification | 7 debt types with severity levels |
| 8️⃣ **Maturity** | Architecture maturity | Maturity level, dimensions, improvement pathway |
| 9️⃣ **Compliance** | 24-point standard | Compliance score, topic status |

### 🔌 JIRA Integration
- 🔗 Real-time API integration (Atlassian Cloud)
- 💾 Cached issue storage
- 🔄 Manual fallback input
- 📊 Issue tracking and sync status

### 🤖 AI-Powered Template Generation
- **OpenAI GPT-4** integration for smart templates
- **Rule-based fallback** without API key
- **24 standard sections** pre-populated
- 📋 Copy to clipboard, markdown download

### 👁️ Professional UI/UX
- 📑 Tab-based interface (Analyze | Generate)
- 🎯 Real-time "thinking process" visualization
- 📊 Score badges with visual progress
- 🎨 Beautiful gradient design
- 📱 Fully responsive

## 🚀 Quick Start (5 Minutes)

### Prerequisites
```bash
# Check versions
python --version  # 3.8+
npm --version     # 16+
```

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env      # Configure your API keys
python main.py            # Runs on http://localhost:8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev               # Runs on http://localhost:3000
```

**Open http://localhost:3000** 🎉

## 📊 Architecture

```
┌─────────────────────────────────────────┐
│   React Frontend (Vite)                 │
│  ├─ Analyze Tab (Upload/Paste)         │
│  └─ Generate Tab (JIRA/Manual)         │
└──────────────────┬──────────────────────┘
                   │ REST API
┌──────────────────┴──────────────────────┐
│   FastAPI Backend (Python)              │
│  ├─ Analysis Service (9-phase engine)   │
│  ├─ Template Service (GPT-4 powered)    │
│  └─ JIRA Service (Atlassian API)        │
└──────────────────┬──────────────────────┘
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
    PostgreSQL  Files    JIRA API
```

## 📁 Project Structure

```
ADKbasictopro/
├── backend/
│   ├── main.py                           # FastAPI app
│   ├── config.py                         # Configuration
│   ├── models.py                         # Database models
│   ├── requirements.txt                  # Dependencies
│   ├── Dockerfile                        # Container image
│   ├── services/
│   │   └── adr_analysis_engine.py       # 9-phase analysis (600+ lines)
│   └── routers/
│       ├── analysis.py                   # Analysis endpoints
│       ├── templates.py                  # Template endpoints
│       └── jira.py                      # JIRA endpoints
│
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   ├── Dockerfile
│   ├── index.html
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       ├── api/index.js                  # API client
│       ├── components/
│       │   ├── ScoreBadge.jsx           # Score display
│       │   └── AnalysisResults.jsx      # Results panel
│       ├── tabs/
│       │   ├── AnalyzeTab.jsx           # Analysis UI
│       │   └── GenerateTab.jsx          # Generation UI
│       └── styles/
│           ├── App.css
│           ├── AnalyzeTab.css
│           ├── GenerateTab.css
│           └── AnalysisResults.css
│
├── docker-compose.yml                    # Full stack compose
├── nginx.conf                            # Reverse proxy config
├── SETUP.md                              # Detailed setup guide
└── README.md                             # This file
```

## 🔑 API Endpoints (20+)

### Analysis Endpoints
```bash
POST   /api/analyze/text              # Analyze from text input
POST   /api/analyze/markdown           # Analyze from MD file
POST   /api/analyze/pdf                # Analyze from PDF
GET    /api/analysis/{id}              # Get results
GET    /api/analyses                   # List all (paginated)
DELETE /api/analysis/{id}              # Delete analysis
```

### Template Endpoints
```bash
POST   /api/templates/generate-from-jira  # Generate from JIRA
GET    /api/templates/{id}                # Get template
GET    /api/templates                     # List templates
PUT    /api/templates/{id}                # Update template
DELETE /api/templates/{id}                # Delete template
```

### JIRA Endpoints
```bash
GET    /api/jira/issues/{key}         # Fetch JIRA issue
GET    /api/jira/issues/cached        # List cached issues
POST   /api/jira/test-connection      # Test JIRA API
GET    /api/jira/config-status        # Check configuration
```

### System Endpoints
```bash
GET    /health                         # Health check
GET    /docs                          # Swagger UI
GET    /redoc                         # ReDoc
```

## 🧠 What Each Analysis Phase Does

### Phase 1: Structural Analysis
```
Validates mandatory sections:
✓ Title          ✓ Status         ✓ Context
✓ Decision       ✓ Consequences

Rates structure quality (0-100)
Identifies optional sections
```

### Phase 2: Quality Assessment
```
Completeness:   0-100   (Section depth)
Clarity:        0-100   (Readability)
Traceability:   0-100   (References)
Consistency:    0-100   (Coherence)
Justification:  0-100   (Decision rationale)
→ Overall:      0-100
```

### Phase 3: LLM Detection
```
Analyzes:
✓ Generic phrase frequency
✓ Repetitive structures
✓ Grammatical consistency
✓ Corporate jargon usage

→ Confidence: 0-100
→ Indicators: List of AI-like patterns
```

### Phase 4: Improvement Suggestions
```
Provides:
✓ Structural recommendations
✓ Missing section filling
✓ Quality enhancements
✓ Specific examples
✓ Implementation guidance

Prioritized: High → Medium → Low
```

### Phase 5: Enterprise Architecture (TOGAF)
```
Six Categories:
1. Strategic Alignment   (Business goals)
2. Governance           (Approval structures)
3. Integration          (System dependencies)
4. Security            (Threat mitigation)
5. Scalability         (Growth planning)
6. Data Management     (Information architecture)
```

### Phase 6: Design Patterns
```
25+ Patterns across 6 categories:

Architectural:  Microservices, Layered, Event-Driven
Integration:    API Gateway, Service Mesh
Data:          Event Sourcing, CQRS
Resilience:    Circuit Breaker, Bulkhead
Security:      Auth, Encryption
Scalability:   Horizontal, Caching, Load Balancing
```

### Phase 7: Technical Debt
```
7 Debt Types with severity:
- Code Debt         (Messy code)
- Architectural     (Wrong structure)
- Design           (Wrong patterns)
- Documentation    (Missing docs)
- Test             (Low coverage)
- Infrastructure   (Legacy systems)
- Knowledge        (Org gaps)
```

### Phase 8: Maturity Scoring
```
Assesses across 4 dimensions:

Documentation Quality    0-100
Decision Rationale      0-100
Risk Assessment         0-100
Alternative Analysis    0-100

Maturity Levels:
Initial    (0-20%)    Developing (20-40%)
Defined    (40-60%)   Managed     (60-80%)
Optimizing (80-100%)
```

### Phase 9: Standards Compliance
```
Evaluates against 24 topics:

✓ Title, Status, Context, Decision, Consequences
✓ Alternatives, Assumptions, Constraints
✓ Risks, Stakeholders, Timeline, Metrics
✓ Dependencies, Costs, Security, Compliance
✓ Scalability, Performance, Testing
✓ Rollback, Monitoring, Documentation, Reviews

→ Compliance Score: 0-100%
→ Missing Topics: List
→ Priority Improvements: Top 5
```

## 🔧 Configuration

### Environment Variables

**Backend (.env)**
```env
# OpenAI (Optional)
OPENAI_API_KEY=sk-proj-...
OPENAI_MODEL=gpt-4

# Database
DATABASE_URL=postgresql://user:pass@localhost/adr_analyzer
DATABASE_POOL_SIZE=5

# JIRA (Optional)
JIRA_API_URL=https://your-jira.atlassian.net
JIRA_API_TOKEN=...
JIRA_USERNAME=...@company.com

# Server
DEBUG=False
LOG_LEVEL=INFO
CORS_ORIGINS=["http://localhost:3000"]
```

**Frontend (.env.local)**
```env
VITE_API_URL=http://localhost:8000/api
```

## 🐳 Docker Deployment

### One-Command Deployment
```bash
docker-compose up -d
```

Runs:
- PostgreSQL database
- FastAPI backend (port 8000)
- React frontend (port 3000)
- Nginx reverse proxy (port 80/443)

All health checks configured ✓

## 📚 Example Usage

### Analyze an ADR
```bash
curl -X POST http://localhost:8000/api/analyze/text \
  -F "content=# ADR-001: Use Microservices\n\n## Status\nProposed\n\n..."
```

### Generate from JIRA
```bash
curl -X POST http://localhost:8000/api/templates/generate-from-jira \
  -F "jira_ticket_id=PROJ-123" \
  -F "user_context=Additional context..."
```

## 📈 Performance

- **Analysis Speed**: <1 second for typical ADRs
- **File Handling**: Supports PDFs up to 50MB
- **Concurrent Users**: 100+ with connection pooling
- **Database**: Indexed queries for fast retrieval
- **Caching**: Redis-ready for production

## 🔐 Security

- ✅ CORS protection
- ✅ Environment variable secrets
- ✅ Secure API token handling
- ✅ Database connection pooling
- ✅ Rate limiting ready
- ✅ HTTPS/SSL support
- ✅ Non-root Docker containers

## 🧪 Testing

```bash
# Backend tests
cd backend
pip install pytest
pytest -v

# Frontend tests
cd frontend
npm test -- --coverage
```

## 📖 Documentation

- **[SETUP.md](SETUP.md)** - Detailed setup & deployment guide
- **[API Docs](http://localhost:8000/docs)** - Interactive Swagger UI
- **[ReDoc](http://localhost:8000/redoc)** - Alternative API documentation

## 🛠️ Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Backend** | FastAPI | 0.104+ |
| **Runtime** | Python | 3.11+ |
| **Database** | PostgreSQL | 15+ |
| **Frontend** | React | 18+ |
| **Build** | Vite | 5+ |
| **Styling** | Tailwind CSS | 3.4+ |
| **API Client** | Axios | 1.6+ |
| **ORM** | SQLAlchemy | 2+ |
| **AI** | OpenAI API | Latest |

## 🚧 Roadmap

- [ ] Multi-language ADR support
- [ ] Custom scoring rubrics
- [ ] Team collaboration (comments, reviews)
- [ ] ADR version history & diffing
- [ ] Git repository integration
- [ ] Automated CI/CD gates
- [ ] Advanced dashboards
- [ ] Bulk operations
- [ ] Custom compliance rules
- [ ] Slack/Teams integration

## 🤝 Contributing

1. Fork the repository
2. Create branch: `git checkout -b feature/amazing-feature`
3. Commit: `git commit -m 'Add amazing feature'`
4. Push: `git push origin feature/amazing-feature`
5. Open Pull Request

## 📄 License

MIT License - Free for commercial and personal use

## 📞 Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/CodeEZ-Dev/ADKbasictopro/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/CodeEZ-Dev/ADKbasictopro/discussions)
- 📧 **Email**: contact@example.com

## 📚 Resources

- [ADR Documentation](https://adr.github.io/)
- [TOGAF Standard](https://www.opengroup.org/togaf)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev)

---

<div align="center">

**Built with ❤️ for Enterprise Architecture Teams**

[⭐ Star us on GitHub](https://github.com/CodeEZ-Dev/ADKbasictopro) | [📖 Full Documentation](./SETUP.md) | [🐛 Report Issues](https://github.com/CodeEZ-Dev/ADKbasictopro/issues)

</div>
