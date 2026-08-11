from fastapi import APIRouter, HTTPException

from app.database import get_driver


router = APIRouter(
    prefix="/graph",
    tags=["Graph"]
)


@router.get("/{candidate_name}/{job_id}")
def get_graph(
    candidate_name: str,
    job_id: str
):

    # Remove accidental spaces from URL parameters
    candidate_name = candidate_name.strip()
    job_id = job_id.strip()

    print("Graph request:")
    print("Candidate:", candidate_name)
    print("Job ID:", job_id)

    query = """
    MATCH (c:Candidate {name: $candidate_name})
          -[:HAS_SKILL]->(s:Skill)
          <-[:REQUIRES]-(j:Job {id: $job_id})

    OPTIONAL MATCH (j)-[:POSTED_BY]->(company:Company)

    OPTIONAL MATCH (j)-[:LOCATED_IN]->(location:Location)

    OPTIONAL MATCH (j)-[:USES]->(technology:Technology)

    RETURN
        c.name AS candidate,
        collect(DISTINCT s.name) AS candidate_skills,
        j.id AS job_id,
        j.title AS job_title,
        collect(DISTINCT s.name) AS matched_skills,
        company.name AS company,
        location.name AS location,
        collect(DISTINCT technology.name) AS technologies
    """

    try:

        driver = get_driver()

        with driver.session() as session:

            result = session.run(
                query,
                candidate_name=candidate_name,
                job_id=job_id
            )

            record = result.single()

            if not record:

                raise HTTPException(
                    status_code=404,
                    detail="Graph relationship not found"
                )

            return {
                "candidate": record["candidate"],

                "candidate_skills":
                    record["candidate_skills"],

                "job": {
                    "id": record["job_id"],
                    "title": record["job_title"]
                },

                "matched_skills":
                    record["matched_skills"],

                "company":
                    record["company"],

                "location":
                    record["location"],

                "technologies":
                    record["technologies"]
            }

    except HTTPException:

        raise

    except Exception as error:

        print("Graph API error:", error)

        raise HTTPException(
            status_code=503,
            detail="Unable to retrieve graph data"
        )