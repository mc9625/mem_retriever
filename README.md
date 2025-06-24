# 🧠 Declarative Memory API Plugin

A powerful REST API plugin for **Cheshire Cat AI** that provides direct access to declarative memory without LLM overhead.

## 🚀 Features

- **🔍 Direct Memory Access**: Query declarative memory without using the LLM for maximum performance
- **🌐 RESTful API**: Standard GET and POST endpoints with JSON responses
- **🎛️ Advanced Filtering**: Search by metadata, similarity scores, and content patterns
- **⚙️ Highly Configurable**: Customizable thresholds, limits, and behaviors
- **🛡️ Secure**: Built-in authentication and authorization
- **⚡ High Performance**: Fast responses with detailed timing metrics
- **📊 Rich Metadata**: Comprehensive information about embeddings and search parameters

## 📦 Installation

1. Download or clone this plugin to your Cheshire Cat's `/plugins` folder
2. Restart your Cheshire Cat instance
3. Configure plugin settings via the admin interface at `/admin`
4. Start making API calls!

## 🔧 Configuration

The plugin offers several configurable options in the admin interface:

| Setting | Default | Range | Description |
|---------|---------|-------|-------------|
| **Default number of results** | 5 | 1-50 | Default number of results to return |
| **Default similarity threshold** | 0.7 | 0.0-1.0 | Default similarity threshold for results |
| **Maximum number of results** | 20 | 1-100 | Maximum results that can be requested |
| **Enable metadata filters** | Yes | - | Allow filtering results by metadata |
| **Enable content preview** | Yes | - | Include content preview in results |
| **Preview length** | 200 | 50-1000 | Number of characters for content preview |

## 🌐 API Endpoints

### 1. Simple Search (GET)

```http
GET /custom/declarative-memory/search?query={query}&k={k}&threshold={threshold}
```

**Parameters:**
- `query` (required): Search query text
- `k` (optional): Number of results (default from settings)
- `threshold` (optional): Similarity threshold 0.0-1.0 (default from settings)
- `include_scores` (optional): Include similarity scores (default: true)
- `include_metadata` (optional): Include document metadata (default: true)

**Example:**
```bash
curl "https://your-cat-instance.com/custom/declarative-memory/search?query=machine%20learning&k=5&threshold=0.8"
```

### 2. Advanced Search (POST)

```http
POST /custom/declarative-memory/search
Content-Type: application/json
```

**Request Body:**
```json
{
    "query": "artificial intelligence algorithms",
    "k": 10,
    "threshold": 0.75,
    "metadata_filter": {
        "source": "research_papers.pdf",
        "category": "AI"
    },
    "include_scores": true,
    "include_metadata": true
}
```

**Example with curl:**
```bash
curl -X POST "https://your-cat-instance.com/custom/declarative-memory/search" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "neural networks deep learning",
       "k": 10,
       "threshold": 0.8,
       "metadata_filter": {"source": "*.pdf"}
     }'
```

### 3. Memory Statistics

```http
GET /custom/declarative-memory/stats
```

**Response:**
```json
{
    "user_id": "user123",
    "memory_type": "declarative",
    "timestamp": 1706123456.789,
    "total_documents": 1234,
    "collection_name": "cat_declarative_memory",
    "embedder_info": {
        "name": "text-embedding-ada-002",
        "size": 1536
    }
}
```

### 4. Collections Information

```http
GET /custom/declarative-memory/collections
```

**Response:**
```json
{
    "collections": {
        "declarative": {
            "name": "cat_declarative_memory",
            "embedder_name": "text-embedding-ada-002",
            "embedder_size": 1536,
            "description": "Long term factual memory"
        },
        "episodic": {
            "name": "cat_episodic_memory",
            "embedder_name": "text-embedding-ada-002", 
            "embedder_size": 1536,
            "description": "Conversation and interaction memory"
        },
        "procedural": {
            "name": "cat_procedural_memory",
            "embedder_name": "text-embedding-ada-002",
            "embedder_size": 1536,
            "description": "Tools and procedures memory"
        }
    },
    "user_id": "user123",
    "timestamp": 1706123456.789
}
```

### 5. Health Check

```http
GET /custom/declarative-memory/health
```

