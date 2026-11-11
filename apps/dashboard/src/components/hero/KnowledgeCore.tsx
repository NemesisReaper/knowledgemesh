export interface CoreLayer {
  radius: number;
  rotationSpeed: number;
  wireframe: boolean;
  color: string;
  opacity: number;
}

export const CORE_LAYERS: CoreLayer[] = [
  { radius: 68, rotationSpeed: 0.008, wireframe: false, color: "#5B8CFF", opacity: 0.18 },
  { radius: 54, rotationSpeed: -0.012, wireframe: true, color: "#67E8F9", opacity: 0.65 },
  { radius: 38, rotationSpeed: 0.016, wireframe: false, color: "#3B82F6", opacity: 0.35 },
  { radius: 22, rotationSpeed: -0.022, wireframe: true, color: "#8B5CF6", opacity: 0.85 },
];

export interface CoreState {
  pulse: number;
  hoverIntensity: number;
  rotation: number;
}

