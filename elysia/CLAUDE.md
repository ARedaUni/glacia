# Elysia: AI-Powered Information Platform for Gaza Awareness

## Overview

Elysia is an open-source agentic AI platform originally designed for intelligent data search and analysis. This documentation explains how the application works and how it can be repurposed to create a powerful platform for documenting, searching, and analyzing information about the genocide in Gaza.

### Core Architecture

**Backend**: Python FastAPI server with intelligent decision-tree architecture
**Frontend**: Next.js React application with real-time WebSocket communication
**Database**: Weaviate vector database for semantic search and data storage
**AI Integration**: Multi-provider LLM support (OpenAI, Anthropic, Gemini, etc.)

---

## Technical Architecture

### 1. Backend Structure (`/elysia/`)

#### Core Components:

**Decision Tree System** (`tree/tree.py`)
- Orchestrates AI decision-making process using two LLM models
- Base model: Handles tool selection and simple queries
- Complex model: Processes complex analytical tasks
- Persistent environment stores retrieved data across operations

**Tool System** (`tools/`)
- **Query Tool**: Hybrid/semantic/keyword search in Weaviate collections
- **Aggregate Tool**: Statistical analysis and data aggregation
- **Visualization Tool**: Generates charts and visual data representations
- **Summarization Tools**: Process and summarize large text datasets
- **Text Response Tools**: Generate contextual natural language responses

**API Layer** (`api/app.py`)
- FastAPI application with WebSocket support
- RESTful endpoints for data management
- CORS middleware for frontend communication
- Scheduled cleanup and resource monitoring

**Configuration System** (`config.py`)
- Multi-provider LLM configuration with API key management
- Environment variable support with Ansible Vault integration
- Model validation and connection testing

#### Service Managers (`api/services/`)

**UserManager**: Handles multiple users and their configurations
**TreeManager**: Manages conversation trees and context
**ClientManager**: Manages Weaviate database connections
**Automatic Cleanup**: Timeout-based resource management

### 2. Frontend Structure (`/elysia/api/static/`)

**Next.js React Application**
- Static build served by FastAPI
- Real-time WebSocket communication
- Interactive chat interface
- Data visualization components
- Collection management interface

### 3. Database Integration

**Weaviate Vector Database**
- Semantic search capabilities
- Multi-modal data storage (text, images, metadata)
- Automatic vectorization of content
- Advanced filtering and aggregation
- Schema-flexible collection management

---

## Key Features for Gaza Documentation

### 1. Intelligent Query Processing

The decision tree system can intelligently route queries about Gaza-related topics:
- **Testimonies**: Search through survivor accounts and witness statements
- **Reports**: Find specific information in human rights reports
- **Statistics**: Query demographic and casualty data
- **Timeline Events**: Locate information about specific dates or incidents
- **Geographic Data**: Search by location or region within Gaza

### 2. Multi-Modal Data Support

- **Text Documents**: Reports, testimonies, news articles, legal documents
- **Images**: Photos, satellite imagery, infographics
- **Data Visualizations**: Charts, graphs, statistical representations
- **Metadata**: Dates, locations, sources, verification status

### 3. Advanced Search Capabilities

**Semantic Search**: Find contextually related information even without exact keyword matches
**Hybrid Search**: Combines keyword and semantic search for comprehensive results
**Aggregation**: Generate statistics and summaries across large datasets
**Filtering**: Query by date ranges, geographic areas, source types, verification status

### 4. Real-Time Interaction

**WebSocket Communication**: Immediate responses and streaming results
**Conversation Context**: Maintains context across multiple queries
**Progressive Disclosure**: Builds understanding through follow-up questions
**Interactive Exploration**: Users can drill down into specific topics or sources

---

## Data Architecture for Gaza Collections

### Recommended Weaviate Schema

```json
{
  "class": "GazaTestimony",
  "properties": [
    {"name": "content", "dataType": ["text"]},
    {"name": "date", "dataType": ["date"]},
    {"name": "location", "dataType": ["string"]},
    {"name": "source", "dataType": ["string"]},
    {"name": "verified", "dataType": ["boolean"]},
    {"name": "tags", "dataType": ["string[]"]},
    {"name": "casualty_type", "dataType": ["string"]},
    {"name": "age_group", "dataType": ["string"]}
  ]
}
```

```json
{
  "class": "HumanRightsReport",
  "properties": [
    {"name": "title", "dataType": ["text"]},
    {"name": "content", "dataType": ["text"]},
    {"name": "organization", "dataType": ["string"]},
    {"name": "publication_date", "dataType": ["date"]},
    {"name": "report_type", "dataType": ["string"]},
    {"name": "key_findings", "dataType": ["text[]"]},
    {"name": "recommendations", "dataType": ["text[]"]}
  ]
}
```

---

## API Endpoints

### WebSocket Endpoints
- `/ws/query`: Real-time conversation processing for Gaza queries
- `/ws/process`: Collection preprocessing for new Gaza data

