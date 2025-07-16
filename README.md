# Sales Report API 📊

A FastAPI application that converts CSV sales data into professional PDF reports.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://docker.com)

---

## 🎯 **What it does**

This API takes a CSV file with sales data and generates a professional PDF report with:
- Summary statistics (total items, revenue)
- Detailed sales table
- Bar chart visualization
- Professional formatting

Perfect for automating sales reporting workflows.

---

## 🚀 **Quick Start**

### **Using Docker (Recommended)**

```bash
# Clone the repository
git clone https://github.com/your-username/sales-report-api.git
cd sales-report-api

# Run with Docker Compose
docker-compose up -d

# Test the API
curl http://localhost:8000/
```

### **Local Development**

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn app.main:app --reload

# Open browser
open http://localhost:8000/docs
```

---

## 📊 **API Endpoints**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/api/v1/reports/generate` | GET | Generate PDF from CSV |
| `/api/v1/reports/download/{filename}` | GET | Download specific report |
| `/api/v1/reports/list` | GET | List all reports |

**Interactive documentation:** `http://localhost:8000/docs`

---

## 📁 **CSV Format**

Place your CSV file in the `data/` directory as `ventas.csv`:

```csv
Producto,Cantidad,Precio
Laptop Dell XPS 13,5,1200.00
Mouse Logitech,10,25.50
Teclado Mecánico,3,89.99
```

**Supported columns:**
- `Producto` / `Product` - Product name
- `Cantidad` / `Quantity` - Quantity sold
- `Precio` / `Price` - Unit price

---

## 🏗️ **Project Structure**

```
sales-report-api/
├── app/
│   ├── main.py              # FastAPI application
│   ├── models/              # Pydantic models
│   ├── services/            # Business logic
│   ├── routers/             # API endpoints
│   └── config/              # Settings
├── data/                    # CSV input files
├── reports/                 # Generated PDF reports
├── tests/                   # Unit tests
├── requirements.txt         # Python dependencies
├── Dockerfile              # Container configuration
└── docker-compose.yml     # Multi-container setup
```

---

## 🧪 **Testing**

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app

# Test the API manually
curl -X GET "http://localhost:8000/api/v1/reports/generate"
```

---

## 🔧 **Features**

- ✅ **FastAPI** - Modern, fast web framework
- ✅ **PDF Generation** - Professional reports with ReportLab
- ✅ **Data Validation** - Input validation with Pydantic
- ✅ **Interactive Docs** - Automatic OpenAPI/Swagger documentation
- ✅ **Docker Support** - Containerized deployment
- ✅ **Error Handling** - Comprehensive error responses
- ✅ **CORS Enabled** - Ready for frontend integration

---

## 🐳 **Docker Usage**

```bash
# Build image
docker build -t sales-report-api .

# Run container
docker run -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/reports:/app/reports \
  sales-report-api

# Using docker-compose (easier)
docker-compose up -d
```

---

## 🔨 **Development**

### **Adding new features**

1. **Models**: Add new Pydantic models in `app/models/`
2. **Services**: Business logic goes in `app/services/`
3. **Endpoints**: API routes in `app/routers/`
4. **Tests**: Add tests in `tests/`

### **Code quality**

```bash
# Format code
black app/

# Lint code
flake8 app/

# Type checking
mypy app/
```

---

## 📈 **Example Usage**

### **Generate Report**

```bash
# Generate a new report
curl -X GET "http://localhost:8000/api/v1/reports/generate"

# Response
{
  "filename": "sales_report_20241201_143022.pdf",
  "generated_at": "2024-12-01T14:30:22.123456",
  "items_count": 4,
  "total_revenue": 1615.47,
  "download_url": "/api/v1/reports/download/sales_report_20241201_143022.pdf"
}
```

### **Download Report**

```bash
# Download the generated PDF
curl -O "http://localhost:8000/api/v1/reports/download/sales_report_20241201_143022.pdf"
```

---

## 🛠️ **Configuration**

Environment variables (optional):

```bash
DEBUG=false                    # Enable debug mode
ALLOWED_ORIGINS=*             # CORS allowed origins
MAX_FILE_SIZE=10485760        # Max CSV file size (10MB)
```

---

## 📝 **Sample Output**

The generated PDF includes:

1. **Header** - "Sales Report" title
2. **Summary Table** - Total items, revenue, generation date
3. **Detailed Table** - Product, quantity, price, total for each item
4. **Bar Chart** - Visual representation of quantities sold

---

## ⚠️ **Limitations**

- CSV files must be under 10MB
- Only supports CSV input format
- Reports are stored locally (not in database)
- Single CSV file processing at a time

---

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 **Author**

**Victor Velazquez** - [vvelc](https://github.com/vvelc)

*Built with FastAPI and ReportLab for efficient sales reporting automation.*

---

## 🔗 **Links**

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [ReportLab Documentation](https://www.reportlab.com/docs/)
- [Docker Documentation](https://docs.docker.com/)

---

**⭐ If this project helped you, please give it a star!**