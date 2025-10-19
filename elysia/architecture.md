# Elysia Backend Architecture

## Overview

Elysia is an agentic framework powered by decision trees that dynamically selects and executes tools based on user input and environmental context. The system is designed to work with Weaviate vector databases and LLMs to provide intelligent data retrieval and processing capabilities.

## High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    CLIENT INTERFACE                                         │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│  ┌────────────────────┐  ┌────────────────────┐  ┌──────────────────────────────────────┐  │
│  │   Web Browser      │  │   Python Client    │  │   API Clients (REST/WebSocket)       │  │
│  │  (Frontend UI)     │  │   (SDK Usage)      │  │   (Direct API Access)                │  │
│  └────────────────────┘  └────────────────────┘  └──────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
                                      │  │  │
                                      ▼  ▼  ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                               API GATEWAY & ROUTING                                     │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│  ┌────────────────────┐  ┌────────────────────┐  ┌──────────────────────────────────────┐  │
│  │   FastAPI          │  │   WebSocket        │  │   REST Endpoints                   │  │
│  │   Application      │  │   Connections      │  │   (HTTP Routes)                    │  │
│  │                    │  │   (Real-time)      │  │                                    │  │
│  │  - /init           │  │  - /ws/query       │  │  - /collections                    │  │
│  │  - /ws             │  │  - /ws/processor   │  │  - /user/config                    │  │
│  │  - /collections    │  │                    │  │  - /tree/config                    │  │
│  │  - /user/config    │  │                    │  │  - /feedback                       │  │
│  │  - /tree/config    │  │                    │  │  - /utils                          │  │
│  │  - /feedback       │  │                    │  │  - /tools                          │  │
│  │  - /utils          │  │                    │  │  - /db                             │  │
│  │  - /tools          │  │                    │  │                                    │  │
│  │  - /db             │  │                    │  │                                    │  │
│  └────────────────────┘  └────────────────────┘  └──────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
                                      │  │  │
                                      ▼  ▼  ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                           USER SESSION MANAGEMENT                                       │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐  │
