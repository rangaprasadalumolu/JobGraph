import os

from dotenv import load_dotenv
from neo4j import GraphDatabase


# Load environment variables
load_dotenv()

COGNODB_URI = os.getenv("COGNODB_URI")
COGNODB_USERNAME = os.getenv("COGNODB_USERNAME")
COGNODB_PASSWORD = os.getenv("COGNODB_PASSWORD")


# Create database driver
driver = GraphDatabase.driver(
    COGNODB_URI,
    auth=(COGNODB_USERNAME, COGNODB_PASSWORD)
)


def clear_database(session):
    """
    Remove existing nodes and relationships.
    This allows us to run the seed script multiple times.
    """

    session.run("""
        MATCH (n)
        DETACH DELETE n
    """)

    print("Old database data cleared.")


def create_constraints(session):
    """
    Create uniqueness constraints for important nodes.
    """

    queries = [
        """
        CREATE CONSTRAINT candidate_name_unique IF NOT EXISTS
        FOR (c:Candidate)
        REQUIRE c.name IS UNIQUE
        """,

        """
        CREATE CONSTRAINT skill_name_unique IF NOT EXISTS
        FOR (s:Skill)
        REQUIRE s.name IS UNIQUE
        """,

        """
        CREATE CONSTRAINT technology_name_unique IF NOT EXISTS
        FOR (t:Technology)
        REQUIRE t.name IS UNIQUE
        """,

        """
        CREATE CONSTRAINT company_name_unique IF NOT EXISTS
        FOR (c:Company)
        REQUIRE c.name IS UNIQUE
        """,

        """
        CREATE CONSTRAINT location_name_unique IF NOT EXISTS
        FOR (l:Location)
        REQUIRE l.name IS UNIQUE
        """,

        """
        CREATE CONSTRAINT job_id_unique IF NOT EXISTS
        FOR (j:Job)
        REQUIRE j.id IS UNIQUE
        """
    ]

    for query in queries:
        session.run(query)

    print("Constraints created.")