**Response:**
```json
{
    "status": "healthy",
    "service": "declarative-memory-api",
    "version": "1.0.0",
    "timestamp": "1706123456.789"
}
```

## 📊 Search Response Format

All search endpoints return results in this format:

```json
{
    "query": "machine learning",
    "results": [
        {
            "content": "Machine learning is a subset of artificial intelligence...",
            "content_preview": "Machine learning is a subset of artificial...",
            "score": 0.85,
            "metadata": {
                "source": "ML_guide.pdf",
                "page": 1,
                "category": "education",
                "when": 1706123456.789
            },
            "document_id": "doc_123"
        }
    ],
    "total_results": 5,
    "search_time_ms": 45.7,
    "parameters": {
        "k": 5,
        "threshold": 0.7,
        "metadata_filter": null,
        "include_scores": true,
        "include_metadata": true
    },
    "embedder_info": {
        "name": "text-embedding-ada-002",
        "size": 1536,
        "embedding_dimensions": 1536
    }
}
```

## 🔍 Usage Examples

### Basic Search
```bash
# Search for documents about machine learning
curl "https://your-cat-instance.com/custom/declarative-memory/search?query=machine%20learning&k=5"
```

### High Precision Search
```bash
# Search with high threshold for very relevant results
curl "https://your-cat-instance.com/custom/declarative-memory/search?query=neural%20networks&threshold=0.9&k=3"
```

### Filtered Search
```bash
# Search only in PDF documents
curl -X POST "https://your-cat-instance.com/custom/declarative-memory/search" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "python programming",
       "k": 10,
       "metadata_filter": {"source": "*.pdf"}
     }'
```

### System Status Check
```bash
# Check how many documents are in memory
curl "https://your-cat-instance.com/custom/declarative-memory/stats"
```

## 🛡️ Authentication

The plugin uses Cheshire Cat's built-in authentication system:

- **Required Permissions**: `MEMORY.READ` for all endpoints
- **Authentication Methods**: 
  - Session cookies (when logged into admin)
  - API tokens (if configured)
  - Bearer tokens (if configured)

### Using Session Authentication
If you're logged into the Cat admin interface, you can access endpoints directly in your browser:
```
https://your-cat-instance.com/custom/declarative-memory/search?query=test&k=3
```

### Using API Keys (if available)
```bash
curl -H "access_token: YOUR_API_KEY" \
     "https://your-cat-instance.com/custom/declarative-memory/search?query=test&k=3"
```

## ⚡ Performance Features

- **Direct Vector Search**: Bypasses LLM processing for optimal speed
- **Configurable Limits**: Prevent resource exhaustion with customizable limits
- **Response Timing**: Every response includes search time metrics
- **Memory Efficient**: Streaming results for large datasets
- **Similarity Thresholds**: Filter out irrelevant results automatically

## 🐛 Troubleshooting

### Common Issues

**🔒 "Permission Denied" Error**
- Ensure you're authenticated (logged into admin or using API key)
- Check that your user has `MEMORY.READ` permissions

**📭 "No Results Found"**
- Lower the similarity threshold (try 0.5 or 0.6)
- Check that documents exist in declarative memory using `/stats` endpoint
- Verify metadata filters aren't too restrictive

**⚠️ "Max Results Exceeded" Error**
- Reduce the `k` parameter in your request
- Increase `max_k` in plugin settings (admin interface)

**🐌 Slow Performance**
- Reduce the number of results requested
- Increase threshold for more selective results
- Check system load and vector database performance

### Debug Tips

1. **Check Health**: Use `/health` endpoint to verify plugin is running
2. **Inspect Stats**: Use `/stats` to see memory status and document counts
3. **Test Incrementally**: Start with simple queries and gradually add complexity
4. **Monitor Logs**: Check Cat logs for detailed error information

## 🎯 Use Cases

1. **🔍 Search Applications**: Build custom search interfaces for stored content
2. **📊 Content Analytics**: Analyze and categorize stored documents
3. **🤖 API Integrations**: Connect external systems to Cat's knowledge base
4. **🔬 Research Tools**: Fast exploration of large document collections
5. **📈 Performance Monitoring**: Direct access for system monitoring and debugging