│  │              UserManager (Singleton)                                                │  │
│  │  ┌─────────────────────────────────────────────────────────────────────────────┐  │  │
│  │  │  User Sessions                                                              │  │  │
│  │  │  - Session tracking                                                         │  │  │
│  │  │  - User configurations                                                     │  │  │
│  │  │  - API key management                                                       │  │  │
│  │  │  - Resource allocation                                                      │  │  │
│  │  └─────────────────────────────────────────────────────────────────────────────┘  │  │
│  │                                                                                     │  │
│  │  ┌─────────────────────────────────────────────────────────────────────────────┐  │  │
│  │  │              TreeManager                                                    │  │  │
│  │  │  - Manages multiple conversation trees per user                             │  │  │
│  │  │  - Tree lifecycle management                                                │  │  │
│  │  │  - Memory management                                                        │  │  │
│  │  │  - Timeout handling                                                         │  │  │
│  │  └─────────────────────────────────────────────────────────────────────────────┘  │  │
│  │                                                                                     │  │
│  │  ┌─────────────────────────────────────────────────────────────────────────────┐  │  │
│  │  │              ClientManager                                                  │  │  │
│  │  │  - Weaviate connections                                                     │  │  │
│  │  │  - LLM API connections                                                      │  │  │
│  │  │  - Connection pooling                                                        │  │  │
│  │  │  - Resource recycling                                                       │  │  │
│  │  └─────────────────────────────────────────────────────────────────────────────┘  │  │
│  └─────────────────────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                            DECISION TREE ENGINE                                             │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐  │
│  │              Tree (Core Decision Engine)                                           │  │
│  │  ┌─────────────────────────────────────────────────────────────────────────────┐  │  │
│  │  │  Decision Nodes                                                             │  │  │
│  │  │  - Branching logic                                                          │  │  │
│  │  │  - Tool selection                                                           │  │  │
│  │  │  - Routing decisions                                                        │  │  │
│  │  └─────────────────────────────────────────────────────────────────────────────┘  │  │
│  │                                                                                     │  │
│  │  ┌─────────────────────────────────────────────────────────────────────────────┐  │  │
│  │  │  TreeData                                                                   │  │  │
│  │  │  - Environmental context                                                    │  │  │
│  │  │  - Conversation history                                                      │  │  │
│  │  │  - Collection metadata                                                       │  │  │
│  │  │  - Task completion tracking                                                 │  │  │
│  │  └─────────────────────────────────────────────────────────────────────────────┘  │  │
│  │                                                                                     │  │
│  │  ┌─────────────────────────────────────────────────────────────────────────────┐  │  │
│  │  │  Tools Registry                                                             │  │  │
│  │  │  - Available tools                                                           │  │  │
│  │  │  - Tool configurations                                                      │  │  │
│  │  │  - Tool availability logic                                                   │  │  │
│  │  └─────────────────────────────────────────────────────────────────────────────┘  │  │
│  │                                                                                     │  │
│  │  ┌─────────────────────────────────────────────────────────────────────────────┐  │  │
│  │  │  Language Models                                                             │  │  │
│  │  │  - Base LM (fast, lightweight)                                              │  │  │
│  │  │  - Complex LM (accurate, heavyweight)                                       │  │  │
│  │  │  - DSPy integration                                                         │  │  │
│  │  └─────────────────────────────────────────────────────────────────────────────┘  │  │
│  └─────────────────────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 TOOL ECOSYSTEM                                            │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│  ┌────────────────────┐  ┌────────────────────┐  ┌────────────────────┐  ┌─────────────────┐ │
│  │   Retrieval        │  │   Aggregation      │  │   Visualization    │  │   Text          │ │
│  │   Tools            │  │   Tools            │  │   Tools            │  │   Tools         │ │
│  │                    │  │                    │  │                    │  │                 │ │
│  │ - Query            │  │ - Aggregate        │  │ - Charts           │  │ - Summarizer    │ │
│  │ - Semantic Search  │  │ - Statistics       │  │ - Graphs           │  │ - Cited         │ │
│  │ - Keyword Search   │  │ - Grouping         │  │ - Plots            │  │   Summarizer    │ │
│  │ - Filtering        │  │ - Calculations     │  │ - Dashboards       │  │ - Response      │ │
│  └────────────────────┘  └────────────────────┘  └────────────────────┘  └─────────────────┘ │
│                                                                                           │
│  ┌────────────────────┐  ┌────────────────────┐  ┌────────────────────┐  ┌─────────────────┐ │
│  │   Postprocessing   │  │   Custom Tools     │  │   Preprocessing     │  │   Utilities     │ │
│  │   Tools            │  │                    │  │                    │  │                 │ │
│  │                    │  │ - User defined     │  │ - Data prep        │  │ - Helpers       │ │
│  │ - Summarization    │  │ - Extensions       │  │ - Chunking         │  │ - Parsers       │ │
│  │ - Analysis         │  │ - Plugins          │  │ - Formatting       │  │ - Validators    │ │
│  │ - Transformation   │  │                    │  │ - Optimization     │  │ - Converters    │ │
│  └────────────────────┘  └────────────────────┘  └────────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                              DATA INFRASTRUCTURE                                          │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│  ┌────────────────────┐  ┌────────────────────┐  ┌────────────────────┐  ┌─────────────────┐ │
│  │   Weaviate         │  │   LLM Providers    │  │   Collections       │  │   Storage       │ │
│  │   Vector Database  │  │                    │  │   (Processed)       │  │                 │ │
│  │                    │  │ - OpenAI           │  │                    │  │ - Trees         │ │
│  │ - Collections       │  │ - Anthropic        │  │ - Metadata         │  │ - Configs       │ │
│  │ - Vector Search     │  │ - Cohere           │  │ - Schemas          │  │ - Feedback      │ │
│  │ - CRUD Operations  │  │ - Mistral          │  │ - Summaries         │  │ - Sessions      │ │
│  │ - Aggregations     │  │ - Local Models     │  │ - Stats            │  │                 │ │
│  └────────────────────┘  └────────────────────┘  └────────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Component Breakdown

### 1. Client Interface Layer

The system supports multiple ways to interact with Elysia:

- **Web Browser**: Full-featured frontend UI built with React
- **Python Client**: SDK for programmatic access
- **API Clients**: Direct REST and WebSocket API access

### 2. API Gateway & Routing

Built with FastAPI, this layer handles:

- **WebSocket Endpoints**: Real-time communication for processing pipelines
- **REST Endpoints**: Traditional HTTP requests for configuration and management
- **Authentication & Authorization**: User session management
- **Rate Limiting**: Resource protection
- **Request Validation**: Input sanitization and validation

### 3. User Session Management

The UserManager acts as the central hub for all user-related operations:

#### UserManager
- Singleton pattern for centralized user management
- Tracks all active user sessions
- Manages user configurations and preferences
- Handles API key encryption and secure storage
- Coordinates resource allocation across users

