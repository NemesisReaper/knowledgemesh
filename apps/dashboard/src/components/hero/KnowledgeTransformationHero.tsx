import { Suspense, useMemo, useRef, useState } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { Html, Sparkles } from '@react-three/drei';
import * as THREE from 'three';
import './knowledge-hero.css';

const LOOP_SECONDS = 15;
const COUNT = 18;
const clamp01 = (v: number) => THREE.MathUtils.clamp(v, 0, 1);
const smooth = (a: number, b: number, x: number) => { const t = clamp01((x-a)/(b-a)); return t*t*(3-2*t); };
type PieceData = { from: THREE.Vector3; to: THREE.Vector3; scale: number; rot: THREE.Euler; kind: number; phase: number };

function GlassPiece({ data, index, progress }: { data: PieceData; index: number; progress: number }) {
  const ref = useRef<THREE.Group>(null);
  const material = useMemo(() => new THREE.MeshPhysicalMaterial({
    color: index % 3 === 0 ? '#a8c8ff' : '#dceaff',
    metalness: data.kind === 2 ? 0.68 : 0.16,
    roughness: 0.2,
    transmission: data.kind === 1 ? 0.55 : 0.12,
    thickness: 0.28,
    transparent: true,
    opacity: 0.86,
    clearcoat: 0.9,
    clearcoatRoughness: 0.16
  }), [data.kind, index]);

  useFrame(({ clock }) => {
    if (!ref.current) return;
    const t = clock.elapsedTime;
    const attract = smooth(0.20, 0.43, progress);
    const emerge = smooth(0.53, 0.78, progress);
    const settle = smooth(0.72, 0.88, progress);
    const transit = smooth(0.40, 0.48, progress) * (1 - smooth(0.51, 0.60, progress));
    const center = new THREE.Vector3(0, (index % 5 - 2) * 0.09, 0);
    const p = data.from.clone().lerp(center, attract).lerp(data.to, emerge);
    ref.current.position.set(p.x, p.y + Math.sin(t * 0.8 + data.phase) * 0.035, p.z);
    const fragment = 1 - smooth(0.38, 0.59, progress);
    const pulse = Math.sin(t * 1.1 + data.phase) * 0.025;
    ref.current.rotation.set(data.rot.x * fragment + pulse, data.rot.y * fragment + t * 0.1 * (1 - fragment), data.rot.z * fragment);
    ref.current.scale.setScalar(data.scale * (0.94 + 0.06 * settle));
    material.opacity = 0.86 * (1 - transit * 0.94);
  });

  return (
    <group ref={ref}>
      {data.kind === 0 ? (
        <mesh material={material}><boxGeometry args={[0.58, 0.78, 0.045]} /></mesh>
      ) : data.kind === 1 ? (
        <mesh material={material}><boxGeometry args={[0.7, 0.5, 0.11]} /></mesh>
      ) : (
        <mesh material={material}><octahedronGeometry args={[0.34, 0]} /></mesh>
      )}
      <mesh position={[0, 0, 0.04]}>
        <planeGeometry args={[0.36, 0.48]} />
        <meshBasicMaterial color="#a7d4ff" transparent opacity={0.10} />
      </mesh>
    </group>
  );
}

function Chamber({ progress }: { progress: number }) {
  const core = useRef<THREE.Group>(null);
  const ring1 = useRef<THREE.Mesh>(null);
  const ring2 = useRef<THREE.Mesh>(null);

  useFrame(({ clock }) => {
    const t = clock.elapsedTime;
    const active = smooth(0.18, 0.42, progress);
    if (core.current) {
      core.current.rotation.y = t * 0.14;
      core.current.rotation.x = Math.sin(t * 0.2) * 0.06;
      core.current.scale.setScalar(1 + active * 0.04 + Math.sin(t * 1.5) * 0.006);
    }
    if (ring1.current) ring1.current.rotation.z = t * (0.16 + active * 0.4);
    if (ring2.current) ring2.current.rotation.x = -t * (0.12 + active * 0.32);
  });

  return (
    <group ref={core}>
      <mesh>
        <icosahedronGeometry args={[0.68, 2]} />
        <meshPhysicalMaterial color="#5595ff" metalness={0.25} roughness={0.12} transmission={0.78} thickness={1} transparent opacity={0.7} clearcoat={1} />
      </mesh>
      <mesh ref={ring1}>
        <torusGeometry args={[0.98, 0.022, 16, 128]} />
        <meshStandardMaterial color="#a5d5ff" metalness={0.8} roughness={0.2} emissive="#286fe0" emissiveIntensity={1.25} />
      </mesh>
      <mesh ref={ring2} rotation={[Math.PI / 2.8, 0.2, 0]}>
        <torusGeometry args={[1.2, 0.013, 12, 128]} />
        <meshStandardMaterial color="#83eaff" metalness={0.7} roughness={0.22} emissive="#247dff" emissiveIntensity={1.1} />
      </mesh>
      <mesh>
        <sphereGeometry args={[0.105, 32, 32]} />
        <meshBasicMaterial color="#d1f5ff" />
      </mesh>
      <pointLight color="#438dff" intensity={2} distance={4} />
      <Html position={[0, -1.5, 0]} center>
        <div className="okf-core-label">OKF<span>KNOWLEDGE FORMAT</span></div>
      </Html>
    </group>
  );
}

