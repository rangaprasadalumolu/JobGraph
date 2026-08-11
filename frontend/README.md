# JobGraph

## Graph-Based Job Recommendation System

JobGraph is a full-stack job recommendation application built around a graph database.

The system connects candidates, skills, jobs, companies, locations and technologies using graph relationships and uses those relationships to recommend relevant jobs and identify skill gaps.

---

## Features

- Candidate selection
- Graph-based job recommendations
- Skill matching
- Match percentage calculation
- Job details
- Skill gap analysis
- Company and location information
- Technology relationships
- Interactive graph visualization
- REST API using FastAPI
- React frontend
- CognoDB graph database

---

## Technology Stack

### Backend

- Python
- FastAPI
- Neo4j Python Driver
- Uvicorn
- python-dotenv

### Frontend

- React
- Vite
- JavaScript
- CSS
- Lucide React
- React Flow

### Database

- CognoDB

---

# Graph Data Model

The core graph contains the following node types:

- Candidate
- Skill
- Technology
- Job
- Company
- Location

The main relationships are:

- `HAS_SKILL`
- `REQUIRES`
- `USES`
- `POSTED_BY`
- `LOCATED_IN`
- `RELATED_TO`

Conceptually:

```text
Candidate
    |
    | HAS_SKILL
    v
  Skill
    |
    | REQUIRES
    v
   Job
   / \
  /   \
POSTED  LOCATED_IN
 /          \
v            v
Company    Location

Job
 |
 | USES
 v
Technology