#### TreeManager
- Manages multiple conversation trees per user
- Handles tree lifecycle (creation, deletion, persistence)
- Implements memory management strategies
- Enforces timeout policies for inactive conversations

#### ClientManager
- Manages connections to external services (Weaviate, LLMs)
- Implements connection pooling for efficiency
- Handles connection recycling and resource cleanup
- Provides abstraction layer for different service providers

### 4. Decision Tree Engine

The core intelligence of Elysia lies in its Tree-based decision-making system:

#### Tree (Core Engine)
- Implements the decision tree logic
- Coordinates between different decision nodes
- Manages conversation state and context
- Orchestrates tool execution workflows

#### Decision Nodes
- Represent branching points in the decision process
- Contain logic for selecting next actions
- Evaluate environmental context for decisions
- Maintain tool availability rules

#### TreeData
- Encapsulates the complete environmental context
- Maintains conversation history
- Tracks task completion status
- Stores collection metadata and schemas

#### Tools Registry
- Central repository of available tools
- Manages tool configurations and parameters
- Evaluates tool availability based on context
- Facilitates dynamic tool selection

### 5. Tool Ecosystem

Elysia comes with a rich set of pre-built tools:

#### Retrieval Tools
- **Query Tool**: Semantic and keyword search capabilities
- **Advanced Filtering**: Complex query construction
- **Cross-collection Search**: Unified search across multiple data sources

#### Aggregation Tools
- **Statistical Analysis**: Mean, median, mode, standard deviation
- **Data Grouping**: Category-based aggregation
- **Time Series Analysis**: Temporal data summarization

#### Visualization Tools
- **Chart Generation**: Bar charts, line graphs, pie charts
- **Dashboard Creation**: Composite visualizations
- **Interactive Elements**: Clickable and filterable visuals

#### Text Tools
- **Summarization**: Concise content summarization
- **Citation Management**: Proper attribution of sources
- **Natural Language Responses**: Human-like output generation

#### Custom Tools
- Extensible framework for user-defined functionality
- Plugin architecture for third-party integrations
- Template system for rapid tool development

### 6. Data Infrastructure

Elysia leverages modern data infrastructure for optimal performance:

#### Weaviate Vector Database
- Core data storage and retrieval system
- Vector search capabilities for semantic matching
- Schema management for structured data
- Real-time indexing and querying

#### LLM Providers
- Integration with multiple AI model providers
- Fallback mechanisms for service reliability
- Model selection based on task requirements
- Cost optimization through model tiering

#### Collections
- Pre-processed data sets optimized for Elysia
- Metadata enrichment for improved search
- Schema standardization for consistent access
- Performance optimization through indexing

#### Storage Systems
- Persistent storage for conversation trees
- Configuration management
- Feedback collection and analysis
- Session state preservation

## Data Flow

1. **User Input**: Client sends request via WebSocket/REST
2. **Session Management**: UserManager validates/creates session
3. **Tree Initialization**: TreeManager loads/creates conversation tree
4. **Context Analysis**: Tree analyzes environment and user prompt
5. **Decision Making**: Decision nodes select appropriate tools
6. **Tool Execution**: Selected tools process data/concepts
7. **Result Processing**: Results are formatted and validated
8. **Response Generation**: Output prepared for client delivery
9. **State Persistence**: Updated tree state saved for continuity
10. **Client Delivery**: Final response sent back to client

## Scalability Considerations

- **Connection Pooling**: Efficient reuse of database/LM connections
- **Memory Management**: Tree timeout and cleanup policies
- **Asynchronous Processing**: Non-blocking operations for responsiveness
- **Load Distribution**: Horizontal scaling capabilities
- **Caching Strategies**: Frequently accessed data caching
- **Resource Monitoring**: Performance metrics and alerts

## Security Features

- **API Key Encryption**: Secure storage of sensitive credentials
- **Input Validation**: Protection against malicious inputs
- **Rate Limiting**: Prevention of abuse and DOS attacks
- **Session Management**: Secure user authentication and authorization
- **Data Isolation**: Per-user data separation
- **Audit Logging**: Comprehensive activity tracking

## Extensibility Points

- **Custom Tools**: Easy addition of domain-specific functionality
- **Model Integration**: Support for new LLM providers
- **Data Connectors**: Integration with additional data sources
- **Workflow Customization**: Tailored decision tree configurations
- **Plugin Architecture**: Third-party extension support
- **Template System**: Rapid development of new components