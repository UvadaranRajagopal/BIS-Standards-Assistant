import { useEffect, useState } from "react";

import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
  Handle,
  Position,
  type Node,
  type Edge,
} from "@xyflow/react";

import "@xyflow/react/dist/style.css";

interface GraphNodeData {
  label: string;
  title: string;
  category: string;
}

interface GraphResponse {
  nodes: {
    id: string;
    label: string;
    title: string;
    category: string;
  }[];

  edges: {
    source: string;
    target: string;
    relationship: string;
  }[];
}

function StandardNode({
  data,
}: {
  data: GraphNodeData;
}) {
  return (
    <div className="bis-graph-node">

      <Handle
        type="target"
        position={Position.Top}
      />

      <div className="bis-node-number">
        {data.label}
      </div>

      <div className="bis-node-title">
        {data.title}
      </div>

      <div className="bis-node-category">
        {data.category}
      </div>

      <Handle
        type="source"
        position={Position.Bottom}
      />

    </div>
  );
}

const nodeTypes = {
  standard: StandardNode,
};

export default function StandardsGraph() {

  const [nodes, setNodes] = useState<Node[]>([]);
  const [edges, setEdges] = useState<Edge[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {

    const loadGraph = async () => {

      try {

        // Get the current analysis result
        const stored =
          sessionStorage.getItem("analysisResult");

        if (!stored) {
          throw new Error(
            "No analysis result found."
          );
        }

        const analysis = JSON.parse(stored);

        // Get only the standards recommended
        // by the current RAG analysis
        const selectedStandards =
          analysis.standards.map(
            (standard: any) =>
              standard.metadata.is_number
          );

        if (selectedStandards.length === 0) {
          throw new Error(
            "No recommended standards found."
          );
        }

        // Build query parameters
        const params = new URLSearchParams();

        selectedStandards.forEach(
          (standard: string) => {
            params.append("standards", standard);
          }
        );

        const response = await fetch(
          `http://127.0.0.1:8000/graph/standards?${params.toString()}`
        );

        if (!response.ok) {
          throw new Error(
            "Failed to load standards graph"
          );
        }

        const data: GraphResponse =
          await response.json();

        // Arrange nodes in a clean grid
        const graphNodes: Node[] =
          data.nodes.map((node, index) => {

            const columns = 3;

            const column = index % columns;
            const row = Math.floor(index / columns);

            return {
              id: node.id,

              type: "standard",

              position: {
                x: column * 420,
                y: row * 190,
              },

              data: {
                label: node.label,
                title: node.title,
                category: node.category,
              },

              draggable: true,
            };
          });

        // Remove duplicate reverse relationships
        const uniqueRelationships =
          new Set<string>();

        const graphEdges: Edge[] =
          data.edges
            .filter((edge) => {

              const key =
                [edge.source, edge.target]
                  .sort()
                  .join("::");

              if (
                uniqueRelationships.has(key)
              ) {
                return false;
              }

              uniqueRelationships.add(key);

              return true;
            })
            .map((edge, index) => ({

              id: `relationship-${index}`,

              source: edge.source,

              target: edge.target,

              label: edge.relationship,

              type: "smoothstep",

              animated: false,

            }));

        setNodes(graphNodes);
        setEdges(graphEdges);

      } catch (err) {

        console.error(err);

        setError(
          "Unable to load the standards relationship graph."
        );

      } finally {

        setLoading(false);

      }
    };

    loadGraph();

  }, []);

  if (loading) {

    return (
      <div className="graph-loading">
        Loading standards relationship graph...
      </div>
    );

  }

  if (error) {

    return (
      <div className="graph-error">
        {error}
      </div>
    );

  }

  return (

    <div className="standards-graph-page">

      <div className="graph-header">

        <div>

          <div className="graph-eyebrow">
            BIS KNOWLEDGE GRAPH
          </div>

          <h1>
            Standards Relationship Graph
          </h1>

          <p>
            Relationships between standards relevant
            to the current procurement requirement.
          </p>

        </div>

        <div className="graph-count">

          <strong>
            {nodes.length}
          </strong>

          <span>
            Related Standards
          </span>

        </div>

      </div>

      <div className="standards-graph-container">

        <ReactFlow
          nodes={nodes}
          edges={edges}
          nodeTypes={nodeTypes}
          fitView
          fitViewOptions={{
            padding: 0.15,
            minZoom: 0.35,
            maxZoom: 1,
          }}
          nodesDraggable={true}
          nodesConnectable={false}
          elementsSelectable={true}
        >

          <Background />

          <Controls />

          <MiniMap />

        </ReactFlow>

      </div>

    </div>

  );
}