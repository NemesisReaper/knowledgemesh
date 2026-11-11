export interface TransformationTimeline {
  currentTime: number;
  totalDuration: number;
  phaseIndex: 0 | 1 | 2 | 3 | 4;
  phaseProgress: number; // 0 to 1 inside current phase
  globalProgress: number; // 0 to 1 overall
  fragmentedDispersion: number; // 1 = fully dispersed on left, 0 = converged to center
  coreIllumination: number; // 0 to 1 intensity
  unifiedNetworkOpacity: number; // 0 = invisible, 1 = fully illuminated on right
  pulseTraveling: number; // 0 to 1 traversal pulse across unified graph
}

export function evaluateTransformationTimeline(
  timeSeconds: number,
  loopDuration = 14.0
): TransformationTimeline {
  const normTime = timeSeconds % loopDuration;
  const globalProgress = normTime / loopDuration;

  let phaseIndex: 0 | 1 | 2 | 3 | 4 = 0;
  let phaseProgress = 0;
  let fragmentedDispersion = 1.0;
  let coreIllumination = 0.25;
  let unifiedNetworkOpacity = 0.15;
  let pulseTraveling = 0;

  // Phase 1: Fragmentation (0 to 3s -> 0.0 to 0.214)
  if (globalProgress < 0.214) {
    phaseIndex = 0;
    phaseProgress = globalProgress / 0.214;
    fragmentedDispersion = 1.0;
    coreIllumination = 0.25 + 0.1 * Math.sin(phaseProgress * Math.PI);
    unifiedNetworkOpacity = 0.15;
    pulseTraveling = 0;
  }
  // Phase 2: Transformation begins (3 to 6s -> 0.214 to 0.428)
  else if (globalProgress < 0.428) {
    phaseIndex = 1;
    phaseProgress = (globalProgress - 0.214) / 0.214;
    // Smooth ease in toward center
    const ease = 0.5 - 0.5 * Math.cos(phaseProgress * Math.PI);
    fragmentedDispersion = 1.0 - ease;
    coreIllumination = 0.35 + 0.55 * ease;
    unifiedNetworkOpacity = 0.15 + 0.25 * ease;
    pulseTraveling = 0;
  }
  // Phase 3: Knowledge structuring (6 to 9s -> 0.428 to 0.642)
  else if (globalProgress < 0.642) {
    phaseIndex = 2;
    phaseProgress = (globalProgress - 0.428) / 0.214;
    fragmentedDispersion = 0.0;
    // Core pulses at maximum radiance
    coreIllumination = 0.9 + 0.1 * Math.sin(phaseProgress * Math.PI * 4);
    unifiedNetworkOpacity = 0.4 + 0.6 * phaseProgress;
    pulseTraveling = phaseProgress;
  }
  // Phase 4: Unified knowledge (9 to 12s -> 0.642 to 0.856)
  else if (globalProgress < 0.856) {
    phaseIndex = 3;
    phaseProgress = (globalProgress - 0.642) / 0.214;
    fragmentedDispersion = 0.0;
    coreIllumination = 0.75 - 0.2 * phaseProgress;
    unifiedNetworkOpacity = 1.0;
    pulseTraveling = 0.5 + 0.5 * Math.sin(phaseProgress * Math.PI);
  }
  // Phase 5: Seamless reset (12 to 14s -> 0.856 to 1.0)
  else {
    phaseIndex = 4;
    phaseProgress = (globalProgress - 0.856) / 0.144;
    const easeReset = 0.5 - 0.5 * Math.cos(phaseProgress * Math.PI);
    fragmentedDispersion = easeReset;
    coreIllumination = 0.55 * (1 - easeReset) + 0.25 * easeReset;
    unifiedNetworkOpacity = 1.0 * (1 - easeReset) + 0.15 * easeReset;
    pulseTraveling = 0;
  }

  return {
    currentTime: normTime,
    totalDuration: loopDuration,
    phaseIndex,
    phaseProgress,
    globalProgress,
    fragmentedDispersion,
    coreIllumination,
    unifiedNetworkOpacity,
    pulseTraveling,
  };
}

