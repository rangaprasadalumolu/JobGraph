// =====================================================
// JobGraph Cypher Queries
// =====================================================


// =====================================================
// 1. Get all jobs
// =====================================================

MATCH (j:Job)

RETURN
    j.id AS id,
    j.title AS title,
    j.experience AS experience,
    j.salary AS salary

ORDER BY j.title;


// =====================================================
// 2. Get candidate skills
// =====================================================

MATCH (c:Candidate {name: $candidate_name})
      -[:HAS_SKILL]->(s:Skill)

RETURN
    s.name AS skill

ORDER BY s.name;


// =====================================================
// 3. Job recommendations
//
// Candidate → Skill ← Job
// =====================================================

MATCH (c:Candidate {name: $candidate_name})
      -[:HAS_SKILL]->(s:Skill)
      <-[:REQUIRES]-(j:Job)

RETURN DISTINCT
    j.id AS id,
    j.title AS title,
    j.experience AS experience,
    j.salary AS salary

ORDER BY j.title;


// =====================================================
// 4. Multi-hop job details
//
// Candidate → Skill ← Job → Company
//                              ↓
//                           Location
// =====================================================

MATCH (c:Candidate {name: $candidate_name})
      -[:HAS_SKILL]->(s:Skill)
      <-[:REQUIRES]-(j:Job)
      -[:POSTED_BY]->(company:Company)

MATCH (j)-[:LOCATED_IN]->(location:Location)

RETURN DISTINCT
    j.id AS job_id,
    j.title AS job_title,
    j.salary AS salary,
    company.name AS company,
    location.name AS location

ORDER BY j.title;


// =====================================================
// 5. Skill gap
// =====================================================

MATCH (j:Job {id: $job_id})
      -[:REQUIRES]->(required:Skill)

OPTIONAL MATCH (c:Candidate {name: $candidate_name})
      -[:HAS_SKILL]->(candidate_skill:Skill)

WITH
    required,
    collect(candidate_skill.name) AS candidate_skills

WHERE NOT required.name IN candidate_skills

RETURN
    required.name AS missing_skill

ORDER BY missing_skill;


// =====================================================
// 6. Recommendation score
// =====================================================

MATCH (c:Candidate {name: $candidate_name})
      -[:HAS_SKILL]->(s:Skill)
      <-[:REQUIRES]-(j:Job)

WITH
    c,
    j,
    COUNT(DISTINCT s) AS matched_skills

MATCH (j)-[:REQUIRES]->(required:Skill)

WITH
    c,
    j,
    matched_skills,
    COUNT(DISTINCT required) AS total_required_skills

RETURN
    j.id AS job_id,
    j.title AS job_title,
    matched_skills,
    total_required_skills,
    CASE
        WHEN total_required_skills = 0
        THEN 0
        ELSE
            ROUND(
                100.0 *
                matched_skills /
                total_required_skills
            )
    END AS match_percentage

ORDER BY match_percentage DESC;