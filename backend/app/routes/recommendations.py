from fastapi import APIRouter, HTTPException

from app.database import get_driver


router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"]
)


@router.get("/{candidate_name}")
def get_recommendations(candidate_name: str):

    query = """
    MATCH (c:Candidate {name: $candidate_name})
          -[:HAS_SKILL]->(s:Skill)
          <-[:REQUIRES]-(j:Job)

    WITH c, j, COUNT(DISTINCT s) AS matched_skills

    MATCH (j)-[:REQUIRES]->(required_skill:Skill)

    WITH
        c,
        j,
        matched_skills,
        COUNT(DISTINCT required_skill) AS total_required_skills

    OPTIONAL MATCH (j)-[:POSTED_BY]->(company:Company)

    OPTIONAL MATCH (j)-[:LOCATED_IN]->(location:Location)

    RETURN DISTINCT
        j.id AS job_id,
        j.title AS job_title,
        j.experience AS experience,
        j.salary AS salary,
        company.name AS company,
        location.name AS location,
        matched_skills,
        total_required_skills

    ORDER BY matched_skills DESC
    """

    try:

        driver = get_driver()

        with driver.session() as session:

            result = session.run(
                query,
                candidate_name=candidate_name
            )

            recommendations = []

            for record in result:

                total = record["total_required_skills"]
                matched = record["matched_skills"]

                if total:
                    match_percentage = round(
                        (matched / total) * 100
                    )
                else:
                    match_percentage = 0

                recommendations.append({

                    "job_id": record["job_id"],

                    "job_title": record["job_title"],

                    "experience": record["experience"],

                    "salary": record["salary"],

                    "company": record["company"],

                    "location": record["location"],

                    "matched_skills": matched,

                    "total_required_skills": total,

                    "match_percentage": match_percentage
                })

            if not recommendations:

                raise HTTPException(
                    status_code=404,
                    detail="No recommendations found for this candidate"
                )

            return {
                "candidate": candidate_name,
                "recommendations": recommendations
            }

    except HTTPException:

        raise

    except Exception:

        raise HTTPException(
            status_code=503,
            detail="Unable to connect to CognoDB"
        )
@router.get("/{candidate_name}/{job_id}/skill-gap")
def get_skill_gap(
    candidate_name: str,
    job_id: str
):

    query = """
    MATCH (j:Job {id: $job_id})
          -[:REQUIRES]->(required:Skill)

    OPTIONAL MATCH (c:Candidate {name: $candidate_name})
          -[:HAS_SKILL]->(candidate_skill:Skill)

    WITH
        required,
        collect(candidate_skill.name) AS candidate_skills

    WHERE NOT required.name IN candidate_skills

    RETURN required.name AS missing_skill

    ORDER BY missing_skill
    """

    try:

        driver = get_driver()

        with driver.session() as session:

            result = session.run(
                query,
                candidate_name=candidate_name,
                job_id=job_id
            )

            missing_skills = []

            for record in result:

                missing_skills.append(
                    record["missing_skill"]
                )

            return {
                "candidate": candidate_name,
                "job_id": job_id,
                "missing_skills": missing_skills
            }

    except Exception:

        raise HTTPException(
            status_code=503,
            detail="Unable to connect to CognoDB"
        )