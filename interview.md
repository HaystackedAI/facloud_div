***Polished Interview Answer – Data Ingestion & Indexing***

For data ingestion, we use a time-triggered Azure Function App that runs daily at 4:00 AM to ensure fresh dividend data for the upcoming four-week window.

The function invokes a FastAPI backend responsible for orchestrating the data pipeline. The backend first retrieves dividend schedules from Nasdaq APIs, and for each dividend record, it calls Finnhub to enrich the data with market capitalization and the previous trading day’s closing price.

We apply business filters early in the pipeline, excluding companies with a market capitalization below $1B to ensure data relevance and reduce downstream processing cost.

After validation and filtering, we normalize and persist the structured dividend data into PostgreSQL, which acts as the system of record.

For GenAI use cases, the backend transforms each dividend record into a semantic chunk, combining key attributes such as company name, dividend date, yield, market cap, and price context.

These chunks are embedded using Azure OpenAI embedding models, and the resulting vectors are stored in pgvector for traceability and versioning.

Finally, the embedded documents are indexed into Azure Cognitive Search, enabling semantic and vector search for downstream RAG workflows.



