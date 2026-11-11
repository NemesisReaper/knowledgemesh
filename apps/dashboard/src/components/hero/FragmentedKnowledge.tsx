export interface FragmentedItem {
  id: string;
  type: "glass_cube" | "document_slab" | "layered_sheet" | "data_block" | "wireframe" | "metadata_card";
  initialX: number;
  initialY: number;
  initialZ: number;
  rotationX: number;
  rotationY: number;
  rotationZ: number;
  size: { w: number; h: number; d: number };
  opacity: number;
}

export function generateFragmentedKnowledgeObjects(count = 15): FragmentedItem[] {
  const types: FragmentedItem["type"][] = [
    "glass_cube",
    "document_slab",
    "layered_sheet",
    "data_block",
    "wireframe",
    "metadata_card",
  ];

  const items: FragmentedItem[] = [];
  for (let i = 0; i < count; i++) {
    // Left-third zone: -320 to -110 in relative coordinates
    const row = Math.floor(i / 3);
    const col = i % 3;
    const baseOffset = (i * 137.5) % 100;
    items.push({
      id: `frag-${i}`,
      type: types[i % types.length],
      initialX: -280 + col * 75 + ((baseOffset % 30) - 15),
      initialY: -110 + row * 55 + (((baseOffset * 3) % 24) - 12),
      initialZ: -80 + ((baseOffset * 7) % 160),
      rotationX: (i * 0.42) % Math.PI,
      rotationY: (i * 0.65) % Math.PI,
      rotationZ: (i * 0.31) % Math.PI,
      size: {
        w: 22 + (i % 4) * 6,
        h: 28 + ((i * 2) % 5) * 6,
        d: 14 + (i % 3) * 6,
      },
      opacity: 0.55 + (i % 4) * 0.1,
    });
  }
  return items;
}

