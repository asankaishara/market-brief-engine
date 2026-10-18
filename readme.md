## Set python in Intelij Idea
- Project Structure ->  Project Settings -> Project,
  - set, SDK: select the <path>\market-brief-engine\.venv
- Platform Settings -> SDKs, remove java 25, only keep python .venv
- Once this is done, when you open terminal in intelij idea, it will automatically activate the python environment

## Install python dependencies
- Upgrade pip -> python -m pip install --upgrade pip
- Install requirements -> pip install -r requirements.txt

## Run the FastAPI app using uvicorn
- uvicorn app.main:app --reload
- application swagger url: http://127.0.0.1:8000/docs

## Run DB server
- Make sure docker desktop is up and running
- Run ```docker compose up -d```
- Verify the container ```docker compose ps```

## Test DB connection from the app
- In python console
```
  from app.db.session import engine;
  conn = engine.connect();
  print('Database connection successful:', conn.closed == 0);
  conn.close()
```

## DB details for clients to connect
- url: jdbc:postgresql://localhost:5432/market_db
- username: postgres
- password: postgres

## Test fetcher service
```
  python -c "import asyncio; from app.services.fetcher import DataFetcherService; service = DataFetcherService(); print(asyncio.run(service.fetch_rss_or_api('AAPL')))"
```

## Test local ollama call with embedding service
```
  python -c "import asyncio; from app.services.embedder import EmbeddingService; svc = EmbeddingService(); print(asyncio.run(svc.get_embedding('Testing GPU embedding generation'))[:5])"
```

## Test ingestion service
```
  python -c "import asyncio; from app.db.session import SessionLocal; from app.services.ingestion import IngestionPipeline; db = SessionLocal(); pipeline = IngestionPipeline(db); print('New articles ingested:', asyncio.run(pipeline.ingest_ticker_news('AAPL'))); db.close()"
```

## Test vector search from the swagger UI
- Payload to try
```
  {
  "query": "earnings growth and cloud adoption",
  "ticker": "MU",
  "top_k": 2
  }
```

## It is important to understand vector operations
- <=>	Cosine Distance
- <->	Euclidean / L2 Distance
- <#>	Negative Inner Product
- <+>	L1 / Taxicab Distance
- <~>	Hamming Distance
- <%>	Jaccard Distance