def create_data(session):

    # -------------------------
    # Skills
    # -------------------------

    skills = [
        "Python",
        "Java",
        "SQL",
        "Machine Learning",
        "Deep Learning",
        "FastAPI",
        "Flask",
        "Django",
        "React",
        "JavaScript",
        "Docker",
        "Git",
        "AWS",
        "TensorFlow",
        "PyTorch"
    ]

    for skill in skills:
        session.run(
            """
            MERGE (s:Skill {name: $name})
            """,
            name=skill
        )

    print(f"Created {len(skills)} skills.")

    # -------------------------
    # Technologies
    # -------------------------

    technologies = [
        {
            "name": "FastAPI",
            "category": "Backend"
        },
        {
            "name": "Flask",
            "category": "Backend"
        },
        {
            "name": "Django",
            "category": "Backend"
        },
        {
            "name": "React",
            "category": "Frontend"
        },
        {
            "name": "Docker",
            "category": "DevOps"
        },
        {
            "name": "AWS",
            "category": "Cloud"
        },
        {
            "name": "TensorFlow",
            "category": "AI"
        },
        {
            "name": "PyTorch",
            "category": "AI"
        }
    ]

    for technology in technologies:
        session.run(
            """
            MERGE (t:Technology {
                name: $name
            })
            SET t.category = $category
            """,
            name=technology["name"],
            category=technology["category"]
        )

    print(f"Created {len(technologies)} technologies.")

    # -------------------------
    # Locations
    # -------------------------

    locations = [
        "Hyderabad",
        "Bangalore",
        "Chennai",
        "Pune",
        "Mumbai",
        "Remote"
    ]

    for location in locations:
        session.run(
            """
            MERGE (l:Location {name: $name})
            """,
            name=location
        )

    print(f"Created {len(locations)} locations.")

    # -------------------------
    # Companies
    # -------------------------

    companies = [
        "TechNova Solutions",
        "DataSphere Technologies",
        "AI Vision Labs",
        "CloudBridge Systems",
        "CodeCraft Technologies"
    ]

    for company in companies:
        session.run(
            """
            MERGE (c:Company {name: $name})
            """,
            name=company
        )

    print(f"Created {len(companies)} companies.")

    # -------------------------
    # Candidates
    # -------------------------

    candidates = [
        {
            "name": "Naveen",
            "experience": 0
        },
        {
            "name": "Rahul",
            "experience": 1
        },
        {
            "name": "Priya",
            "experience": 0
        },
        {
            "name": "Arjun",
            "experience": 2
        }
    ]

    for candidate in candidates:
        session.run(
            """
            MERGE (c:Candidate {name: $name})
            SET c.experience = $experience
            """,
            name=candidate["name"],
            experience=candidate["experience"]
        )

    print(f"Created {len(candidates)} candidates.")

    # -------------------------
    # Candidate Skills
    # -------------------------

    candidate_skills = {
        "Naveen": [
            "Python",
            "SQL",
            "FastAPI",
            "Machine Learning",
            "Git"
        ],
        "Rahul": [
            "Java",
            "SQL",
            "Spring Boot",
            "Git"
        ],
        "Priya": [
            "Python",
            "React",
            "JavaScript",
            "SQL"
        ],
        "Arjun": [
            "Python",
            "Docker",
            "AWS",
            "FastAPI"
        ]
    }

    for candidate_name, skills_list in candidate_skills.items():

        for skill in skills_list:

            # Create skill if it does not exist
            session.run(
                """
                MERGE (s:Skill {name: $skill})
                """,
                skill=skill
            )

            # Connect candidate to skill
            session.run(
                """
                MATCH (c:Candidate {name: $candidate})
                MATCH (s:Skill {name: $skill})
                MERGE (c)-[:HAS_SKILL]->(s)
                """,
                candidate=candidate_name,
                skill=skill
            )

    print("Candidate-skill relationships created.")

    # -------------------------
    # Skill relationships
    # -------------------------

    related_skills = [
        ("Python", "FastAPI"),
        ("Python", "Flask"),
        ("Python", "Django"),
        ("Python", "Machine Learning"),
        ("Machine Learning", "Deep Learning"),
        ("Machine Learning", "TensorFlow"),
        ("Machine Learning", "PyTorch"),
        ("JavaScript", "React"),
        ("Python", "SQL"),
        ("Docker", "AWS")
    ]

    for skill_a, skill_b in related_skills:

        session.run(
            """
            MATCH (a:Skill {name: $skill_a})
            MATCH (b:Skill {name: $skill_b})
            MERGE (a)-[:RELATED_TO]->(b)
            """,
            skill_a=skill_a,
            skill_b=skill_b
        )

    print("Skill relationships created.")

    # -------------------------
    # Jobs
    # -------------------------

    jobs = [
        {
            "id": "JOB001",
            "title": "Python Backend Developer",
            "experience": "Fresher",
            "salary": "4-7 LPA",
            "company": "TechNova Solutions",
            "location": "Hyderabad"
        },
        {
            "id": "JOB002",
            "title": "AI/ML Engineer",
            "experience": "0-2 years",
            "salary": "6-10 LPA",
            "company": "AI Vision Labs",
            "location": "Bangalore"
        },
        {
            "id": "JOB003",
            "title": "Data Analyst",
            "experience": "Fresher",
            "salary": "3-6 LPA",
            "company": "DataSphere Technologies",
            "location": "Hyderabad"
        },
        {
            "id": "JOB004",
            "title": "Full Stack Developer",
            "experience": "0-2 years",
            "salary": "5-9 LPA",
            "company": "CodeCraft Technologies",
            "location": "Pune"
        },
        {
            "id": "JOB005",
            "title": "Cloud Backend Engineer",
            "experience": "1-3 years",
            "salary": "7-12 LPA",
            "company": "CloudBridge Systems",
            "location": "Remote"
        }
    ]

    for job in jobs:

        session.run(
            """
            MERGE (j:Job {id: $id})
            SET
                j.title = $title,
                j.experience = $experience,
                j.salary = $salary
            """,
            id=job["id"],
            title=job["title"],
            experience=job["experience"],
            salary=job["salary"]
        )

        session.run(
            """
            MATCH (j:Job {id: $job_id})
            MATCH (c:Company {name: $company})
            MERGE (j)-[:POSTED_BY]->(c)
            """,
            job_id=job["id"],
            company=job["company"]
        )

        session.run(
            """
            MATCH (j:Job {id: $job_id})
            MATCH (l:Location {name: $location})
            MERGE (j)-[:LOCATED_IN]->(l)
            """,
            job_id=job["id"],
            location=job["location"]
        )

    print(f"Created {len(jobs)} jobs.")

    # -------------------------
    # Job required skills
    # -------------------------

    job_skills = {
        "JOB001": [
            "Python",
            "SQL",
            "FastAPI",
            "Git"
        ],
        "JOB002": [
            "Python",
            "Machine Learning",
            "Deep Learning",
            "TensorFlow"
        ],
        "JOB003": [
            "Python",
            "SQL",
            "Machine Learning"
        ],
        "JOB004": [
            "Python",
            "React",
            "JavaScript",
            "SQL"
        ],
        "JOB005": [
            "Python",
            "FastAPI",
            "Docker",
            "AWS"
        ]
    }

    for job_id, required_skills in job_skills.items():

        for skill in required_skills:

            session.run(
                """
                MERGE (s:Skill {name: $skill})
                """,
                skill=skill
            )

            session.run(
                """
                MATCH (j:Job {id: $job_id})
                MATCH (s:Skill {name: $skill})
                MERGE (j)-[:REQUIRES]->(s)
                """,
                job_id=job_id,
                skill=skill
            )

    print("Job-skill relationships created.")

    # -------------------------
    # Job technologies
    # -------------------------

    job_technologies = {
        "JOB001": ["FastAPI"],
        "JOB002": ["TensorFlow", "PyTorch"],
        "JOB003": ["Python"],
        "JOB004": ["React"],
        "JOB005": ["FastAPI", "Docker", "AWS"]
    }

    for job_id, technologies_list in job_technologies.items():

        for technology in technologies_list:

            session.run(
                """
                MATCH (j:Job {id: $job_id})
                MATCH (t:Technology {name: $technology})
                MERGE (j)-[:USES]->(t)
                """,
                job_id=job_id,
                technology=technology
            )

    print("Job-technology relationships created.")


def main():

    print("Connecting to CognoDB...")

    try:

        driver.verify_connectivity()

        print("Connection successful!")

        with driver.session() as session:

            clear_database(session)

            create_constraints(session)

            create_data(session)

        print()
        print("======================================")
        print("DATABASE SEEDING COMPLETED SUCCESSFULLY")
        print("======================================")

    except Exception as error:

        print()
        print("ERROR:")
        print(error)

    finally:

        driver.close()


if __name__ == "__main__":
    main()