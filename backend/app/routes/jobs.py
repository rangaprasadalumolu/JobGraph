from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.database import get_driver


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)


# =====================================================
# REQUEST MODEL
# =====================================================

class JobCreate(BaseModel):
    id: str
    title: str
    experience: str
    salary: str
    company: str
    location: str
    required_skills: list[str]
    technologies: list[str]


# =====================================================
# GET ALL JOBS
# =====================================================

@router.get("")
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

    try:

        driver = get_driver()

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

            return {
                "count": len(jobs),
                "jobs": jobs
            }

    except Exception as error:

        print(
            "Get jobs error:",
            error
        )

        raise HTTPException(
            status_code=503,
            detail="Unable to connect to CognoDB"
        )


# =====================================================
# GET JOB DETAILS
# =====================================================

@router.get("/{job_id}")
def get_job_details(
    job_id: str
):

    query = """
    MATCH (j:Job {id: $job_id})

    OPTIONAL MATCH
        (j)-[:POSTED_BY]->(company:Company)

    OPTIONAL MATCH
        (j)-[:LOCATED_IN]->(location:Location)

    OPTIONAL MATCH
        (j)-[:REQUIRES]->(skill:Skill)

    OPTIONAL MATCH
        (j)-[:USES]->(technology:Technology)

    RETURN
        j.id AS id,
        j.title AS title,
        j.experience AS experience,
        j.salary AS salary,
        company.name AS company,
        location.name AS location,
        collect(DISTINCT skill.name) AS required_skills,
        collect(DISTINCT technology.name) AS technologies
    """

    try:

        driver = get_driver()

        with driver.session() as session:

            result = session.run(
                query,
                job_id=job_id
            )

            record = result.single()

            if not record:

                raise HTTPException(
                    status_code=404,
                    detail="Job not found"
                )

            return {
                "id": record["id"],
                "title": record["title"],
                "experience": record["experience"],
                "salary": record["salary"],
                "company": record["company"],
                "location": record["location"],
                "required_skills":
                    record["required_skills"],
                "technologies":
                    record["technologies"]
            }

    except HTTPException:

        raise

    except Exception as error:

        print(
            "Get job details error:",
            error
        )

        raise HTTPException(
            status_code=503,
            detail="Unable to connect to CognoDB"
        )


# =====================================================
# CREATE NEW JOB
# =====================================================

@router.post("")
def create_job(
    job: JobCreate
):

    # -------------------------------------------------
    # Clean input values
    # -------------------------------------------------

    job_id = job.id.strip()
    title = job.title.strip()
    experience = job.experience.strip()
    salary = job.salary.strip()
    company = job.company.strip()
    location = job.location.strip()

    required_skills = [
        skill.strip()
        for skill in job.required_skills
        if skill.strip()
    ]

    technologies = [
        technology.strip()
        for technology in job.technologies
        if technology.strip()
    ]


    # -------------------------------------------------
    # Validate required fields
    # -------------------------------------------------

    if not job_id:

        raise HTTPException(
            status_code=400,
            detail="Job ID is required"
        )


    if not title:

        raise HTTPException(
            status_code=400,
            detail="Job title is required"
        )


    if not experience:

        raise HTTPException(
            status_code=400,
            detail="Experience is required"
        )


    if not salary:

        raise HTTPException(
            status_code=400,
            detail="Salary is required"
        )


    if not company:

        raise HTTPException(
            status_code=400,
            detail="Company is required"
        )


    if not location:

        raise HTTPException(
            status_code=400,
            detail="Location is required"
        )


    if not required_skills:

        raise HTTPException(
            status_code=400,
            detail="At least one required skill is required"
        )


    if not technologies:

        raise HTTPException(
            status_code=400,
            detail="At least one technology is required"
        )


    # -------------------------------------------------
    # Remove duplicate values
    # -------------------------------------------------

    required_skills = list(
        dict.fromkeys(required_skills)
    )

    technologies = list(
        dict.fromkeys(technologies)
    )


    # -------------------------------------------------
    # Create graph structure
    # -------------------------------------------------

    query = """
    MERGE (j:Job {id: $job_id})

    SET
        j.title = $title,
        j.experience = $experience,
        j.salary = $salary

    MERGE (c:Company {name: $company})

    MERGE (l:Location {name: $location})

    MERGE (j)-[:POSTED_BY]->(c)

    MERGE (j)-[:LOCATED_IN]->(l)

    WITH j

    UNWIND $required_skills AS skill_name

    MERGE (s:Skill {name: skill_name})

    MERGE (j)-[:REQUIRES]->(s)

    WITH j

    UNWIND $technologies AS technology_name

    MERGE (t:Technology {name: technology_name})

    MERGE (j)-[:USES]->(t)

    RETURN
        j.id AS id,
        j.title AS title,
        j.experience AS experience,
        j.salary AS salary
    """


    # -------------------------------------------------
    # Execute query
    # -------------------------------------------------

    try:

        driver = get_driver()

        with driver.session() as session:

            result = session.run(
                query,
                job_id=job_id,
                title=title,
                experience=experience,
                salary=salary,
                company=company,
                location=location,
                required_skills=required_skills,
                technologies=technologies
            )

            record = result.single()


            if not record:

                raise HTTPException(
                    status_code=500,
                    detail="Job could not be created"
                )


            return {
                "message":
                    "Job created successfully",

                "job": {
                    "id": record["id"],
                    "title": record["title"],
                    "experience":
                        record["experience"],
                    "salary":
                        record["salary"]
                }
            }


    except HTTPException:

        raise

    except Exception as error:

        print(
            "Create job error:",
            error
        )

        raise HTTPException(
            status_code=503,
            detail="Unable to create job"
        )