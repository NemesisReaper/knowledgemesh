export interface UnifiedKnowledgeNode {
  id: string;
  x: number;
  y: number;
  z: number;
  label: string;
  category: "concept" | "claim" | "evidence" | "provenance";
  connectedTo: string[];
}

export function generateUnifiedKnowledgeNetwork(): {
  nodes: UnifiedKnowledgeNode[];
  edges: Array<{ source: string; target: string; weight: number }>;
} {
  const nodes: UnifiedKnowledgeNode[] = [];
  const edges: Array<{ source: string; target: string; weight: number }> = [];

  const categories: UnifiedKnowledgeNode["category"][] = [
    "concept",
    "claim",
    "evidence",
    "provenance",
  ];

  // Right zone: x from +120 to +290, y from -100 to +100
  const cols = 4;
  const rows = 4;
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const idx = r * cols + c;
      const id = `uni-${idx}`;
      const x = 125 + c * 48;
      const y = -85 + r * 52;
      const z = -20 + ((idx * 17) % 40);
      const category = categories[idx % categories.length];

      nodes.push({
        id,
        x,
        y,
        z,
        label: `OKF::${category.toUpperCase()}_${idx + 1}`,
        category,
        connectedTo: [],
      });
    }
  }

  // Connect adjacent grid nodes and diagonal links
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const current = `uni-${r * cols + c}`;
      if (c < cols - 1) {
        const right = `uni-${r * cols + (c + 1)}`;
        edges.push({ source: current, target: right, weight: 1 });
      }
      if (r < rows - 1) {
        const down = `uni-${(r + 1) * cols + c}`;
        edges.push({ source: current, target: down, weight: 1 });
      }
      if (c < cols - 1 && r < rows - 1 && (r + c) % 2 === 0) {
        const diag = `uni-${(r + 1) * cols + (c + 1)}`;
        edges.push({ source: current, target: diag, weight: 0.8 });
      }
    }
  }

  return { nodes, edges };
}

