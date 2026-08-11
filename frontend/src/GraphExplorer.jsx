import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
} from "@xyflow/react";

import "@xyflow/react/dist/style.css";


// --------------------------------------------------
// Graph Explorer
// --------------------------------------------------

function GraphExplorer({
  graphData
}) {

  // ------------------------------------------------
  // Safety check
  // ------------------------------------------------

  if (!graphData) {

    return null;

  }


  // ------------------------------------------------
  // Extract graph data
  // ------------------------------------------------

  const candidate =
    graphData.candidate;

  const candidateSkills =
    graphData.candidate_skills || [];

  const job =
    graphData.job;

  const matchedSkills =
    graphData.matched_skills || [];

  const company =
    graphData.company;

  const location =
    graphData.location;

  const technologies =
    graphData.technologies || [];


  // ------------------------------------------------
  // Create nodes
  // ------------------------------------------------

  const nodes = [];


  // Candidate node
  nodes.push({

    id: "candidate",

    position: {
      x: 50,
      y: 260
    },

    data: {
      label: `Candidate\n${candidate}`
    },

    style: {
      background: "#172033",
      color: "white",
      border: "1px solid #172033",
      borderRadius: "12px",
      padding: "14px",
      width: 170,
      fontWeight: 600,
      whiteSpace: "pre-line",
      textAlign: "center"
    }

  });


  // Job node
  nodes.push({

    id: "job",

    position: {
      x: 430,
      y: 260
    },

    data: {
      label: `Job\n${job.title}`
    },

    style: {
      background: "#eef1f6",
      color: "#172033",
      border: "1px solid #cfd5df",
      borderRadius: "12px",
      padding: "14px",
      width: 190,
      fontWeight: 600,
      whiteSpace: "pre-line",
      textAlign: "center"
    }

  });


  // Company node
  if (company) {

    nodes.push({

      id: "company",

      position: {
        x: 780,
        y: 130
      },

      data: {
        label: `Company\n${company}`
      },

      style: {
        background: "#f5f1ea",
        color: "#493b29",
        border: "1px solid #d8cbb8",
        borderRadius: "12px",
        padding: "14px",
        width: 180,
        fontWeight: 600,
        whiteSpace: "pre-line",
        textAlign: "center"
      }

    });

  }


  // Location node
  if (location) {

    nodes.push({

      id: "location",

      position: {
        x: 780,
        y: 360
      },

      data: {
        label: `Location\n${location}`
      },

      style: {
        background: "#eef5f2",
        color: "#245443",
        border: "1px solid #c5ddd3",
        borderRadius: "12px",
        padding: "14px",
        width: 180,
        fontWeight: 600,
        whiteSpace: "pre-line",
        textAlign: "center"
      }

    });

  }


  // ------------------------------------------------
  // Skill nodes
  // ------------------------------------------------

  const uniqueSkills =
    [...new Set(matchedSkills)];


  uniqueSkills.forEach(
    (skill, index) => {

      const yPosition =
        60 + index * 95;


      nodes.push({

        id: `skill-${index}`,

        position: {
          x: 240,
          y: yPosition
        },

        data: {
          label: `Skill\n${skill}`
        },

        style: {
          background: "#eef6f1",
          color: "#167647",
          border: "1px solid #c5dfd0",
          borderRadius: "10px",
          padding: "10px",
          width: 135,
          fontWeight: 600,
          whiteSpace: "pre-line",
          textAlign: "center",
          fontSize: "12px"
        }

      });

    }
  );


  // ------------------------------------------------
  // Technology nodes
  // ------------------------------------------------

  technologies.forEach(
    (technology, index) => {

      nodes.push({

        id: `technology-${index}`,

        position: {
          x: 1030,
          y: 100 + index * 90
        },

        data: {
          label:
            `Technology\n${technology}`
        },

        style: {
          background: "#f1eff8",
          color: "#51427a",
          border: "1px solid #d6cfea",
          borderRadius: "10px",
          padding: "10px",
          width: 150,
          fontWeight: 600,
          whiteSpace: "pre-line",
          textAlign: "center",
          fontSize: "12px"
        }

      });

    }
  );


  // ------------------------------------------------
  // Create edges
  // ------------------------------------------------

  const edges = [];


  // Candidate -> Skills
  uniqueSkills.forEach(
    (skill, index) => {

      edges.push({

        id:
          `candidate-skill-${index}`,

        source: "candidate",

        target:
          `skill-${index}`,

        label: "HAS_SKILL",

        animated: false,

        style: {
          strokeWidth: 2
        },

        labelStyle: {
          fontSize: 10,
          fill: "#667085"
        }

      });

    }
  );


  // Skills -> Job
  uniqueSkills.forEach(
    (skill, index) => {

      edges.push({

        id:
          `skill-job-${index}`,

        source:
          `skill-${index}`,

        target: "job",

        label: "REQUIRES",

        animated: false,

        style: {
          strokeWidth: 2
        },

        labelStyle: {
          fontSize: 10,
          fill: "#667085"
        }

      });

    }
  );


  // Job -> Company
  if (company) {

    edges.push({

      id: "job-company",

      source: "job",

      target: "company",

      label: "POSTED_BY",

      style: {
        strokeWidth: 2
      },

      labelStyle: {
        fontSize: 10,
        fill: "#667085"
      }

    });

  }


  // Job -> Location
  if (location) {

    edges.push({

      id: "job-location",

      source: "job",

      target: "location",

      label: "LOCATED_IN",

      style: {
        strokeWidth: 2
      },

      labelStyle: {
        fontSize: 10,
        fill: "#667085"
      }

    });

  }


  // Job -> Technologies
  technologies.forEach(
    (technology, index) => {

      edges.push({

        id:
          `job-technology-${index}`,

        source: "job",

        target:
          `technology-${index}`,

        label: "USES",

        style: {
          strokeWidth: 2
        },

        labelStyle: {
          fontSize: 10,
          fill: "#667085"
        }

      });

    }
  );


  // ------------------------------------------------
  // Render
  // ------------------------------------------------

  return (

    <div className="graph-explorer">

      <div className="graph-title">

        <div>

          <span className="eyebrow">
            GRAPH EXPLORER
          </span>

          <h3>
            How this recommendation is connected
          </h3>

          <p>

            Explore the relationships between
            the candidate, skills, job, company
            and location.

          </p>

        </div>

      </div>


      <div className="graph-container">

        <ReactFlow
          nodes={nodes}
          edges={edges}
          fitView
          fitViewOptions={{
            padding: 0.2
          }}
          nodesDraggable={true}
          nodesConnectable={false}
          elementsSelectable={true}
          zoomOnScroll={true}
          panOnScroll={true}
        >

          <Background />

          <Controls />

          <MiniMap />

        </ReactFlow>

      </div>

    </div>

  );

}


export default GraphExplorer;