### REST Endpoints
- `/collections`: Manage Gaza-related Weaviate collections
- `/user/config`: User-specific settings and query preferences
- `/tree/config`: Conversation-specific configurations
- `/feedback`: Collect user feedback on search results and accuracy
- `/tools`: Register custom tools for Gaza-specific analysis
- `/db`: Manage saved conversations and bookmarked information

---

## Custom Tools for Gaza Analysis

### 1. Casualty Analysis Tool
```python
@tool
async def analyze_casualties(
    date_range: str,
    location: str = None,
    demographic: str = None
) -> AsyncGenerator[Result, None]:
    """Analyze casualty data within specified parameters"""
    # Query Weaviate for casualty data
    # Generate statistical summaries
    # Create visualizations
```

### 2. Timeline Generator Tool
```python
@tool
async def generate_timeline(
    start_date: str,
    end_date: str,
    event_types: List[str] = None
) -> AsyncGenerator[Result, None]:
    """Generate chronological timeline of events"""
    # Query events within date range
    # Sort chronologically
    # Format as interactive timeline
```

### 3. Source Verification Tool
```python
@tool
async def verify_sources(
    claim: str,
    min_sources: int = 3
) -> AsyncGenerator[Result, None]:
    """Cross-reference claims with multiple verified sources"""
    # Search for corroborating evidence
    # Rank sources by credibility
    # Present verification status
```

---

## Setup Instructions

### 1. Environment Setup

```bash
# Install Python dependencies
pip install -e .

# Set up environment variables
export OPENAI_API_KEY="your_api_key"
export WEAVIATE_URL="your_weaviate_instance"
export WEAVIATE_API_KEY="your_weaviate_key"
```

### 2. Database Configuration

```python
# Configure Weaviate collections for Gaza data
from elysia.preprocessing import setup_gaza_collections

await setup_gaza_collections(client)
```

### 3. Running the Application

```bash
# Start the backend server
elysia serve --port 8000

# Access the frontend
# Navigate to http://localhost:8000
```

---

## Usage Patterns for Gaza Documentation

### 1. Research Queries
- "Find testimonies from Gaza City hospitals in October 2023"
- "Show casualty statistics for children under 10"
- "What do human rights organizations say about displacement?"

### 2. Timeline Exploration
- "Create a timeline of major events in Northern Gaza"
- "Show the progression of the humanitarian crisis"
- "When did specific hospitals come under attack?"

### 3. Data Analysis
- "Aggregate casualty data by age group and location"
- "Compare international media coverage over time"
- "Analyze the impact on educational infrastructure"

### 4. Source Verification
- "Cross-reference this claim with multiple sources"
- "Show verification status of casualty figures"
- "Find primary sources for this information"

---

## Ethical Considerations

### 1. Data Accuracy
- Implement rigorous source verification
- Clearly mark unverified vs. verified information
- Provide confidence scores for claims
- Enable community fact-checking

### 2. Trauma-Informed Design
- Content warnings for graphic material
- Respectful presentation of victim information
- Support resources for users processing difficult content

### 3. Source Protection
- Anonymization options for sensitive testimonies
- Secure data storage and transmission
- Clear data retention and deletion policies

---

## Extending the Platform

### 1. Custom Tool Development
The modular tool system allows for specialized analysis tools:
- Media bias analysis
- International law compliance checking
- Geographic impact mapping
- Psychological impact assessment

### 2. Data Source Integration
- News article scrapers with verification
- Social media content analysis
- Official document processing
- Satellite imagery analysis

### 3. Visualization Extensions
- Interactive maps showing damage over time
- Demographic impact charts
- Media coverage analysis dashboards
- Source credibility networks

---

## Technical Implementation Notes

### Performance Optimization
- **Low Memory Mode**: For resource-constrained deployments
- **Caching**: Preprocessed collection summaries and frequent queries
- **Chunking**: Handles large document collections efficiently
- **Connection Pooling**: Optimized Weaviate client management

### Security Features
- **API Key Encryption**: Secure storage of LLM and database credentials
- **User Isolation**: Separate data access for different user groups
- **CORS Configuration**: Safe frontend-backend communication
- **Audit Logging**: Track all queries and data access

### Scalability
- **Microservice Architecture**: Easily deployable components
- **Async Processing**: Non-blocking query execution
- **Resource Monitoring**: Automatic cleanup and memory management
- **Multi-user Support**: Concurrent access with proper isolation

---

## Conclusion

Elysia provides a robust foundation for creating an intelligent, searchable platform for Gaza-related information. Its AI-powered decision tree architecture, combined with vector database capabilities, enables sophisticated querying and analysis of complex humanitarian data. The platform can serve as a valuable tool for researchers, journalists, human rights advocates, and anyone seeking verified information about the situation in Gaza.

By leveraging semantic search, intelligent tool selection, and real-time interaction capabilities, this platform can help make critical information more accessible and discoverable, contributing to greater awareness and understanding of the humanitarian crisis.

The modular architecture ensures the platform can evolve with new data sources, analysis tools, and user needs while maintaining accuracy, performance, and ethical standards in presenting sensitive humanitarian information.