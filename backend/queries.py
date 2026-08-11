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


# ---------------------------------------------------------
# QUERY 1
# Get all jobs
# ---------------------------------------------------------

def get_all_jobs():

    query = """
    MATCH (j:Job)
    RETURN
        j.id AS id,
        j.title AS title,
        j.experience AS experience,
        j.salary AS salary
    ORDER BY j.title
    """

    with driver.session() as session:

        result = session.run(query)

        jobs = []

        for record in result:

            jobs.append({
                "id": record["id"],
                "title": record["title"],
                "experience": record["experience"],
                "salary": record["salary"]
            })

        return jobs


# ---------------------------------------------------------
# QUERY 2
# Get all skills of a candidate
# ---------------------------------------------------------

def get_candidate_skills(candidate_name):

    query = """
    MATCH (c:Candidate {name: $candidate_name})
          -[:HAS_SKILL]->(s:Skill)

    RETURN s.name AS skill
    ORDER BY s.name
    """

    with driver.session() as session:

        result = session.run(
            query,
            candidate_name=candidate_name
        )

        skills = []

        for record in result:

            skills.append(record["skill"])

        return skills


# ---------------------------------------------------------
# QUERY 3
# Multi-hop job recommendation
#
# Candidate
#     ↓
# Skill
#     ↓
# Job
# ---------------------------------------------------------

def get_recommended_jobs(candidate_name):

    query = """
    MATCH (c:Candidate {name: $candidate_name})
          -[:HAS_SKILL]->(s:Skill)
          <-[:REQUIRES]-(j:Job)

    RETURN DISTINCT
        j.id AS id,
        j.title AS title,
        j.experience AS experience,
        j.salary AS salary

    ORDER BY j.title
    """

    with driver.session() as session:

        result = session.run(
            query,
            candidate_name=candidate_name
        )

        jobs = []

        for record in result:

            jobs.append({
                "id": record["id"],
                "title": record["title"],
                "experience": record["experience"],
                "salary": record["salary"]
            })

        return jobs


# ---------------------------------------------------------
# QUERY 4
# Candidate → Skill → Job → Company → Location
#
# This is a 4-hop graph traversal.
# ---------------------------------------------------------

def get_job_details_for_candidate(candidate_name):

    query = """
    MATCH (c:Candidate {name: $candidate_name})
          -[:HAS_SKILL]->(s:Skill)
          <-[:REQUIRES]-(j:Job)
          -[:POSTED_BY]->(company:Company)
          ,
          (j)-[:LOCATED_IN]->(location:Location)

    RETURN DISTINCT
        j.id AS job_id,
        j.title AS job_title,
        j.salary AS salary,
        company.name AS company,
        location.name AS location

    ORDER BY j.title
    """

    with driver.session() as session:

        result = session.run(
            query,
            candidate_name=candidate_name
        )

        jobs = []

        for record in result:

            jobs.append({
                "job_id": record["job_id"],
                "job_title": record["job_title"],
                "salary": record["salary"],
                "company": record["company"],
                "location": record["location"]
            })

        return jobs


# ---------------------------------------------------------
# QUERY 5
# Find missing skills for a candidate and a job
# ---------------------------------------------------------

def get_skill_gap(candidate_name, job_id):

    query = """
    MATCH (j:Job {id: $job_id})
          -[:REQUIRES]->(required:Skill)

    OPTIONAL MATCH (c:Candidate {name: $candidate_name})
          -[:HAS_SKILL]->(candidate_skill:Skill)

    WITH required, collect(candidate_skill.name) AS candidate_skills

    WHERE NOT required.name IN candidate_skills

    RETURN required.name AS missing_skill
    ORDER BY missing_skill
    """

    with driver.session() as session:

        result = session.run(
            query,
            candidate_name=candidate_name,
            job_id=job_id
        )

        missing_skills = []

        for record in result:

            missing_skills.append(record["missing_skill"])

        return missing_skills


# ---------------------------------------------------------
# Run tests
# ---------------------------------------------------------

if __name__ == "__main__":

    try:

        driver.verify_connectivity()

        print()
        print("====================================")
        print("CONNECTED TO COGNODB")
        print("====================================")


        # Query 1
        print()
        print("1. ALL JOBS")
        print("------------------------------------")

        jobs = get_all_jobs()

        for job in jobs:
            print(
                job["id"],
                "|",
                job["title"],
                "|",
                job["salary"]
            )


        # Query 2
        print()
        print("2. NAVEEN'S SKILLS")
        print("------------------------------------")

        skills = get_candidate_skills("Naveen")

        print(skills)


        # Query 3
        print()
        print("3. RECOMMENDED JOBS FOR NAVEEN")
        print("------------------------------------")

        recommended_jobs = get_recommended_jobs("Naveen")

        for job in recommended_jobs:
            print(
                job["title"],
                "|",
                job["salary"]
            )


        # Query 4
        print()
        print("4. JOB DETAILS FOR NAVEEN")
        print("------------------------------------")

        details = get_job_details_for_candidate("Naveen")

        for job in details:

            print(
                job["job_title"],
                "|",
                job["company"],
                "|",
                job["location"]
            )


        # Query 5
        print()
        print("5. SKILL GAP")
        print("------------------------------------")

        missing = get_skill_gap(
            "Naveen",
            "JOB005"
        )

        print("Missing skills:", missing)


    except Exception as error:

        print()
        print("ERROR:")
        print(error)

    finally:

        driver.close()