## 🔗 Related Links

- [Cheshire Cat AI Documentation](https://cheshire-cat-ai.github.io/docs/)
- [Plugin Development Guide](https://cheshire-cat-ai.github.io/docs/plugins/)
- [REST API Documentation](http://localhost:1865/docs)
- [Vector Memory Documentation](https://cheshire-cat-ai.github.io/docs/conceptual/memory/vector_memory/)

## 📝 License

MIT License - See LICENSE file for details.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/mc9625/mem_retriever/issues)
- **Discussions**: [GitHub Discussions](https://github.com/cheshire-cat-ai/core/discussions)
- **Community**: [Discord Server](https://discord.gg/bHX5sNFCYU)

---

**Made with ❤️ for the Cheshire Cat AI community**

[![Cheshire Cat AI](https://img.shields.io/badge/Cheshire%20Cat%20AI-Plugin-purple)](https://github.com/cheshire-cat-ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-1.0.0-blue)](https://github.com/mc9625/mem_retriever)# 🧠 Declarative Memory API Plugin

Plugin per Cheshire Cat AI che espone endpoint REST per accedere direttamente alla memoria dichiarativa senza utilizzare l'LLM.

## 🚀 Caratteristiche

- **Accesso diretto**: Interroga la memoria dichiarativa senza overhead dell'LLM
- **API RESTful**: Endpoint standard GET e POST
- **Filtri avanzati**: Ricerca per metadata, punteggi di similarità, contenuto
- **Configurabile**: Soglie, limiti e comportamenti personalizzabili
- **Sicuro**: Autenticazione e autorizzazioni integrate
- **Performante**: Risposte rapide con metriche di timing

## 📦 Installazione

1. Scarica il plugin nella cartella `/plugins` del tuo Cheshire Cat
2. Riavvia il Cat
3. Configura le impostazioni del plugin dall'interfaccia web

## 🔧 Configurazione

Il plugin offre diverse opzioni configurabili:

- **Numero default di risultati**: 5 (1-50)
- **Soglia di similarità default**: 0.7 (0.0-1.0)
- **Massimo numero di risultati**: 20 (1-100)
- **Abilita filtri metadata**: Sì
- **Abilita preview contenuto**: Sì
- **Lunghezza preview**: 200 caratteri

## 🌐 Endpoint Disponibili

### 1. Ricerca Semplice (GET)

```http
GET /custom/declarative-memory/search?query=your_query&k=5&threshold=0.7
```

**Parametri:**
- `query` (obbligatorio): Query di ricerca
- `k` (opzionale): Numero di risultati
- `threshold` (opzionale): Soglia di similarità
- `include_scores` (opzionale): Includi punteggi (default: true)
- `include_metadata` (opzionale): Includi metadata (default: true)

**Esempio:**
```bash
curl "http://localhost:1865/custom/declarative-memory/search?query=machine%20learning&k=3&threshold=0.8"
```

### 2. Ricerca Avanzata (POST)

```http
POST /custom/declarative-memory/search
Content-Type: application/json
```

**Body JSON:**
```json
{
    "query": "machine learning algorithms",
    "k": 5,
    "threshold": 0.75,
    "metadata_filter": {
        "source": "research_papers",
        "category": "AI"
    },
    "include_scores": true,
    "include_metadata": true
}
```

**Esempio con curl:**
```bash
curl -X POST "http://localhost:1865/custom/declarative-memory/search" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "neural networks",
       "k": 10,
       "threshold": 0.8,
       "metadata_filter": {"type": "article"}
     }'
```

### 3. Statistiche Memoria

```http
GET /custom/declarative-memory/stats
```

**Risposta:**
```json
{
    "total_documents": 1234,
    "user_id": "user123",
    "memory_type": "declarative",
    "timestamp": 1706123456.789
}
```

### 4. Informazioni Collezioni

```http
GET /custom/declarative-memory/collections
```

**Risposta:**
```json
{
    "collections": {
        "declarative": {
            "name": "cat_declarative_memory",
            "count": 500,
            "description": "Long term factual memory"
        },
        "episodic": {
            "name": "cat_episodic_memory", 
            "count": 250,
            "description": "Conversation and interaction memory"
        },
        "procedural": {
            "name": "cat_procedural_memory",
            "count": 75,
            "description": "Tools and procedures memory"
        }
    },
    "user_id": "user123",
    "timestamp": 1706123456.789
}
```

### 5. Health Check

```http
GET /custom/declarative-memory/health
```

**Risposta:**
```json
{
    "status": "healthy",
    "service": "declarative-memory-api",
    "timestamp": "1706123456.789"
}
```

## 📊 Formato Risposta Ricerca

```json
{
    "query": "machine learning",
    "results": [
        {
            "content": "Machine learning is a subset of artificial intelligence...",
            "content_preview": "Machine learning is a subset of artificial...",
            "score": 0.85,
            "metadata": {
                "source": "ML_guide.pdf",
                "page": 1,
                "category": "education",
                "when": 1706123456.789
            },
            "document_id": "doc_123"
        }
    ],
    "total_results": 5,
    "search_time_ms": 45.7,
    "parameters": {
        "k": 5,
        "threshold": 0.7,
        "metadata_filter": null,
        "include_scores": true,
        "include_metadata": true
    }
}
```

## 🔍 Esempi di Utilizzo

### Ricerca Base
```bash
# Cerca documenti sul machine learning
curl "http://localhost:1865/custom/declarative-memory/search?query=machine%20learning&k=5"
```

### Ricerca con Filtri
```bash
# Cerca solo nei PDF
curl -X POST "http://localhost:1865/custom/declarative-memory/search" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "python programming",
       "k": 10,
       "metadata_filter": {"source": "*.pdf"}
     }'
```

### Ricerca Alta Precisione
```bash
# Cerca con soglia alta per risultati molto rilevanti
curl "http://localhost:1865/custom/declarative-memory/search?query=neural%20networks&threshold=0.9&k=3"
```

### Controllo Stato Sistema
```bash
# Verifica quanti documenti sono in memoria
curl "http://localhost:1865/custom/declarative-memory/stats"
```

## 🛡️ Sicurezza

- **Autenticazione**: Tutti gli endpoint richiedono autenticazione
- **Autorizzazioni**: Permessi `MEMORY.READ` necessari per accedere ai dati
- **Validazione**: Input sanitizzati e validati con Pydantic
- **Rate Limiting**: Limiti configurabili sui risultati

## ⚡ Performance

- **Ricerca diretta**: Bypass dell'LLM per prestazioni ottimali
- **Caching**: Working memory utilizzata per risultati frequenti
- **Metrics**: Tempo di risposta tracciato per ogni richiesta
- **Configurabile**: Parametri ottimizzabili per il tuo caso d'uso

## 🐛 Troubleshooting

### Errore "Permission Denied"
- Verifica di essere autenticato
- Controlla i permessi utente per `MEMORY.READ`

### Nessun Risultato
- Abbassa la soglia di similarità (`threshold`)
- Controlla che ci siano documenti in memoria dichiarativa
- Verifica i filtri metadata

### Errore "Max Results Exceeded"
- Il parametro `k` supera il limite configurato
- Riduci `k` o aumenta `max_k` nelle settings

### Performance Lente
- Riduci il numero di risultati richiesti
- Aumenta la soglia per risultati più selettivi
- Controlla il carico del sistema

## 📈 Casi d'Uso

1. **Search Engine**: Interfaccia di ricerca rapida per applicazioni
2. **Content Discovery**: Esplorazione di contenuti senza chat
3. **API Integration**: Integrazione con sistemi esterni
4. **Analytics**: Analisi dei contenuti memorizzati
5. **Debugging**: Ispezione diretta della memoria del Cat

## 🔗 Link Utili

- [Cheshire Cat AI Documentation](https://cheshire-cat-ai.github.io/docs/)
- [Plugin Development Guide](https://cheshire-cat-ai.github.io/docs/plugins/)
- [REST API Documentation](http://localhost:1865/docs)

## 📝 Licenza

MIT License - Vedi file LICENSE per dettagli.

## 🤝 Contributi

Contributi, issue e feature request sono benvenuti! Sentiti libero di aprire una issue o submit una pull request.

---

**Made with ❤️ for the Cheshire Cat AI community**