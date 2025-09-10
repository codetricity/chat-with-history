---
theme: gaia
_class: lead
paginate: true
backgroundColor: #fff
backgroundImage: url('https://marp.app/assets/hero-background.svg')
---

![bg left:40% 80%](https://oppkey.com/static/logo.jpg)

# **Database Exploration Assignment**
## Beyond SQLite and FAISS

**Explore different databases for different use cases**

---

# Assignment Overview

## What You'll Build

A comprehensive database exploration system that:
- **Compares different databases** - SQLite, PostgreSQL, MongoDB, Elasticsearch
- **Optimizes for different use cases** - OLTP, OLAP, search, analytics
- **Implements data pipelines** - ETL processes and data synchronization
- **Benchmarks performance** - Speed, scalability, and resource usage
- **Handles different data types** - Structured, semi-structured, and unstructured
- **Provides data insights** - Analytics and reporting capabilities

---

# Problem Statement

## Database Limitations

The current FastOpp system uses SQLite and FAISS, which have limitations:
- **Scalability** - SQLite doesn't scale well for large datasets
- **Concurrency** - Limited concurrent read/write operations
- **Search capabilities** - Basic text search and vector similarity
- **Data types** - Limited support for complex data structures
- **Performance** - Not optimized for specific use cases
- **Analytics** - Limited analytical and reporting capabilities

---

# Your Solution

## Multi-Database Architecture

Create a comprehensive database system that addresses these limitations:

1. **Database Selection** - Choose the right database for each use case
2. **Data Modeling** - Design optimal schemas for different databases
3. **Performance Optimization** - Indexing, query optimization, and caching
4. **Data Synchronization** - Keep multiple databases in sync
5. **Analytics Pipeline** - Extract insights from your data
6. **Monitoring** - Track performance and usage patterns

---

# Technical Requirements

## Tech Stack

- **PostgreSQL** - Advanced relational database
- **MongoDB** - Document-based NoSQL database
- **Elasticsearch** - Full-text search and analytics
- **Redis** - In-memory caching and session storage
- **ClickHouse** - Columnar database for analytics
- **Neo4j** - Graph database for relationships
- **Apache Kafka** - Stream processing and data pipelines

---

# Database Comparison

## Use Case Matrix

| Database | Best For | Strengths | Weaknesses |
|----------|----------|-----------|------------|
| **SQLite** | Development, small apps | Simple, embedded, no setup | Limited concurrency, no network |
| **PostgreSQL** | Complex queries, ACID | Advanced SQL, JSON support | Memory usage, complexity |
| **MongoDB** | Document storage, flexibility | Schema flexibility, scaling | No joins, eventual consistency |
| **Elasticsearch** | Search, analytics | Full-text search, aggregations | Not ACID, resource intensive |
| **Redis** | Caching, sessions | Speed, data structures | Memory only, no persistence |
| **ClickHouse** | Analytics, OLAP | Columnar storage, speed | Not OLTP, limited updates |
| **Neo4j** | Graph relationships | Graph queries, relationships | Not for tabular data |

---

# Core Components

## 1. Database Connectors

```python
# src/databases/connectors.py
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import asyncio
import asyncpg
import motor.motor_asyncio
from elasticsearch import AsyncElasticsearch
import redis.asyncio as redis
import clickhouse_connect
from neo4j import AsyncGraphDatabase

class BaseDatabase(ABC):
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.client = None
    
    @abstractmethod
    async def connect(self) -> bool:
        """Connect to the database"""
        pass
    
    @abstractmethod
    async def disconnect(self) -> None:
        """Disconnect from the database"""
        pass
    
    @abstractmethod
    async def query(self, query: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Execute a query and return results"""
        pass

class PostgreSQLConnector(BaseDatabase):
    async def connect(self) -> bool:
        try:
            self.client = await asyncpg.connect(self.connection_string)
            return True
        except Exception as e:
            print(f"PostgreSQL connection failed: {e}")
            return False
    
    async def disconnect(self) -> None:
        if self.client:
            await self.client.close()
    
    async def query(self, query: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        if not self.client:
            raise ValueError("Not connected to database")
        
        rows = await self.client.fetch(query, *(params or {}).values())
        return [dict(row) for row in rows]

class MongoDBConnector(BaseDatabase):
    async def connect(self) -> bool:
        try:
            self.client = motor.motor_asyncio.AsyncIOMotorClient(self.connection_string)
            await self.client.admin.command('ping')
            return True
        except Exception as e:
            print(f"MongoDB connection failed: {e}")
            return False
    
    async def disconnect(self) -> None:
        if self.client:
            self.client.close()
    
    async def query(self, collection: str, filter: Dict[str, Any] = None, 
                   projection: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        if not self.client:
            raise ValueError("Not connected to database")
        
        db = self.client.get_default_database()
        cursor = db[collection].find(filter or {}, projection)
        return await cursor.to_list(length=None)

class ElasticsearchConnector(BaseDatabase):
    async def connect(self) -> bool:
        try:
            self.client = AsyncElasticsearch([self.connection_string])
            await self.client.ping()
            return True
        except Exception as e:
            print(f"Elasticsearch connection failed: {e}")
            return False
    
    async def disconnect(self) -> None:
        if self.client:
            await self.client.close()
    
    async def query(self, index: str, body: Dict[str, Any]) -> List[Dict[str, Any]]:
        if not self.client:
            raise ValueError("Not connected to database")
        
        response = await self.client.search(index=index, body=body)
        return [hit['_source'] for hit in response['hits']['hits']]

class RedisConnector(BaseDatabase):
    async def connect(self) -> bool:
        try:
            self.client = redis.from_url(self.connection_string)
            await self.client.ping()
            return True
        except Exception as e:
            print(f"Redis connection failed: {e}")
            return False
    
    async def disconnect(self) -> None:
        if self.client:
            await self.client.close()
    
    async def query(self, command: str, *args) -> Any:
        if not self.client:
            raise ValueError("Not connected to database")
        
        return await self.client.execute_command(command, *args)
```

---

# Core Components

## 2. Data Synchronization

```python
# src/databases/sync.py
import asyncio
from typing import Dict, Any, List
from datetime import datetime
import json

class DatabaseSynchronizer:
    def __init__(self, source_db: BaseDatabase, target_dbs: List[BaseDatabase]):
        self.source_db = source_db
        self.target_dbs = target_dbs
        self.sync_log = []
    
    async def sync_table(self, table_name: str, 
                        sync_strategy: str = 'full') -> Dict[str, Any]:
        """Synchronize a table from source to target databases"""
        sync_start = datetime.now()
        
        try:
            # Get data from source
            if sync_strategy == 'full':
                data = await self._full_sync(table_name)
            elif sync_strategy == 'incremental':
                data = await self._incremental_sync(table_name)
            else:
                raise ValueError(f"Unknown sync strategy: {sync_strategy}")
            
            # Sync to target databases
            sync_results = {}
            for target_db in self.target_dbs:
                result = await self._sync_to_target(target_db, table_name, data)
                sync_results[target_db.__class__.__name__] = result
            
            sync_end = datetime.now()
            sync_duration = (sync_end - sync_start).total_seconds()
            
            sync_info = {
                'table': table_name,
                'strategy': sync_strategy,
                'records_synced': len(data),
                'duration_seconds': sync_duration,
                'target_results': sync_results,
                'timestamp': sync_start.isoformat()
            }
            
            self.sync_log.append(sync_info)
            return sync_info
            
        except Exception as e:
            error_info = {
                'table': table_name,
                'strategy': sync_strategy,
                'error': str(e),
                'timestamp': sync_start.isoformat()
            }
            self.sync_log.append(error_info)
            raise
    
    async def _full_sync(self, table_name: str) -> List[Dict[str, Any]]:
        """Perform full table synchronization"""
        query = f"SELECT * FROM {table_name}"
        return await self.source_db.query(query)
    
    async def _incremental_sync(self, table_name: str) -> List[Dict[str, Any]]:
        """Perform incremental synchronization"""
        # Get last sync timestamp
        last_sync = await self._get_last_sync_timestamp(table_name)
        
        # Query for records modified since last sync
        query = f"""
        SELECT * FROM {table_name} 
        WHERE updated_at > %s
        ORDER BY updated_at
        """
        return await self.source_db.query(query, {'last_sync': last_sync})
    
    async def _sync_to_target(self, target_db: BaseDatabase, 
                            table_name: str, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Sync data to a specific target database"""
        start_time = datetime.now()
        
        try:
            if isinstance(target_db, MongoDBConnector):
                result = await self._sync_to_mongodb(target_db, table_name, data)
            elif isinstance(target_db, ElasticsearchConnector):
                result = await self._sync_to_elasticsearch(target_db, table_name, data)
            elif isinstance(target_db, RedisConnector):
                result = await self._sync_to_redis(target_db, table_name, data)
            else:
                result = await self._sync_to_sql(target_db, table_name, data)
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            return {
                'success': True,
                'records_processed': len(data),
                'duration_seconds': duration,
                'result': result
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'records_processed': 0
            }
    
    async def _sync_to_mongodb(self, target_db: MongoDBConnector, 
                              table_name: str, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Sync data to MongoDB"""
        db = target_db.client.get_default_database()
        collection = db[table_name]
        
        # Clear existing data
        await collection.delete_many({})
        
        # Insert new data
        if data:
            await collection.insert_many(data)
        
        return {'operation': 'insert_many', 'count': len(data)}
    
    async def _sync_to_elasticsearch(self, target_db: ElasticsearchConnector, 
                                   table_name: str, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Sync data to Elasticsearch"""
        index_name = table_name.lower()
        
        # Create index if it doesn't exist
        if not await target_db.client.indices.exists(index=index_name):
            await target_db.client.indices.create(index=index_name)
        
        # Bulk insert data
        if data:
            bulk_body = []
            for doc in data:
                bulk_body.append({
                    'index': {
                        '_index': index_name,
                        '_id': doc.get('id', doc.get('_id'))
                    }
                })
                bulk_body.append(doc)
            
            response = await target_db.client.bulk(body=bulk_body)
            return {'operation': 'bulk_insert', 'count': len(data)}
        
        return {'operation': 'bulk_insert', 'count': 0}
    
    async def _sync_to_redis(self, target_db: RedisConnector, 
                           table_name: str, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Sync data to Redis"""
        key_prefix = f"{table_name}:"
        
        # Clear existing keys
        pattern = f"{key_prefix}*"
        keys = await target_db.client.keys(pattern)
        if keys:
            await target_db.client.delete(*keys)
        
        # Set new data
        for doc in data:
            key = f"{key_prefix}{doc.get('id', doc.get('_id'))}"
            await target_db.client.set(key, json.dumps(doc))
        
        return {'operation': 'set', 'count': len(data)}
    
    async def _sync_to_sql(self, target_db: BaseDatabase, 
                          table_name: str, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Sync data to SQL database"""
        if not data:
            return {'operation': 'insert', 'count': 0}
        
        # Get column names from first record
        columns = list(data[0].keys())
        placeholders = ', '.join([f'${i+1}' for i in range(len(columns))])
        
        # Create table if it doesn't exist
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            {', '.join([f'{col} TEXT' for col in columns])}
        )
        """
        await target_db.query(create_table_query)
        
        # Insert data
        insert_query = f"""
        INSERT INTO {table_name} ({', '.join(columns)})
        VALUES ({placeholders})
        """
        
        for doc in data:
            values = [doc.get(col) for col in columns]
            await target_db.query(insert_query, values)
        
        return {'operation': 'insert', 'count': len(data)}
```

---

# Core Components

## 3. Performance Benchmarking

```python
# src/databases/benchmark.py
import asyncio
import time
from typing import Dict, Any, List
import statistics
from dataclasses import dataclass

@dataclass
class BenchmarkResult:
    operation: str
    database: str
    records: int
    duration_seconds: float
    records_per_second: float
    memory_usage_mb: float
    cpu_usage_percent: float

class DatabaseBenchmark:
    def __init__(self, databases: Dict[str, BaseDatabase]):
        self.databases = databases
        self.results = []
    
    async def benchmark_read_operations(self, table_name: str, 
                                      record_counts: List[int] = [100, 1000, 10000]) -> List[BenchmarkResult]:
        """Benchmark read operations across different databases"""
        results = []
        
        for db_name, db in self.databases.items():
            for record_count in record_counts:
                # Generate test data
                test_data = await self._generate_test_data(record_count)
                
                # Benchmark read operations
                result = await self._benchmark_read(db, table_name, test_data)
                result.database = db_name
                result.records = record_count
                results.append(result)
        
        return results
    
    async def benchmark_write_operations(self, table_name: str, 
                                       record_counts: List[int] = [100, 1000, 10000]) -> List[BenchmarkResult]:
        """Benchmark write operations across different databases"""
        results = []
        
        for db_name, db in self.databases.items():
            for record_count in record_counts:
                # Generate test data
                test_data = await self._generate_test_data(record_count)
                
                # Benchmark write operations
                result = await self._benchmark_write(db, table_name, test_data)
                result.database = db_name
                result.records = record_count
                results.append(result)
        
        return results
    
    async def benchmark_search_operations(self, table_name: str, 
                                        search_queries: List[str]) -> List[BenchmarkResult]:
        """Benchmark search operations across different databases"""
        results = []
        
        for db_name, db in self.databases.items():
            for query in search_queries:
                result = await self._benchmark_search(db, table_name, query)
                result.database = db_name
                result.records = 0  # Search results vary
                results.append(result)
        
        return results
    
    async def _benchmark_read(self, db: BaseDatabase, table_name: str, 
                            test_data: List[Dict[str, Any]]) -> BenchmarkResult:
        """Benchmark read operations for a specific database"""
        start_time = time.time()
        start_memory = self._get_memory_usage()
        start_cpu = self._get_cpu_usage()
        
        # Perform read operations
        if isinstance(db, MongoDBConnector):
            await db.query(table_name, {})
        elif isinstance(db, ElasticsearchConnector):
            await db.query(table_name, {'query': {'match_all': {}}})
        else:
            await db.query(f"SELECT * FROM {table_name}")
        
        end_time = time.time()
        end_memory = self._get_memory_usage()
        end_cpu = self._get_cpu_usage()
        
        duration = end_time - start_time
        memory_usage = end_memory - start_memory
        cpu_usage = end_cpu - start_cpu
        
        return BenchmarkResult(
            operation='read',
            database='',
            records=len(test_data),
            duration_seconds=duration,
            records_per_second=len(test_data) / duration if duration > 0 else 0,
            memory_usage_mb=memory_usage,
            cpu_usage_percent=cpu_usage
        )
    
    async def _benchmark_write(self, db: BaseDatabase, table_name: str, 
                             test_data: List[Dict[str, Any]]) -> BenchmarkResult:
        """Benchmark write operations for a specific database"""
        start_time = time.time()
        start_memory = self._get_memory_usage()
        start_cpu = self._get_cpu_usage()
        
        # Perform write operations
        if isinstance(db, MongoDBConnector):
            db_client = db.client.get_default_database()
            collection = db_client[table_name]
            await collection.insert_many(test_data)
        elif isinstance(db, ElasticsearchConnector):
            # Bulk insert to Elasticsearch
            bulk_body = []
            for doc in test_data:
                bulk_body.append({'index': {'_index': table_name}})
                bulk_body.append(doc)
            await db.client.bulk(body=bulk_body)
        else:
            # SQL insert
            if test_data:
                columns = list(test_data[0].keys())
                placeholders = ', '.join([f'${i+1}' for i in range(len(columns))])
                insert_query = f"""
                INSERT INTO {table_name} ({', '.join(columns)})
                VALUES ({placeholders})
                """
                for doc in test_data:
                    values = [doc.get(col) for col in columns]
                    await db.query(insert_query, values)
        
        end_time = time.time()
        end_memory = self._get_memory_usage()
        end_cpu = self._get_cpu_usage()
        
        duration = end_time - start_time
        memory_usage = end_memory - start_memory
        cpu_usage = end_cpu - start_cpu
        
        return BenchmarkResult(
            operation='write',
            database='',
            records=len(test_data),
            duration_seconds=duration,
            records_per_second=len(test_data) / duration if duration > 0 else 0,
            memory_usage_mb=memory_usage,
            cpu_usage_percent=cpu_usage
        )
    
    async def _benchmark_search(self, db: BaseDatabase, table_name: str, 
                              query: str) -> BenchmarkResult:
        """Benchmark search operations for a specific database"""
        start_time = time.time()
        start_memory = self._get_memory_usage()
        start_cpu = self._get_cpu_usage()
        
        # Perform search operations
        if isinstance(db, MongoDBConnector):
            await db.query(table_name, {'$text': {'$search': query}})
        elif isinstance(db, ElasticsearchConnector):
            search_body = {
                'query': {
                    'multi_match': {
                        'query': query,
                        'fields': ['*']
                    }
                }
            }
            await db.query(table_name, search_body)
        else:
            await db.query(f"""
                SELECT * FROM {table_name} 
                WHERE content ILIKE %s
            """, {'query': f'%{query}%'})
        
        end_time = time.time()
        end_memory = self._get_memory_usage()
        end_cpu = self._get_cpu_usage()
        
        duration = end_time - start_time
        memory_usage = end_memory - start_memory
        cpu_usage = end_cpu - start_cpu
        
        return BenchmarkResult(
            operation='search',
            database='',
            records=0,  # Search results vary
            duration_seconds=duration,
            records_per_second=0,
            memory_usage_mb=memory_usage,
            cpu_usage_percent=cpu_usage
        )
    
    def generate_report(self, results: List[BenchmarkResult]) -> str:
        """Generate a comprehensive benchmark report"""
        report = "# Database Performance Benchmark Report\n\n"
        
        # Group results by operation
        operations = {}
        for result in results:
            if result.operation not in operations:
                operations[result.operation] = []
            operations[result.operation].append(result)
        
        for operation, op_results in operations.items():
            report += f"## {operation.title()} Operations\n\n"
            
            # Group by database
            databases = {}
            for result in op_results:
                if result.database not in databases:
                    databases[result.database] = []
                databases[result.database].append(result)
            
            for db_name, db_results in databases.items():
                report += f"### {db_name}\n\n"
                
                # Calculate statistics
                durations = [r.duration_seconds for r in db_results]
                throughputs = [r.records_per_second for r in db_results]
                memory_usage = [r.memory_usage_mb for r in db_results]
                cpu_usage = [r.cpu_usage_percent for r in db_results]
                
                report += f"- **Average Duration**: {statistics.mean(durations):.4f}s\n"
                report += f"- **Average Throughput**: {statistics.mean(throughputs):.2f} records/s\n"
                report += f"- **Average Memory Usage**: {statistics.mean(memory_usage):.2f} MB\n"
                report += f"- **Average CPU Usage**: {statistics.mean(cpu_usage):.2f}%\n\n"
        
        return report
```

---

# Success Criteria

## Must-Have Features

- [ ] **Multiple Database Support** - Connect to at least 3 different databases
- [ ] **Data Synchronization** - Keep multiple databases in sync
- [ ] **Performance Benchmarking** - Compare database performance
- [ ] **Data Modeling** - Design optimal schemas for each database
- [ ] **Query Optimization** - Optimize queries for each database type
- [ ] **Monitoring** - Track database performance and usage
- [ ] **Documentation** - Comprehensive documentation of findings
- [ ] **Testing** - Unit tests and integration tests

---

# Bonus Challenges

## Advanced Features

- [ ] **Data Pipeline** - Implement ETL processes
- [ ] **Real-time Sync** - Stream data between databases
- [ ] **Data Quality** - Implement data validation and cleaning
- [ ] **Backup Strategy** - Implement backup and recovery
- [ ] **Security** - Implement proper authentication and authorization
- [ ] **Scalability** - Test with large datasets
- [ ] **Analytics** - Extract insights from your data
- [ ] **Visualization** - Create dashboards for monitoring

---

# Getting Started

## Setup Instructions

1. **Set up databases** - Install and configure different databases
2. **Implement connectors** - Create database connection classes
3. **Design schemas** - Create optimal schemas for each database
4. **Build sync system** - Implement data synchronization
5. **Create benchmarks** - Build performance testing framework
6. **Run experiments** - Test different scenarios and configurations
7. **Analyze results** - Compare performance and identify best practices
8. **Document findings** - Create comprehensive documentation

---

# Dependencies

## requirements.txt

```txt
asyncpg>=0.28.0
motor>=3.3.0
elasticsearch>=8.8.0
redis>=4.6.0
clickhouse-connect>=0.6.0
neo4j>=5.12.0
kafka-python>=2.0.2
pandas>=2.0.0
matplotlib>=3.7.0
seaborn>=0.12.0
psutil>=5.9.0
pytest>=7.0.0
```

---

# Resources

## Helpful Links

- **PostgreSQL** - https://www.postgresql.org/
- **MongoDB** - https://www.mongodb.com/
- **Elasticsearch** - https://www.elastic.co/elasticsearch/
- **Redis** - https://redis.io/
- **ClickHouse** - https://clickhouse.com/
- **Neo4j** - https://neo4j.com/
- **Apache Kafka** - https://kafka.apache.org/

---

# Let's Explore Databases!

## Ready to Start?

**This assignment will teach you:**
- Different database types and their use cases
- Data modeling and schema design
- Performance optimization and benchmarking
- Data synchronization and ETL processes
- Database monitoring and maintenance
- Best practices for database selection

**Start with one database and build up to a comprehensive multi-database system!**

---

# Next Steps

## After Completing This Assignment

1. **Deploy your system** - Set up production databases
2. **Monitor performance** - Track database performance in production
3. **Share your findings** - Document your database comparison results
4. **Contribute to open source** - Share your database connectors
5. **Move to the next track** - Try machine learning pipelines or data visualization next!

**Happy database exploring! 🚀**
