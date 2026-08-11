// =====================================================
// JobGraph Graph Schema
// =====================================================


// -----------------------------------------------------
// Candidate
// -----------------------------------------------------

CREATE CONSTRAINT candidate_name_unique IF NOT EXISTS
FOR (c:Candidate)
REQUIRE c.name IS UNIQUE;


// -----------------------------------------------------
// Skill
// -----------------------------------------------------

CREATE CONSTRAINT skill_name_unique IF NOT EXISTS
FOR (s:Skill)
REQUIRE s.name IS UNIQUE;


// -----------------------------------------------------
// Technology
// -----------------------------------------------------

CREATE CONSTRAINT technology_name_unique IF NOT EXISTS
FOR (t:Technology)
REQUIRE t.name IS UNIQUE;


// -----------------------------------------------------
// Company
// -----------------------------------------------------

CREATE CONSTRAINT company_name_unique IF NOT EXISTS
FOR (c:Company)
REQUIRE c.name IS UNIQUE;


// -----------------------------------------------------
// Location
// -----------------------------------------------------

CREATE CONSTRAINT location_name_unique IF NOT EXISTS
FOR (l:Location)
REQUIRE l.name IS UNIQUE;


// -----------------------------------------------------
// Job
// -----------------------------------------------------

CREATE CONSTRAINT job_id_unique IF NOT EXISTS
FOR (j:Job)
REQUIRE j.id IS UNIQUE;