function Network({ progress }: { progress: number }) {
  const lines = useMemo(() => Array.from({ length: 10 }, (_, i) => {
    const y = -1.25 + i * 0.28;
    return [new THREE.Vector3(1.1, y, -0.2), new THREE.Vector3(2.65, y + (i % 2 ? 0.18 : -0.18), -0.2)] as [THREE.Vector3, THREE.Vector3];
  }), []);
  const opacity = smooth(0.62, 0.82, progress) * 0.62 + 0.06;
  return (
    <group>
      {lines.map((points, i) => (
        <line key={i}>
          <bufferGeometry>
            <bufferAttribute attach="attributes-position" args={[new Float32Array(points.flatMap(p => p.toArray())), 3]} />
          </bufferGeometry>
          <lineBasicMaterial color={i % 2 ? '#65dfff' : '#6498ff'} transparent opacity={opacity} />
        </line>
      ))}
    </group>
  );
}

function Scene() {
  const [progress, setProgress] = useState(0);
  const elapsed = useRef(0);
  const pieces = useMemo<PieceData[]>(() => Array.from({ length: COUNT }, (_, i) => {
    const row = i % 6, col = Math.floor(i / 6);
    return {
      from: new THREE.Vector3(-3.15 - (col % 2) * 0.25 + (Math.random() - 0.5) * 0.18, (row - 2.5) * 0.48 + (Math.random() - 0.5) * 0.18, (col - 1) * 0.32),
      to: new THREE.Vector3(2.15 + (col % 2) * 0.25, (row - 2.5) * 0.43, (col - 1) * 0.2),
      scale: 0.64 + Math.random() * 0.18,
      rot: new THREE.Euler(Math.random() * 1.2, Math.random() * 1.2, (Math.random() - 0.5) * 1.1),
      kind: i % 3,
      phase: i * 0.71
    };
  }), []);

  useFrame((_, delta) => {
    elapsed.current = (elapsed.current + Math.min(delta, 0.04)) % LOOP_SECONDS;
    setProgress(elapsed.current / LOOP_SECONDS);
  });

  return (
    <>
      <color attach="background" args={['#070b14']} />
      <fog attach="fog" args={['#070b14', 8, 18]} />
      <ambientLight intensity={0.7} />
      <directionalLight position={[-4, 5, 6]} intensity={2} color="#d6e6ff" />
      <pointLight position={[0, 2, 3]} intensity={1.6} color="#397dff" />
      <pointLight position={[4, -2, -1]} intensity={1} color="#4ce4ff" />
      <Sparkles count={65} scale={[9, 5, 5]} size={1.3} speed={0.14} opacity={0.3} color="#8bbcff" />
      {pieces.map((p, i) => (
        <GlassPiece key={i} data={p} index={i} progress={progress} />
      ))}
      <Chamber progress={progress} />
      <Network progress={progress} />
    </>
  );
}

export interface KnowledgeTransformationHeroProps {
  onExplore?: () => void;
  onDocs?: () => void;
  onLogin?: () => void;
}

export default function KnowledgeTransformationHero({ onExplore, onDocs, onLogin }: KnowledgeTransformationHeroProps) {
  const [reducedMotion] = useState(() => typeof window !== 'undefined' && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  const [failed] = useState(false);

  return (
    <section className="okf-hero">
      <div className="okf-glow" />
      <header className="okf-nav">
        <a className="okf-brand" href="#top"><span>O</span> OKF</a>
        <div>OPEN KNOWLEDGE INFRASTRUCTURE</div>
        {onLogin && (
          <button onClick={onLogin} className="okf-secondary" style={{ padding: '0 14px', minHeight: 32, cursor: 'pointer' }}>
            🔐 Console Sign In
          </button>
        )}
      </header>

      <div className="okf-copy">
        <div className="okf-eyebrow"><i /> OPEN KNOWLEDGE FORMAT</div>
        <h1>From fragmented knowledge<br /><em>to a connected world.</em></h1>
        <p>A common foundation for structuring, sharing, and reusing knowledge across independent AI systems.</p>
        <div className="okf-actions">
          <a className="okf-primary" href="#explore" onClick={(e) => { if (onExplore) { e.preventDefault(); onExplore(); } }}>
            Explore OKF <span style={{ marginLeft: 4 }}>↗</span>
          </a>
          <a className="okf-secondary" href="#docs" onClick={(e) => { if (onDocs) { e.preventDefault(); onDocs(); } }}>
            Read documentation
          </a>
          {onLogin && (
            <button onClick={onLogin} className="okf-secondary" style={{ cursor: 'pointer' }}>
              🔐 Console Sign In
            </button>
          )}
        </div>
      </div>

      <div className="okf-scene" aria-label="3D animation showing fragmented knowledge transforming into a connected network">
        {!reducedMotion && !failed ? (
          <Canvas
            camera={{ position: [0, 0.25, 11], fov: 35 }}
            dpr={[1, 1.5]}
            gl={{ antialias: true, alpha: false, powerPreference: 'high-performance' }}
            onCreated={({ gl }) => {
              gl.toneMapping = THREE.ACESFilmicToneMapping;
              gl.toneMappingExposure = 1.05;
            }}
          >
            <Suspense fallback={null}>
              <Scene />
            </Suspense>
          </Canvas>
        ) : (
          <div className="okf-static">
            <div className="okf-fragments">{Array.from({ length: 6 }, (_, i) => <i key={i} />)}</div>
            <div className="okf-static-core">OKF</div>
            <div className="okf-network">{Array.from({ length: 6 }, (_, i) => <i key={i} />)}</div>
          </div>
        )}
      </div>

      <footer className="okf-foot">
        <span>01 / STRUCTURE</span>
        <span>KNOWLEDGE THAT TRAVELS</span>
        <span>02 / CONNECT</span>
      </footer>
    </section>
  );
}

