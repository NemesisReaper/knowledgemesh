export interface SceneLightingConfig {
  ambientColor: string;
  ambientIntensity: number;
  coreLightColor: string;
  coreLightIntensity: number;
  highlightCyan: string;
  violetAccent: string;
}

export const DEFAULT_SCENE_LIGHTING: SceneLightingConfig = {
  ambientColor: "#0B1220",
  ambientIntensity: 0.6,
  coreLightColor: "#5B8CFF",
  coreLightIntensity: 2.2,
  highlightCyan: "#67E8F9",
  violetAccent: "#8B5CF6",
};

export function getVolumetricLightGradient(
  ctx: CanvasRenderingContext2D | WebGLRenderingContext,
  width: number,
  height: number,
  progress: number
) {
  // Returns normalized lighting pulses for 3D shader / canvas composition
  const pulse = Math.sin(progress * Math.PI * 2);
  return {
    pulseIntensity: 0.8 + 0.3 * pulse,
    coreGlowRadius: 120 + 25 * pulse,
  };
}

