export interface KnowledgeParticle {
  id: number;
  x: number;
  y: number;
  z: number;
  vx: number;
  vy: number;
  vz: number;
  size: number;
  color: string;
  alpha: number;
  phase: number;
}

export function generateKnowledgeParticles(count = 48): KnowledgeParticle[] {
  const particles: KnowledgeParticle[] = [];
  const colors = ["#67E8F9", "#5B8CFF", "#8B5CF6", "#F5B942"];
  for (let i = 0; i < count; i++) {
    particles.push({
      id: i,
      x: -300 + (i % 6) * 100 + ((i * 19) % 30),
      y: -90 + Math.floor(i / 6) * 25 + ((i * 7) % 20),
      z: -60 + ((i * 31) % 120),
      vx: 0.4 + ((i * 3) % 5) * 0.15,
      vy: ((i % 5) - 2) * 0.12,
      vz: ((i % 3) - 1) * 0.08,
      size: 1.5 + (i % 3) * 0.8,
      color: colors[i % colors.length],
      alpha: 0.35 + (i % 4) * 0.15,
      phase: (i / count) * Math.PI * 2,
    });
  }
  return particles;
}

export function updateKnowledgeParticles(
  particles: KnowledgeParticle[],
  timeSeconds: number,
  sequencePhase: number
): KnowledgeParticle[] {
  // sequencePhase in 0..1 (0-3s fragment, 3-6s pull in, 6-9s struct, 9-12s unified, 12-15s reset)
  return particles.map((p) => {
    let targetX = p.x;
    let targetY = p.y;
    let targetZ = p.z;
    let currentAlpha = p.alpha;

    if (sequencePhase < 0.2) {
      // Phase 1: gentle drift on left
      targetX = -240 + Math.sin(timeSeconds * 0.8 + p.phase) * 60;
      targetY = p.y + Math.cos(timeSeconds * 0.6 + p.phase) * 12;
    } else if (sequencePhase < 0.4) {
      // Phase 2: flow toward center OKF core (x = 0)
      const t = (sequencePhase - 0.2) / 0.2;
      targetX = -240 * (1 - t) + Math.sin(timeSeconds * 2 + p.phase) * 15;
      targetY = p.y * (1 - t * 0.7);
    } else if (sequencePhase < 0.6) {
      // Phase 3: swirl inside OKF core
      const angle = timeSeconds * 3 + p.phase;
      targetX = Math.cos(angle) * 35;
      targetY = Math.sin(angle) * 30;
      targetZ = Math.sin(angle * 1.5) * 30;
      currentAlpha = 0.85;
    } else if (sequencePhase < 0.8) {
      // Phase 4: stream to right unified zone (x = 80..280)
      const t = (sequencePhase - 0.6) / 0.2;
      targetX = 40 + t * 200 + ((p.id * 13) % 40);
      targetY = -80 + (p.id % 8) * 22;
      currentAlpha = 0.65;
    } else {
      // Phase 5: smooth return reset
      const t = (sequencePhase - 0.8) / 0.2;
      targetX = 240 * (1 - t) + -240 * t;
      targetY = p.y;
      currentAlpha = 0.4;
    }

    return {
      ...p,
      x: targetX,
      y: targetY,
      z: targetZ,
      alpha: currentAlpha,
    };
  });
}

