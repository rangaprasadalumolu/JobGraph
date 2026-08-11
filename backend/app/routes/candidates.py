from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.database import get_driver


router = APIRouter(
    prefix="/candidates",
    tags=["Candidates"]
)


# =====================================================
# REQUEST MODEL
# =====================================================

class CandidateCreate(BaseModel):
    name: str
    skills: list[str]


# =====================================================
# GET ALL CANDIDATES
# =====================================================

@router.get("")
def get_candidates():

    query = """
    MATCH (c:Candidate)

    RETURN
        c.name AS name

    ORDER BY c.name
    """

    try:

        driver = get_driver()

        with driver.session() as session:

            result = session.run(query)

            candidates = [
                {
                    "name": record["name"]
                }
                for record in result
            ]

            return {
                "candidates": candidates
            }

    except Exception as error:

        print(
            "Candidate fetch error:",
            error
        )

        raise HTTPException(
            status_code=503,
            detail="Unable to retrieve candidates"
        )


# =====================================================
# GET CANDIDATE SKILLS
# =====================================================

@router.get("/{candidate_name}/skills")
def get_candidate_skills(
    candidate_name: str
):

    candidate_name = candidate_name.strip()

    query = """
    MATCH (c:Candidate {name: $candidate_name})
          -[:HAS_SKILL]->(s:Skill)

    RETURN
        s.name AS skill

    ORDER BY s.name
    """

    try:

        driver = get_driver()

        with driver.session() as session:

            result = session.run(
                query,
                candidate_name=candidate_name
            )

            skills = [
                record["skill"]
                for record in result
            ]

            if not skills:

                # Check whether candidate exists
                check_query = """
                MATCH (c:Candidate {name: $candidate_name})
                RETURN c.name AS name
                """

                check_result = session.run(
                    check_query,
                    candidate_name=candidate_name
                )

                candidate_record = (
                    check_result.single()
                )

                if not candidate_record:

                    raise HTTPException(
                        status_code=404,
                        detail="Candidate not found"
                    )

            return {
                "candidate": candidate_name,
                "skills": skills
            }

    except HTTPException:

        raise

    except Exception as error:

        print(
            "Candidate skills error:",
            error
        )

        raise HTTPException(
            status_code=503,
            detail="Unable to retrieve candidate skills"
        )


# =====================================================
# CREATE / UPDATE CANDIDATE
# =====================================================

@router.post("")
def create_candidate(
    candidate: CandidateCreate
):

    # -------------------------------------------------
    # Clean candidate name
    # -------------------------------------------------

    name = candidate.name.strip()


    # -------------------------------------------------
    # Clean skills
    # -------------------------------------------------

    skills = [
        skill.strip()
        for skill in candidate.skills
        if skill.strip()
    ]


    # -------------------------------------------------
    # Validate name
    # -------------------------------------------------

    if not name:

        raise HTTPException(
            status_code=400,
            detail="Candidate name is required"
        )


    # -------------------------------------------------
    # Validate skills
    # -------------------------------------------------

    if not skills:

        raise HTTPException(
            status_code=400,
            detail="At least one skill is required"
        )


    # -------------------------------------------------
    # Remove duplicate skills
    # -------------------------------------------------

    skills = list(
        dict.fromkeys(skills)
    )


    # -------------------------------------------------
    # Cypher query
    # -------------------------------------------------

    query = """
    MERGE (c:Candidate {name: $name})

    WITH c

    UNWIND $skills AS skill_name

    MERGE (s:Skill {name: skill_name})

    MERGE (c)-[:HAS_SKILL]->(s)

    RETURN
        c.name AS candidate,
        collect(DISTINCT s.name) AS skills
    """


    try:

        driver = get_driver()

        with driver.session() as session:

            result = session.run(
                query,
                name=name,
                skills=skills
            )

            record = result.single()


            if not record:

                raise HTTPException(
                    status_code=500,
                    detail="Candidate could not be created"
                )


            return {
                "message":
                    "Candidate created successfully",

                "candidate":
                    record["candidate"],

                "skills":
                    record["skills"]
            }


    except HTTPException:

        raise

    except Exception as error:

        print(
            "Candidate creation error:",
            error
        )

        raise HTTPException(
            status_code=503,
            detail="Unable to create candidate"
        )