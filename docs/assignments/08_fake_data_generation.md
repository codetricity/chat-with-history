---
theme: gaia
_class: lead
paginate: true
backgroundColor: #fff
backgroundImage: url('https://marp.app/assets/hero-background.svg')
---

![bg left:40% 80%](https://oppkey.com/static/logo.jpg)

# **Fake Data Generation Assignment**
## Realistic Test Data for Development

**Create comprehensive fake datasets for testing and development**

---

# Assignment Overview

## What You'll Build

A sophisticated fake data generation system that creates:
- **Customer records** - Realistic customer profiles and purchase history
- **Lead data** - Whitepaper downloads, webinar registrations, and form submissions
- **Social media profiles** - Fake Reddit users, YouTube creators, and Twitter accounts
- **Content data** - Posts, comments, videos, and articles
- **Interaction data** - User engagement, clicks, and behavior patterns
- **Temporal data** - Realistic timestamps and event sequences

---

# Problem Statement

## Why Fake Data?

Real-world data processing systems need realistic test data for:
- **Development testing** - Test algorithms without real customer data
- **Performance testing** - Scale testing with large datasets
- **Privacy protection** - Avoid using sensitive real data
- **Reproducible results** - Consistent data for testing
- **Edge case testing** - Generate unusual scenarios
- **API rate limiting** - Avoid hitting API limits during development

---

# Your Solution

## Comprehensive Data Generation

Create a fake data generation system that addresses these needs:

1. **Realistic Data** - Statistically accurate fake data
2. **Configurable Scale** - Generate datasets of any size
3. **Data Relationships** - Maintain referential integrity
4. **Temporal Consistency** - Realistic time-based data
5. **Edge Cases** - Include unusual and boundary conditions
6. **Export Formats** - Multiple output formats (JSON, CSV, SQL)

---

# Technical Requirements

## Tech Stack

- **Python 3.8+** with type hints
- **Faker** - Primary fake data generation
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical operations
- **SQLAlchemy** - Database operations
- **Pydantic** - Data validation
- **Click** - Command-line interface
- **Tqdm** - Progress bars

---

# Project Structure

## Recommended Architecture

```
fake_data_generator/
├── src/
│   ├── generators/
│   │   ├── base.py
│   │   ├── customers.py
│   │   ├── leads.py
│   │   ├── social_media.py
│   │   └── content.py
│   ├── models/
│   │   ├── customer.py
│   │   ├── lead.py
│   │   ├── social_profile.py
│   │   └── content.py
│   ├── utils/
│   │   ├── data_validation.py
│   │   ├── export.py
│   │   └── statistics.py
│   └── cli.py
├── config/
│   ├── data_config.yaml
│   └── database_config.yaml
├── tests/
│   ├── test_generators.py
│   └── test_models.py
└── requirements.txt
```

---

# Core Components

## 1. Base Generator Class

```python
# src/generators/base.py
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from faker import Faker
import random
from datetime import datetime, timedelta

class BaseGenerator(ABC):
    def __init__(self, locale: str = 'en_US', seed: Optional[int] = None):
        self.fake = Faker(locale)
        if seed:
            Faker.seed(seed)
            random.seed(seed)
    
    @abstractmethod
    def generate(self, count: int) -> List[Dict[str, Any]]:
        """Generate a list of fake records"""
        pass
    
    def generate_batch(self, count: int, batch_size: int = 1000) -> List[Dict[str, Any]]:
        """Generate records in batches for memory efficiency"""
        all_records = []
        for i in range(0, count, batch_size):
            batch_count = min(batch_size, count - i)
            batch = self.generate(batch_count)
            all_records.extend(batch)
            yield batch
    
    def add_relationships(self, records: List[Dict[str, Any]], 
                         related_data: Dict[str, List[Any]]) -> List[Dict[str, Any]]:
        """Add foreign key relationships to records"""
        for record in records:
            for field, related_list in related_data.items():
                if related_list:
                    record[field] = random.choice(related_list)
        return records
```

---

# Core Components

## 2. Customer Generator

```python
# src/generators/customers.py
from typing import Dict, Any, List
from .base import BaseGenerator
from ..models.customer import Customer

class CustomerGenerator(BaseGenerator):
    def __init__(self, locale: str = 'en_US', seed: Optional[int] = None):
        super().__init__(locale, seed)
        self.industries = [
            'Technology', 'Healthcare', 'Finance', 'Education', 
            'Manufacturing', 'Retail', 'Consulting', 'Real Estate'
        ]
        self.company_sizes = ['Startup', 'Small', 'Medium', 'Large', 'Enterprise']
    
    def generate(self, count: int) -> List[Dict[str, Any]]:
        customers = []
        for _ in range(count):
            customer = {
                'id': self.fake.uuid4(),
                'first_name': self.fake.first_name(),
                'last_name': self.fake.last_name(),
                'email': self.fake.email(),
                'phone': self.fake.phone_number(),
                'company': self.fake.company(),
                'job_title': self.fake.job(),
                'industry': random.choice(self.industries),
                'company_size': random.choice(self.company_sizes),
                'location': {
                    'city': self.fake.city(),
                    'state': self.fake.state(),
                    'country': self.fake.country(),
                    'postal_code': self.fake.postcode()
                },
                'created_at': self.fake.date_time_between(start_date='-2y', end_date='now'),
                'last_activity': self.fake.date_time_between(start_date='-6m', end_date='now'),
                'status': random.choices(
                    ['active', 'inactive', 'prospect', 'churned'],
                    weights=[0.6, 0.2, 0.15, 0.05]
                )[0],
                'lifetime_value': round(random.uniform(0, 50000), 2),
                'lead_source': random.choice([
                    'organic_search', 'paid_search', 'social_media', 
                    'referral', 'email_campaign', 'webinar', 'whitepaper'
                ])
            }
            customers.append(customer)
        return customers
    
    def generate_purchase_history(self, customer_ids: List[str], 
                                count_per_customer: int = 5) -> List[Dict[str, Any]]:
        purchases = []
        products = [
            'Software License', 'Consulting Hours', 'Training Course',
            'Support Package', 'Custom Development', 'Integration Service'
        ]
        
        for customer_id in customer_ids:
            for _ in range(random.randint(1, count_per_customer)):
                purchase = {
                    'id': self.fake.uuid4(),
                    'customer_id': customer_id,
                    'product': random.choice(products),
                    'amount': round(random.uniform(100, 10000), 2),
                    'purchase_date': self.fake.date_time_between(start_date='-1y', end_date='now'),
                    'status': random.choice(['completed', 'pending', 'cancelled']),
                    'payment_method': random.choice(['credit_card', 'bank_transfer', 'paypal'])
                }
                purchases.append(purchase)
        return purchases
```

---

# Core Components

## 3. Lead Generator

```python
# src/generators/leads.py
from typing import Dict, Any, List
from .base import BaseGenerator

class LeadGenerator(BaseGenerator):
    def __init__(self, locale: str = 'en_US', seed: Optional[int] = None):
        super().__init__(locale, seed)
        self.lead_sources = [
            'whitepaper_download', 'webinar_registration', 'demo_request',
            'newsletter_signup', 'contact_form', 'social_media',
            'referral', 'trade_show', 'cold_outreach'
        ]
        self.content_types = [
            'whitepaper', 'ebook', 'case_study', 'webinar', 'demo',
            'trial', 'consultation', 'newsletter'
        ]
    
    def generate(self, count: int) -> List[Dict[str, Any]]:
        leads = []
        for _ in range(count):
            lead = {
                'id': self.fake.uuid4(),
                'email': self.fake.email(),
                'first_name': self.fake.first_name(),
                'last_name': self.fake.last_name(),
                'company': self.fake.company(),
                'job_title': self.fake.job(),
                'phone': self.fake.phone_number(),
                'lead_source': random.choice(self.lead_sources),
                'content_type': random.choice(self.content_types),
                'content_title': self.fake.sentence(nb_words=6),
                'created_at': self.fake.date_time_between(start_date='-1y', end_date='now'),
                'status': random.choices(
                    ['new', 'contacted', 'qualified', 'unqualified', 'converted'],
                    weights=[0.3, 0.25, 0.2, 0.15, 0.1]
                )[0],
                'score': random.randint(0, 100),
                'notes': self.fake.text(max_nb_chars=200) if random.random() < 0.3 else None,
                'utm_source': random.choice(['google', 'facebook', 'linkedin', 'twitter', 'direct']),
                'utm_medium': random.choice(['cpc', 'organic', 'social', 'email', 'referral']),
                'utm_campaign': self.fake.word() + '_campaign'
            }
            leads.append(lead)
        return leads
    
    def generate_webinar_registrations(self, webinar_ids: List[str], 
                                     count_per_webinar: int = 50) -> List[Dict[str, Any]]:
        registrations = []
        for webinar_id in webinar_ids:
            for _ in range(random.randint(10, count_per_webinar)):
                registration = {
                    'id': self.fake.uuid4(),
                    'webinar_id': webinar_id,
                    'email': self.fake.email(),
                    'first_name': self.fake.first_name(),
                    'last_name': self.fake.last_name(),
                    'company': self.fake.company(),
                    'job_title': self.fake.job(),
                    'registered_at': self.fake.date_time_between(start_date='-3m', end_date='now'),
                    'attended': random.choice([True, False]),
                    'attendance_duration': random.randint(0, 60) if random.choice([True, False]) else 0,
                    'feedback_score': random.randint(1, 5) if random.choice([True, False]) else None
                }
                registrations.append(registration)
        return registrations
```

---

# Core Components

## 4. Social Media Generator

```python
# src/generators/social_media.py
from typing import Dict, Any, List
from .base import BaseGenerator

class SocialMediaGenerator(BaseGenerator):
    def __init__(self, locale: str = 'en_US', seed: Optional[int] = None):
        super().__init__(locale, seed)
        self.platforms = ['reddit', 'youtube', 'twitter', 'linkedin', 'github']
        self.subreddits = [
            'MachineLearning', 'datascience', 'Python', 'programming',
            'webdev', 'startups', 'entrepreneur', 'technology'
        ]
        self.video_categories = [
            'Tutorial', 'Review', 'News', 'Entertainment', 'Educational',
            'Product Demo', 'Interview', 'Live Stream'
        ]
    
    def generate_reddit_users(self, count: int) -> List[Dict[str, Any]]:
        users = []
        for _ in range(count):
            user = {
                'id': self.fake.uuid4(),
                'username': self.fake.user_name(),
                'display_name': self.fake.name(),
                'email': self.fake.email() if random.random() < 0.3 else None,
                'created_at': self.fake.date_time_between(start_date='-5y', end_date='now'),
                'karma': random.randint(0, 50000),
                'verified': random.choice([True, False]),
                'premium': random.choice([True, False]),
                'bio': self.fake.text(max_nb_chars=160) if random.random() < 0.7 else None,
                'location': self.fake.city() if random.random() < 0.4 else None,
                'interests': random.sample(self.subreddits, random.randint(1, 5))
            }
            users.append(user)
        return users
    
    def generate_reddit_posts(self, user_ids: List[str], count: int) -> List[Dict[str, Any]]:
        posts = []
        for _ in range(count):
            post = {
                'id': self.fake.uuid4(),
                'user_id': random.choice(user_ids),
                'subreddit': random.choice(self.subreddits),
                'title': self.fake.sentence(nb_words=8),
                'content': self.fake.text(max_nb_chars=2000),
                'created_at': self.fake.date_time_between(start_date='-1y', end_date='now'),
                'score': random.randint(-100, 1000),
                'upvote_ratio': random.uniform(0.1, 1.0),
                'num_comments': random.randint(0, 500),
                'awards': random.randint(0, 10),
                'flair': random.choice(['Discussion', 'Question', 'News', 'Meta']) if random.random() < 0.3 else None,
                'nsfw': random.choice([True, False]),
                'stickied': random.choice([True, False])
            }
            posts.append(post)
        return posts
    
    def generate_youtube_channels(self, count: int) -> List[Dict[str, Any]]:
        channels = []
        for _ in range(count):
            channel = {
                'id': self.fake.uuid4(),
                'channel_name': self.fake.company() + ' Tech',
                'description': self.fake.text(max_nb_chars=500),
                'created_at': self.fake.date_time_between(start_date='-3y', end_date='now'),
                'subscriber_count': random.randint(100, 1000000),
                'video_count': random.randint(10, 500),
                'total_views': random.randint(10000, 10000000),
                'category': random.choice(self.video_categories),
                'country': self.fake.country(),
                'verified': random.choice([True, False]),
                'monetization': random.choice([True, False])
            }
            channels.append(channel)
        return channels
    
    def generate_youtube_videos(self, channel_ids: List[str], count: int) -> List[Dict[str, Any]]:
        videos = []
        for _ in range(count):
            video = {
                'id': self.fake.uuid4(),
                'channel_id': random.choice(channel_ids),
                'title': self.fake.sentence(nb_words=6),
                'description': self.fake.text(max_nb_chars=1000),
                'published_at': self.fake.date_time_between(start_date='-1y', end_date='now'),
                'duration': random.randint(60, 3600),  # seconds
                'views': random.randint(100, 1000000),
                'likes': random.randint(0, 50000),
                'dislikes': random.randint(0, 1000),
                'comments': random.randint(0, 10000),
                'category': random.choice(self.video_categories),
                'tags': [self.fake.word() for _ in range(random.randint(3, 10))],
                'thumbnail_url': self.fake.image_url(),
                'privacy': random.choice(['public', 'unlisted', 'private'])
            }
            videos.append(video)
        return videos
```

---

# Data Models

## Pydantic Models

```python
# src/models/customer.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum

class CompanySize(str, Enum):
    STARTUP = "startup"
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    ENTERPRISE = "enterprise"

class CustomerStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PROSPECT = "prospect"
    CHURNED = "churned"

class Location(BaseModel):
    city: str
    state: str
    country: str
    postal_code: str

class Customer(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    company: str
    job_title: str
    industry: str
    company_size: CompanySize
    location: Location
    created_at: datetime
    last_activity: datetime
    status: CustomerStatus
    lifetime_value: float = Field(ge=0)
    lead_source: str

class Purchase(BaseModel):
    id: str
    customer_id: str
    product: str
    amount: float = Field(ge=0)
    purchase_date: datetime
    status: str
    payment_method: str
```

---

# Data Validation

## Quality Assurance

```python
# src/utils/data_validation.py
from typing import List, Dict, Any
import pandas as pd
from datetime import datetime

class DataValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []
    
    def validate_customers(self, customers: List[Dict[str, Any]]) -> bool:
        """Validate customer data for quality and consistency"""
        df = pd.DataFrame(customers)
        
        # Check for required fields
        required_fields = ['id', 'email', 'first_name', 'last_name', 'company']
        for field in required_fields:
            if field not in df.columns:
                self.errors.append(f"Missing required field: {field}")
        
        # Check for duplicate emails
        duplicate_emails = df[df.duplicated(subset=['email'], keep=False)]
        if not duplicate_emails.empty:
            self.warnings.append(f"Found {len(duplicate_emails)} duplicate emails")
        
        # Check email format
        invalid_emails = df[~df['email'].str.contains('@', na=False)]
        if not invalid_emails.empty:
            self.errors.append(f"Found {len(invalid_emails)} invalid email addresses")
        
        # Check date consistency
        if 'created_at' in df.columns and 'last_activity' in df.columns:
            invalid_dates = df[df['created_at'] > df['last_activity']]
            if not invalid_dates.empty:
                self.errors.append(f"Found {len(invalid_dates)} records with invalid date ranges")
        
        return len(self.errors) == 0
    
    def validate_relationships(self, customers: List[Dict[str, Any]], 
                            purchases: List[Dict[str, Any]]) -> bool:
        """Validate referential integrity between related data"""
        customer_ids = {c['id'] for c in customers}
        purchase_customer_ids = {p['customer_id'] for p in purchases}
        
        orphaned_purchases = purchase_customer_ids - customer_ids
        if orphaned_purchases:
            self.errors.append(f"Found {len(orphaned_purchases)} orphaned purchases")
        
        return len(self.errors) == 0
    
    def get_validation_report(self) -> Dict[str, Any]:
        """Generate a comprehensive validation report"""
        return {
            'valid': len(self.errors) == 0,
            'error_count': len(self.errors),
            'warning_count': len(self.warnings),
            'errors': self.errors,
            'warnings': self.warnings
        }
```

---

# Export Functions

## Multiple Output Formats

```python
# src/utils/export.py
import json
import csv
import sqlite3
from typing import List, Dict, Any
import pandas as pd

class DataExporter:
    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def export_to_json(self, data: List[Dict[str, Any]], filename: str) -> str:
        """Export data to JSON format"""
        filepath = os.path.join(self.output_dir, f"{filename}.json")
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        return filepath
    
    def export_to_csv(self, data: List[Dict[str, Any]], filename: str) -> str:
        """Export data to CSV format"""
        filepath = os.path.join(self.output_dir, f"{filename}.csv")
        df = pd.DataFrame(data)
        df.to_csv(filepath, index=False)
        return filepath
    
    def export_to_sqlite(self, tables: Dict[str, List[Dict[str, Any]]], 
                        filename: str) -> str:
        """Export data to SQLite database"""
        filepath = os.path.join(self.output_dir, f"{filename}.db")
        conn = sqlite3.connect(filepath)
        
        for table_name, records in tables.items():
            df = pd.DataFrame(records)
            df.to_sql(table_name, conn, if_exists='replace', index=False)
        
        conn.close()
        return filepath
    
    def export_to_postgresql(self, tables: Dict[str, List[Dict[str, Any]]], 
                           connection_string: str) -> bool:
        """Export data to PostgreSQL database"""
        try:
            import psycopg2
            from sqlalchemy import create_engine
            
            engine = create_engine(connection_string)
            
            for table_name, records in tables.items():
                df = pd.DataFrame(records)
                df.to_sql(table_name, engine, if_exists='replace', index=False)
            
            return True
        except ImportError:
            print("psycopg2 not installed. Install with: pip install psycopg2-binary")
            return False
```

---

# CLI Interface

## Command Line Tool

```python
# src/cli.py
import click
from typing import Optional
from .generators.customers import CustomerGenerator
from .generators.leads import LeadGenerator
from .generators.social_media import SocialMediaGenerator
from .utils.export import DataExporter
from .utils.data_validation import DataValidator

@click.group()
def cli():
    """Fake Data Generator CLI"""
    pass

@cli.command()
@click.option('--count', default=1000, help='Number of records to generate')
@click.option('--output-format', type=click.Choice(['json', 'csv', 'sqlite']), 
              default='json', help='Output format')
@click.option('--seed', type=int, help='Random seed for reproducibility')
@click.option('--locale', default='en_US', help='Locale for fake data')
def generate_customers(count: int, output_format: str, seed: Optional[int], locale: str):
    """Generate fake customer data"""
    generator = CustomerGenerator(locale=locale, seed=seed)
    exporter = DataExporter()
    validator = DataValidator()
    
    click.echo(f"Generating {count} customer records...")
    customers = generator.generate(count)
    
    # Validate data
    if validator.validate_customers(customers):
        click.echo("✅ Data validation passed")
    else:
        click.echo("❌ Data validation failed")
        for error in validator.errors:
            click.echo(f"  - {error}")
        return
    
    # Export data
    if output_format == 'json':
        filepath = exporter.export_to_json(customers, 'customers')
    elif output_format == 'csv':
        filepath = exporter.export_to_csv(customers, 'customers')
    elif output_format == 'sqlite':
        filepath = exporter.export_to_sqlite({'customers': customers}, 'customers')
    
    click.echo(f"✅ Data exported to {filepath}")

@cli.command()
@click.option('--count', default=500, help='Number of records to generate')
@click.option('--output-format', type=click.Choice(['json', 'csv', 'sqlite']), 
              default='json', help='Output format')
@click.option('--seed', type=int, help='Random seed for reproducibility')
def generate_social_media(count: int, output_format: str, seed: Optional[int]):
    """Generate fake social media data"""
    generator = SocialMediaGenerator(seed=seed)
    exporter = DataExporter()
    
    click.echo(f"Generating {count} social media records...")
    
    # Generate users and posts
    users = generator.generate_reddit_users(count // 2)
    posts = generator.generate_reddit_posts([u['id'] for u in users], count)
    
    # Export data
    if output_format == 'sqlite':
        filepath = exporter.export_to_sqlite({
            'reddit_users': users,
            'reddit_posts': posts
        }, 'social_media')
    else:
        users_file = exporter.export_to_json(users, 'reddit_users')
        posts_file = exporter.export_to_json(posts, 'reddit_posts')
        click.echo(f"✅ Users exported to {users_file}")
        click.echo(f"✅ Posts exported to {posts_file}")
        return
    
    click.echo(f"✅ Data exported to {filepath}")

if __name__ == '__main__':
    cli()
```

---

# Testing

## Comprehensive Test Suite

```python
# tests/test_generators.py
import pytest
from src.generators.customers import CustomerGenerator
from src.generators.leads import LeadGenerator
from src.generators.social_media import SocialMediaGenerator

class TestCustomerGenerator:
    def test_generate_customers(self):
        generator = CustomerGenerator(seed=42)
        customers = generator.generate(10)
        
        assert len(customers) == 10
        assert all('email' in customer for customer in customers)
        assert all('@' in customer['email'] for customer in customers)
        assert all(customer['lifetime_value'] >= 0 for customer in customers)
    
    def test_generate_purchase_history(self):
        generator = CustomerGenerator(seed=42)
        customer_ids = ['customer1', 'customer2']
        purchases = generator.generate_purchase_history(customer_ids, 3)
        
        assert len(purchases) == 6  # 2 customers * 3 purchases each
        assert all(purchase['customer_id'] in customer_ids for purchase in purchases)
        assert all(purchase['amount'] > 0 for purchase in purchases)

class TestLeadGenerator:
    def test_generate_leads(self):
        generator = LeadGenerator(seed=42)
        leads = generator.generate(10)
        
        assert len(leads) == 10
        assert all('email' in lead for lead in leads)
        assert all(lead['score'] >= 0 and lead['score'] <= 100 for lead in leads)
        assert all(lead['status'] in ['new', 'contacted', 'qualified', 'unqualified', 'converted'] 
                  for lead in leads)

class TestSocialMediaGenerator:
    def test_generate_reddit_users(self):
        generator = SocialMediaGenerator(seed=42)
        users = generator.generate_reddit_users(10)
        
        assert len(users) == 10
        assert all('username' in user for user in users)
        assert all(user['karma'] >= 0 for user in users)
        assert all(len(user['interests']) > 0 for user in users)
    
    def test_generate_reddit_posts(self):
        generator = SocialMediaGenerator(seed=42)
        user_ids = ['user1', 'user2']
        posts = generator.generate_reddit_posts(user_ids, 10)
        
        assert len(posts) == 10
        assert all(post['user_id'] in user_ids for post in posts)
        assert all(post['score'] >= -100 for post in posts)
        assert all(post['upvote_ratio'] >= 0 and post['upvote_ratio'] <= 1 for post in posts)
```

---

# Success Criteria

## Must-Have Features

- [ ] **Realistic Data** - Generate statistically accurate fake data
- [ ] **Multiple Data Types** - Customers, leads, social media, content
- [ ] **Data Relationships** - Maintain referential integrity
- [ ] **Configurable Scale** - Generate datasets of any size
- [ ] **Multiple Output Formats** - JSON, CSV, SQLite, PostgreSQL
- [ ] **Data Validation** - Quality assurance and error checking
- [ ] **CLI Interface** - Easy-to-use command line tool
- [ ] **Comprehensive Testing** - Unit tests and integration tests

---

# Bonus Challenges

## Advanced Features

- [ ] **Temporal Consistency** - Generate realistic time-based data
- [ ] **Data Anonymization** - Remove PII while maintaining relationships
- [ ] **Custom Schemas** - Allow users to define custom data structures
- [ ] **Performance Optimization** - Generate large datasets efficiently
- [ ] **Data Visualization** - Generate charts and graphs of the data
- [ ] **API Integration** - Generate data based on real API responses
- [ ] **Machine Learning** - Use ML to generate more realistic data
- [ ] **Data Lineage** - Track data generation and transformations

---

# Getting Started

## Setup Instructions

1. **Create project structure** - Set up the recommended architecture
2. **Install dependencies** - Add Faker, Pandas, and other required packages
3. **Implement base generator** - Create the abstract base class
4. **Build specific generators** - Start with customers, then leads, then social media
5. **Add data validation** - Implement quality assurance checks
6. **Create export functions** - Support multiple output formats
7. **Build CLI interface** - Make it easy to use from command line
8. **Write tests** - Ensure data quality and generator reliability

---

# Dependencies

## requirements.txt

```txt
faker>=19.0.0
pandas>=1.5.0
numpy>=1.24.0
pydantic>=2.0.0
click>=8.0.0
tqdm>=4.65.0
sqlalchemy>=2.0.0
psycopg2-binary>=2.9.0
pytest>=7.0.0
pytest-cov>=4.0.0
```

---

# Resources

## Helpful Links

- **Faker Documentation** - https://faker.readthedocs.io/
- **Pandas** - https://pandas.pydata.org/
- **Pydantic** - https://pydantic-docs.helpmanual.io/
- **Click** - https://click.palletsprojects.com/
- **SQLAlchemy** - https://www.sqlalchemy.org/
- **Data Generation Best Practices** - https://www.oreilly.com/library/view/data-generation/9781492048775/

---

# Let's Generate Data!

## Ready to Start?

**This assignment will teach you:**
- Data generation techniques and best practices
- Statistical modeling for realistic fake data
- Data validation and quality assurance
- Multiple output formats and database integration
- Command-line tool development
- Testing strategies for data generation

**Start with basic customer data and build up to complex social media datasets!**

---

# Next Steps

## After Completing This Assignment

1. **Share your datasets** - Make them available for others to use
2. **Document your approach** - Write about your data generation strategies
3. **Contribute to open source** - Share your generators with the community
4. **Move to the next track** - Try social media API integration or advanced search algorithms next!

**Happy data generating! 🚀**
