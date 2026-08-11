import { useEffect, useState } from "react";

import {
  MapPin,
  Briefcase,
  Building2,
  Search,
  CheckCircle2,
  AlertCircle,
  Loader2,
  Code2,
  UserPlus,
  X,
} from "lucide-react";

import "./App.css";

import GraphExplorer from "./GraphExplorer";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [candidates, setCandidates] = useState([]);
  const [selectedCandidate, setSelectedCandidate] = useState("");

  const [recommendations, setRecommendations] = useState([]);

  const [loadingCandidates, setLoadingCandidates] = useState(true);
  const [loadingRecommendations, setLoadingRecommendations] = useState(false);
  const [loadingDetails, setLoadingDetails] = useState(false);
  const [loadingGraph, setLoadingGraph] = useState(false);

  const [addingCandidate, setAddingCandidate] = useState(false);
  const [showAddCandidate, setShowAddCandidate] = useState(false);

  const [newCandidateName, setNewCandidateName] = useState("");
  const [newCandidateSkills, setNewCandidateSkills] = useState("");

  const [showAddJob, setShowAddJob] = useState(false);
  const [addingJob, setAddingJob] = useState(false);

  const [newJobId, setNewJobId] = useState("");
  const [newJobTitle, setNewJobTitle] = useState("");
  const [newJobExperience, setNewJobExperience] = useState("");
  const [newJobSalary, setNewJobSalary] = useState("");
  const [newJobCompany, setNewJobCompany] = useState("");
  const [newJobLocation, setNewJobLocation] = useState("");
  const [newJobSkills, setNewJobSkills] = useState("");
  const [newJobTechnologies, setNewJobTechnologies] = useState("");

  const [error, setError] = useState("");
  const [searched, setSearched] = useState(false);

  const [selectedJob, setSelectedJob] = useState(null);
  const [jobDetails, setJobDetails] = useState(null);
  const [skillGap, setSkillGap] = useState([]);
  const [graphData, setGraphData] = useState(null);

  useEffect(() => {
    loadCandidates();
  }, []);

  async function loadCandidates() {
    try {
      setLoadingCandidates(true);
      setError("");

      const response = await fetch(`${API_URL}/candidates`);

      if (!response.ok) {
        throw new Error("Unable to load candidates");
      }

      const data = await response.json();

      setCandidates(data.candidates || []);

      if (
        data.candidates &&
        data.candidates.length > 0 &&
        !selectedCandidate
      ) {
        setSelectedCandidate(data.candidates[0].name);
      }
    } catch (error) {
      console.error("Candidate loading failed:", error);
      setError("Unable to connect to JobGraph backend.");
    } finally {
      setLoadingCandidates(false);
    }
  }

  function clearResults() {
    setRecommendations([]);
    setSearched(false);
    setSelectedJob(null);
    setJobDetails(null);
    setSkillGap([]);
    setGraphData(null);
  }

  async function findRecommendations() {
    if (!selectedCandidate) {
      setError("Please select a candidate.");
      return;
    }

    try {
      setLoadingRecommendations(true);
      setError("");
      setSearched(true);

      setSelectedJob(null);
      setJobDetails(null);
      setSkillGap([]);
      setGraphData(null);

      const url =
        `${API_URL}/recommendations/` +
        `${encodeURIComponent(selectedCandidate)}`;

      const response = await fetch(url);

      if (!response.ok) {
        let errorMessage = "No recommendations found.";

        try {
          const errorData = await response.json();
          errorMessage = errorData.detail || errorMessage;
        } catch {
          // Ignore JSON parsing errors.
        }

        throw new Error(errorMessage);
      }

      const data = await response.json();

      setRecommendations(data.recommendations || []);
    } catch (error) {
      console.error("Recommendation request failed:", error);
      setRecommendations([]);
      setError(error.message || "Unable to find recommendations.");
    } finally {
      setLoadingRecommendations(false);
    }
  }

  async function addCandidate() {
    const name = newCandidateName.trim();

    const skills = newCandidateSkills
      .split(",")
      .map((skill) => skill.trim())
      .filter(Boolean);

    if (!name) {
      setError("Please enter candidate name.");
      return;
    }

    if (skills.length === 0) {
      setError("Please enter at least one skill.");
      return;
    }

    try {
      setAddingCandidate(true);
      setError("");

      const response = await fetch(`${API_URL}/candidates`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name,
          skills,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Unable to add candidate."
        );
      }

      const candidatesResponse = await fetch(`${API_URL}/candidates`);

      if (!candidatesResponse.ok) {
        throw new Error(
          "Candidate was created, but the candidate list could not be refreshed."
        );
      }

      const candidatesData = await candidatesResponse.json();

      setCandidates(candidatesData.candidates || []);
      setSelectedCandidate(name);

      clearResults();

      setNewCandidateName("");
      setNewCandidateSkills("");
      setShowAddCandidate(false);
      setError("");

      console.log("Candidate added:", data);
    } catch (error) {
      console.error("Add candidate failed:", error);
      setError(error.message || "Unable to add candidate.");
    } finally {
      setAddingCandidate(false);
    }
  }

  async function addJob() {
    const id = newJobId.trim();
    const title = newJobTitle.trim();
    const experience = newJobExperience.trim();
    const salary = newJobSalary.trim();
    const company = newJobCompany.trim();
    const location = newJobLocation.trim();

    const required_skills = newJobSkills
      .split(",")
      .map((skill) => skill.trim())
      .filter(Boolean);

    const technologies = newJobTechnologies
      .split(",")
      .map((technology) => technology.trim())
      .filter(Boolean);

    if (!id) {
      setError("Please enter Job ID.");
      return;
    }

    if (!title) {
      setError("Please enter Job Title.");
      return;
    }

    if (!experience) {
      setError("Please enter experience.");
      return;
    }

    if (!salary) {
      setError("Please enter salary.");
      return;
    }

    if (!company) {
      setError("Please enter company.");
      return;
    }

    if (!location) {
      setError("Please enter location.");
      return;
    }

    if (required_skills.length === 0) {
      setError("Please enter at least one required skill.");
      return;
    }

    if (technologies.length === 0) {
      setError("Please enter at least one technology.");
      return;
    }

    try {
      setAddingJob(true);
      setError("");

      const response = await fetch(`${API_URL}/jobs`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          id,
          title,
          experience,
          salary,
          company,
          location,
          required_skills,
          technologies,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Unable to add job."
        );
      }

      setShowAddJob(false);

      setNewJobId("");
      setNewJobTitle("");
      setNewJobExperience("");
      setNewJobSalary("");
      setNewJobCompany("");
      setNewJobLocation("");
      setNewJobSkills("");
      setNewJobTechnologies("");

      clearResults();
      setError("");

      alert(`Job ${id} created successfully!`);

      console.log("Job created:", data);
    } catch (error) {
      console.error("Add job failed:", error);
      setError(error.message || "Unable to add job.");
    } finally {
      setAddingJob(false);
    }
  }

  async function loadGraphData(jobId) {
    try {
      setLoadingGraph(true);
      setGraphData(null);

      const url =
        `${API_URL}/graph/` +
        `${encodeURIComponent(selectedCandidate)}/` +
        `${encodeURIComponent(jobId)}`;

      const response = await fetch(url);

      if (!response.ok) {
        let errorMessage =
          `Unable to load graph data (${response.status})`;

        try {
          const errorData = await response.json();
          errorMessage = errorData.detail || errorMessage;
        } catch {
          // Ignore parsing errors.
        }

        throw new Error(errorMessage);
      }

      const data = await response.json();

      setGraphData(data);
    } catch (error) {
      console.error("Graph loading failed:", error);
      setError(
        error.message || "Unable to load graph relationships."
      );
    } finally {
      setLoadingGraph(false);
    }
  }

  async function viewJobDetails(job) {
    if (!job || !job.job_id) {
      setError("Unable to identify the selected job.");
      return;
    }

    const jobId = String(job.job_id).trim();

    try {
      setLoadingDetails(true);
      setError("");
      setGraphData(null);

      const detailsUrl =
        `${API_URL}/jobs/` +
        `${encodeURIComponent(jobId)}`;

      const detailsResponse = await fetch(detailsUrl);

      if (!detailsResponse.ok) {
        let errorMessage =
          `Unable to load job details (${detailsResponse.status})`;

        try {
          const errorData = await detailsResponse.json();
          errorMessage = errorData.detail || errorMessage;
        } catch {
          // Ignore parsing errors.
        }

        throw new Error(errorMessage);
      }

      const details = await detailsResponse.json();

      const skillGapUrl =
        `${API_URL}/recommendations/` +
        `${encodeURIComponent(selectedCandidate)}/` +
        `${encodeURIComponent(jobId)}/skill-gap`;

      const skillGapResponse = await fetch(skillGapUrl);

      if (!skillGapResponse.ok) {
        let errorMessage =
          `Unable to calculate skill gap (${skillGapResponse.status})`;

        try {
          const errorData = await skillGapResponse.json();
          errorMessage = errorData.detail || errorMessage;
        } catch {
          // Ignore parsing errors.
        }

        throw new Error(errorMessage);
      }

      const gap = await skillGapResponse.json();

      setSelectedJob(job);
      setJobDetails(details);
      setSkillGap(gap.missing_skills || []);

      await loadGraphData(jobId);
    } catch (error) {
      console.error("View job details failed:", error);
      setError(error.message || "Unable to load job details.");
    } finally {
      setLoadingDetails(false);
    }
  }

  function closeJobDetails() {
    setSelectedJob(null);
    setJobDetails(null);
    setSkillGap([]);
    setGraphData(null);
    setError("");
  }

  function closeCandidateModal() {
    if (addingCandidate) return;

    setShowAddCandidate(false);
    setNewCandidateName("");
    setNewCandidateSkills("");
    setError("");
  }

  function closeJobModal() {
    if (addingJob) return;

    setShowAddJob(false);
    setNewJobId("");
    setNewJobTitle("");
    setNewJobExperience("");
    setNewJobSalary("");
    setNewJobCompany("");
    setNewJobLocation("");
    setNewJobSkills("");
    setNewJobTechnologies("");
    setError("");
  }

  return (
    <div className="app">
      <header className="header">
        <div className="brand">
          <div className="brand-icon">
            <Code2 size={22} />
          </div>

          <div>
            <h1>JobGraph</h1>
            <p>Intelligent Job Recommendations</p>
          </div>
        </div>

        <div className="connection">
          <span className="connection-dot"></span>
          CognoDB Connected
        </div>
      </header>

      <main>
        <section className="hero">
          <div className="hero-content">
            <span className="eyebrow">
              GRAPH-POWERED JOB SEARCH
            </span>

            <h2>
              Find opportunities
              <br />
              that match your skills.
            </h2>

            <p>
              JobGraph analyzes relationships between your skills,
              technologies, jobs and companies to find relevant
              opportunities.
            </p>
          </div>

          <div className="search-card">
            <label>Select candidate</label>

            {loadingCandidates ? (
              <div className="loading-box">
                <Loader2 size={18} className="spin" />
                Loading candidates...
              </div>
            ) : (
              <select
                value={selectedCandidate}
                onChange={(event) => {
                  setSelectedCandidate(event.target.value);
                  clearResults();
                  setError("");
                }}
              >
                {candidates.map((candidate) => (
                  <option
                    key={candidate.name}
                    value={candidate.name}
                  >
                    {candidate.name}
                  </option>
                ))}
              </select>
            )}

            <button
              type="button"
              onClick={findRecommendations}
              disabled={
                loadingCandidates ||
                loadingRecommendations ||
                !selectedCandidate
              }
            >
              {loadingRecommendations ? (
                <>
                  <Loader2 size={18} className="spin" />
                  Finding matches...
                </>
              ) : (
                <>
                  <Search size={18} />
                  Find Matching Jobs
                </>
              )}
            </button>

            {!showAddCandidate && (
              <button
                type="button"
                className="add-candidate-toggle"
                onClick={() => {
                  setShowAddCandidate(true);
                  setError("");
                }}
              >
                <UserPlus size={16} />
                Add New Candidate
              </button>
            )}

            {showAddCandidate && (
              <div className="add-candidate-form">
                <div className="add-form-header">
                  <div>
                    <strong>Add New Candidate</strong>
                    <p>
                      Create a candidate profile with their skills.
                    </p>
                  </div>

                  <button
                    type="button"
                    className="add-form-close"
                    onClick={closeCandidateModal}
                    aria-label="Close add candidate form"
                  >
                    <X size={16} />
                  </button>
                </div>

                <label>Candidate Name</label>

                <input
                  type="text"
                  value={newCandidateName}
                  onChange={(event) =>
                    setNewCandidateName(event.target.value)
                  }
                  placeholder="e.g. Rahul"
                  disabled={addingCandidate}
                />

                <label>Skills</label>

                <input
                  type="text"
                  value={newCandidateSkills}
                  onChange={(event) =>
                    setNewCandidateSkills(event.target.value)
                  }
                  placeholder="Python, SQL, FastAPI, Git"
                  disabled={addingCandidate}
                />

                <small>
                  Enter skills separated by commas.
                </small>

                <button
                  type="button"
                  onClick={addCandidate}
                  disabled={addingCandidate}
                >
                  {addingCandidate ? (
                    <>
                      <Loader2 size={17} className="spin" />
                      Adding Candidate...
                    </>
                  ) : (
                    <>
                      <UserPlus size={17} />
                      Add Candidate
                    </>
                  )}
                </button>
              </div>
            )}

            {!showAddJob && (
              <button
                type="button"
                className="add-job-toggle"
                onClick={() => {
                  setShowAddJob(true);
                  setError("");
                }}
              >
                <Briefcase size={16} />
                Add New Job
              </button>
            )}

            {showAddJob && (
              <div className="add-job-form">
                <div className="add-form-header">
                  <div>
                    <strong>Add New Job</strong>
                    <p>
                      Create a new job opportunity with required skills.
                    </p>
                  </div>

                  <button
                    type="button"
                    className="add-form-close"
                    onClick={closeJobModal}
                    aria-label="Close add job form"
                  >
                    <X size={16} />
                  </button>
                </div>

                <label>Job ID</label>

                <input
                  type="text"
                  value={newJobId}
                  onChange={(event) =>
                    setNewJobId(event.target.value)
                  }
                  placeholder="e.g. JOB006"
                  disabled={addingJob}
                />

                <label>Job Title</label>

                <input
                  type="text"
                  value={newJobTitle}
                  onChange={(event) =>
                    setNewJobTitle(event.target.value)
                  }
                  placeholder="e.g. AI Backend Developer"
                  disabled={addingJob}
                />

                <label>Experience</label>

                <input
                  type="text"
                  value={newJobExperience}
                  onChange={(event) =>
                    setNewJobExperience(event.target.value)
                  }
                  placeholder="e.g. 1-3 years"
                  disabled={addingJob}
                />

                <label>Salary</label>

                <input
                  type="text"
                  value={newJobSalary}
                  onChange={(event) =>
                    setNewJobSalary(event.target.value)
                  }
                  placeholder="e.g. 6-10 LPA"
                  disabled={addingJob}
                />

                <label>Company</label>

                <input
                  type="text"
                  value={newJobCompany}
                  onChange={(event) =>
                    setNewJobCompany(event.target.value)
                  }
                  placeholder="e.g. InnovateAI Technologies"
                  disabled={addingJob}
                />

                <label>Location</label>

                <input
                  type="text"
                  value={newJobLocation}
                  onChange={(event) =>
                    setNewJobLocation(event.target.value)
                  }
                  placeholder="e.g. Hyderabad"
                  disabled={addingJob}
                />

                <label>Required Skills</label>

                <input
                  type="text"
                  value={newJobSkills}
                  onChange={(event) =>
                    setNewJobSkills(event.target.value)
                  }
                  placeholder="Python, SQL, FastAPI"
                  disabled={addingJob}
                />

                <small>
                  Separate skills with commas.
                </small>

                <label>Technologies</label>

                <input
                  type="text"
                  value={newJobTechnologies}
                  onChange={(event) =>
                    setNewJobTechnologies(event.target.value)
                  }
                  placeholder="FastAPI, PostgreSQL, Docker"
                  disabled={addingJob}
                />

                <small>
                  Separate technologies with commas.
                </small>

                <button
                  type="button"
                  onClick={addJob}
                  disabled={addingJob}
                >
                  {addingJob ? (
                    <>
                      <Loader2 size={17} className="spin" />
                      Adding Job...
                    </>
                  ) : (
                    <>
                      <Briefcase size={17} />
                      Add Job
                    </>
                  )}
                </button>
              </div>
            )}
          </div>
        </section>

        {error && (
          <div className="error-box">
            <AlertCircle size={20} />

            <div>
              <strong>Something went wrong</strong>
              <p>{error}</p>
            </div>
          </div>
        )}

        {loadingDetails && (
          <div className="loading-box">
            <Loader2 size={20} className="spin" />
            Loading job details...
          </div>
        )}

        {searched &&
          !loadingRecommendations &&
          !error && (
            <section className="results">
              <div className="results-header">
                <div>
                  <span className="eyebrow">
                    RECOMMENDATIONS
                  </span>

                  <h3>
                    Jobs matched for {selectedCandidate}
                  </h3>
                </div>

                <span className="result-count">
                  {recommendations.length} jobs found
                </span>
              </div>

              {recommendations.length === 0 ? (
                <div className="empty-state">
                  <Briefcase size={32} />

                  <h3>No matching jobs</h3>

                  <p>
                    Try selecting another candidate or adding more
                    skills.
                  </p>
                </div>
              ) : (
                <div className="job-grid">
                  {recommendations.map((job) => (
                    <article
                      className="job-card"
                      key={job.job_id}
                    >
                      <div className="job-card-top">
                        <div className="job-icon">
                          <Briefcase size={20} />
                        </div>

                        <div className="match">
                          <CheckCircle2 size={15} />
                          {job.match_percentage}% Match
                        </div>
                      </div>

                      <h4>{job.job_title}</h4>

                      <div className="company">
                        <Building2 size={16} />
                        {job.company}
                      </div>

                      <div className="location">
                        <MapPin size={16} />
                        {job.location}
                      </div>

                      <div className="job-meta">
                        <span>
                          Experience: {job.experience}
                        </span>

                        <span>{job.salary}</span>
                      </div>

                      <div className="match-bar">
                        <div
                          className="match-progress"
                          style={{
                            width: `${job.match_percentage}%`,
                          }}
                        />
                      </div>

                      <div className="match-info">
                        <span>
                          {job.matched_skills} /{" "}
                          {job.total_required_skills} skills matched
                        </span>
                      </div>

                      <button
                        type="button"
                        className="details-button"
                        onClick={() => viewJobDetails(job)}
                        disabled={loadingDetails}
                      >
                        {loadingDetails &&
                        selectedJob?.job_id === job.job_id ? (
                          <>
                            <Loader2
                              size={16}
                              className="spin"
                            />
                            Loading...
                          </>
                        ) : (
                          <>View Job Details →</>
                        )}
                      </button>
                    </article>
                  ))}
                </div>
              )}
            </section>
          )}

        {selectedJob && jobDetails && (
          <>
            <section className="details-section">
              <div className="details-header">
                <div>
                  <span className="eyebrow">
                    JOB DETAILS
                  </span>

                  <h3>{jobDetails.title}</h3>
                </div>

                <button
                  type="button"
                  className="close-button"
                  onClick={closeJobDetails}
                >
                  Close
                </button>
              </div>

              <div className="details-grid">
                <div className="details-card">
                  <h4>Position Information</h4>

                  <div className="detail-row">
                    <span>Company</span>
                    <strong>{jobDetails.company}</strong>
                  </div>

                  <div className="detail-row">
                    <span>Location</span>
                    <strong>{jobDetails.location}</strong>
                  </div>

                  <div className="detail-row">
                    <span>Experience</span>
                    <strong>{jobDetails.experience}</strong>
                  </div>

                  <div className="detail-row">
                    <span>Salary</span>
                    <strong>{jobDetails.salary}</strong>
                  </div>
                </div>

                <div className="details-card">
                  <h4>Required Skills</h4>

                  <div className="skill-list">
                    {(jobDetails.required_skills || []).map(
                      (skill) => (
                        <span
                          className="skill-tag"
                          key={skill}
                        >
                          {skill}
                        </span>
                      )
                    )}
                  </div>

                  <h4 className="technology-heading">
                    Technologies
                  </h4>

                  <div className="skill-list">
                    {(jobDetails.technologies || []).map(
                      (technology) => (
                        <span
                          className="technology-tag"
                          key={technology}
                        >
                          {technology}
                        </span>
                      )
                    )}
                  </div>
                </div>

                <div className="details-card skill-gap-card">
                  <h4>Your Skill Gap</h4>

                  {skillGap.length === 0 ? (
                    <div className="no-gap">
                      <CheckCircle2 size={22} />

                      <div>
                        <strong>Excellent match!</strong>

                        <p>
                          You have all the skills required for this job.
                        </p>
                      </div>
                    </div>
                  ) : (
                    <>
                      <p className="gap-description">
                        These skills are required by this job but are
                        not currently connected to your candidate
                        profile.
                      </p>

                      <div className="missing-list">
                        {skillGap.map((skill) => (
                          <span
                            className="missing-tag"
                            key={skill}
                          >
                            {skill}
                          </span>
                        ))}
                      </div>
                    </>
                  )}
                </div>
              </div>
            </section>

            {loadingGraph && (
              <div className="loading-box">
                <Loader2 size={20} className="spin" />
                Loading graph relationships...
              </div>
            )}

            {graphData && !loadingGraph && (
              <GraphExplorer graphData={graphData} />
            )}
          </>
        )}

        {!searched &&
          !loadingCandidates &&
          !error && (
            <section className="initial-state">
              <div className="initial-icon">
                <Search size={28} />
              </div>

              <h3>
                Ready to find your next opportunity?
              </h3>

              <p>
                Select a candidate above to discover jobs using
                graph-based matching.
              </p>
            </section>
          )}
      </main>

      <footer>
        <span>JobGraph</span>
        <span>Powered by CognoDB + FastAPI</span>
      </footer>
    </div>
  );
}

export default App;
