"use client";

import React, { useEffect, useRef } from "react";

export interface KnowledgeTransformationSceneProps {
  theme?: "light" | "dark";
  onExploreOkf?: () => void;
  onReadDocs?: () => void;
}

export function KnowledgeTransformationScene({
  theme = "light",
  onExploreOkf,
  onReadDocs,
}: KnowledgeTransformationSceneProps) {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const containerRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    let animId: number | null = null;
    let renderer: any = null;

    function ensureThree(callback: () => void) {
      if ((window as any).THREE) {
        callback();
        return;
      }
      const script = document.createElement("script");
      script.src = "/three.min.js";
      script.async = true;
      script.onload = () => callback();
      script.onerror = () => {
        const cdn = document.createElement("script");
        cdn.src =
          "https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js";
        cdn.onload = () => callback();
        document.head.appendChild(cdn);
      };
      document.head.appendChild(script);
    }

    ensureThree(() => {
      const THREE = (window as any).THREE;
      if (!THREE) return;

      const canvas = canvasRef.current;
      const container = containerRef.current;
      if (!canvas || !container) return;

      const isLight = theme === "light";

      const width = Math.max(container.clientWidth || 700, 360);
      const height = Math.max(container.clientHeight || 640, 560);

      // 1. Scene - 100% Transparent, Unboxed
      const scene = new THREE.Scene();

      // 2. Camera with Generous Breathing Room (centered, no clipping)
      const camera = new THREE.PerspectiveCamera(40, width / height, 0.1, 50);
      camera.position.set(0, 0, 9.6);

      // 3. WebGL Renderer
      renderer = new THREE.WebGLRenderer({
        canvas,
        antialias: true,
        alpha: true,
        powerPreference: "high-performance",
      });
      renderer.setClearColor(0x000000, 0);
      renderer.setSize(width, height);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
      renderer.toneMapping = THREE.ACESFilmicToneMapping;
      renderer.toneMappingExposure = theme === "light" ? 1.35 : 1.25;

      // 4. Studio Lighting Rig tailored for Luxury Light Aesthetic & Cyan Sphere
      const ambientLight = new THREE.AmbientLight(0xffffff, 2.2);
      scene.add(ambientLight);

      // Key light: vibrant cyan highlight
      const keyLight = new THREE.DirectionalLight(0x38bdf8, 4.2);
      keyLight.position.set(-8, 12, 10);
      scene.add(keyLight);

      // Rim light: electric cyan edge definition
      const rimLight = new THREE.DirectionalLight(0x06b6d4, 3.6);
      rimLight.position.set(10, 8, -6);
      scene.add(rimLight);

      // Accent fill light: warm violet accent
      const violetLight = new THREE.PointLight(0xa855f7, 2.6, 25);
      violetLight.position.set(0, -6, 5);
      scene.add(violetLight);

      // Inner glowing core light: electric cyan core
      const innerCoreLight = new THREE.PointLight(0x38bdf8, 5.0, 14);
      innerCoreLight.position.set(0, 0, 0);
      scene.add(innerCoreLight);

      // 5. Build Interconnected Goldberg Polyhedron Dual Sphere (Hexagonal Voids)
      const phi = (1.0 + Math.sqrt(5.0)) / 2.0;
      const baseVerts = [
        [-1, phi, 0],
        [1, phi, 0],
        [-1, -phi, 0],
        [1, -phi, 0],
        [0, -1, phi],
        [0, 1, phi],
        [0, -1, -phi],
        [0, 1, -phi],
        [phi, 0, -1],
        [phi, 0, 1],
        [-phi, 0, -1],
        [-phi, 0, 1],
      ];
      const baseFaces = [
        [0, 11, 5],
        [0, 5, 1],
        [0, 1, 7],
        [0, 7, 10],
        [0, 10, 11],
        [1, 5, 9],
        [5, 11, 4],
        [11, 10, 2],
        [10, 7, 6],
        [7, 1, 8],
        [3, 9, 4],
        [3, 4, 2],
        [3, 2, 6],
        [3, 6, 8],
        [3, 8, 9],
        [4, 9, 5],
        [2, 4, 11],
        [6, 2, 10],
        [8, 6, 7],
        [9, 8, 1],
      ];

      const pVerts: any[] = [];
      for (let i = 0; i < baseVerts.length; i++) {
        const b = baseVerts[i];
        const len = Math.sqrt(b[0] * b[0] + b[1] * b[1] + b[2] * b[2]);
        pVerts.push(new THREE.Vector3(b[0] / len, b[1] / len, b[2] / len));
      }

      let pFaces = baseFaces;
      for (let step = 0; step < 2; step++) {
        const midCache = new Map<string, number>();
        function getMid(i1: number, i2: number): number {
          const k = Math.min(i1, i2) + "_" + Math.max(i1, i2);
          if (midCache.has(k)) return midCache.get(k)!;
          const v1 = pVerts[i1];
          const v2 = pVerts[i2];
          const mx = (v1.x + v2.x) * 0.5;
          const my = (v1.y + v2.y) * 0.5;
          const mz = (v1.z + v2.z) * 0.5;
          const len = Math.sqrt(mx * mx + my * my + mz * mz);
          const idx = pVerts.length;
          pVerts.push(new THREE.Vector3(mx / len, my / len, mz / len));
          midCache.set(k, idx);
          return idx;
        }
        const nextFaces: number[][] = [];
        for (let f = 0; f < pFaces.length; f++) {
          const tri = pFaces[f];
          const a = getMid(tri[0], tri[1]);
          const b = getMid(tri[1], tri[2]);
          const c = getMid(tri[2], tri[0]);
          nextFaces.push([tri[0], a, c]);
          nextFaces.push([tri[1], b, a]);
          nextFaces.push([tri[2], c, b]);
          nextFaces.push([a, b, c]);
        }
        pFaces = nextFaces;
      }

      // Shrunk to perfectly balanced scale (no clipping / out-of-bounds)
      const SPHERE_RADIUS = 1.7;
      const STRUT_RADIUS = 0.026;
      const NODE_RADIUS = 0.042;

      const dualVerts: any[] = [];
      for (let f = 0; f < pFaces.length; f++) {
        const tri = pFaces[f];
        const v0 = pVerts[tri[0]];
        const v1 = pVerts[tri[1]];
        const v2 = pVerts[tri[2]];
        const cx = (v0.x + v1.x + v2.x) / 3.0;
        const cy = (v0.y + v1.y + v2.y) / 3.0;
        const cz = (v0.z + v1.z + v2.z) / 3.0;
        const len = Math.sqrt(cx * cx + cy * cy + cz * cz);
        dualVerts.push(
          new THREE.Vector3(
            (cx / len) * SPHERE_RADIUS,
            (cy / len) * SPHERE_RADIUS,
            (cz / len) * SPHERE_RADIUS
          )
        );
      }

      const edgeToFaces = new Map<string, number[]>();
      for (let f = 0; f < pFaces.length; f++) {
        const tri = pFaces[f];
        const pairs = [
          [Math.min(tri[0], tri[1]), Math.max(tri[0], tri[1])],
          [Math.min(tri[1], tri[2]), Math.max(tri[1], tri[2])],
          [Math.min(tri[2], tri[0]), Math.max(tri[2], tri[0])],
        ];
        for (let p = 0; p < 3; p++) {
          const k = pairs[p][0] + "_" + pairs[p][1];
          if (!edgeToFaces.has(k)) edgeToFaces.set(k, []);
          edgeToFaces.get(k)!.push(f);
        }
      }

      const dualEdges: [number, number][] = [];
      edgeToFaces.forEach((fList) => {
        if (fList.length === 2) {
          dualEdges.push([fList[0], fList[1]]);
        }
      });

      const sphereGroup = new THREE.Group();
      scene.add(sphereGroup);

      // Signature Cyan & Ice-Blue Geodesic Buckyball Materials
      const strutMaterial = new THREE.MeshStandardMaterial({
        color: 0x67e8f9,
        emissive: 0x0284c7,
        emissiveIntensity: 0.55,
        metalness: 0.88,
        roughness: 0.15,
      });

      const nodeMaterial = new THREE.MeshStandardMaterial({
        color: 0x93c5fd,
        emissive: 0x38bdf8,
        emissiveIntensity: 0.70,
        metalness: 0.90,
        roughness: 0.12,
      });

      // Instanced Struts
      const cylinderUnitGeo = new THREE.CylinderGeometry(
        STRUT_RADIUS,
        STRUT_RADIUS,
        1.0,
        10
      );
      const instancedStruts = new THREE.InstancedMesh(
        cylinderUnitGeo,
        strutMaterial,
        dualEdges.length
      );
      instancedStruts.castShadow = true;
      instancedStruts.receiveShadow = true;

      const dummy = new THREE.Object3D();
      const upVector = new THREE.Vector3(0, 1, 0);

      for (let e = 0; e < dualEdges.length; e++) {
        const [idxA, idxB] = dualEdges[e];
        const vA = dualVerts[idxA];
        const vB = dualVerts[idxB];

        const midpoint = new THREE.Vector3()
          .addVectors(vA, vB)
          .multiplyScalar(0.5);
        const dir = new THREE.Vector3().subVectors(vB, vA);
        const len = dir.length();
        dir.normalize();

        dummy.position.copy(midpoint);
        dummy.quaternion.setFromUnitVectors(upVector, dir);
        dummy.scale.set(1.0, len, 1.0);
        dummy.updateMatrix();
        instancedStruts.setMatrixAt(e, dummy.matrix);
      }
      instancedStruts.instanceMatrix.needsUpdate = true;
      sphereGroup.add(instancedStruts);

      // Instanced Nodes
      const sphereUnitGeo = new THREE.SphereGeometry(NODE_RADIUS, 12, 12);
      const instancedNodes = new THREE.InstancedMesh(
        sphereUnitGeo,
        nodeMaterial,
        dualVerts.length
      );

      for (let n = 0; n < dualVerts.length; n++) {
        dummy.position.copy(dualVerts[n]);
        dummy.quaternion.set(0, 0, 0, 1);
        dummy.scale.set(1.0, 1.0, 1.0);
        dummy.updateMatrix();
        instancedNodes.setMatrixAt(n, dummy.matrix);
      }
      instancedNodes.instanceMatrix.needsUpdate = true;
      sphereGroup.add(instancedNodes);

      // Luminous Network Overlay
      const lineGeo = new THREE.BufferGeometry();
      const linePositions = new Float32Array(dualEdges.length * 6);
      for (let e = 0; e < dualEdges.length; e++) {
        const [idxA, idxB] = dualEdges[e];
        const vA = dualVerts[idxA];
        const vB = dualVerts[idxB];
        linePositions[e * 6 + 0] = vA.x;
        linePositions[e * 6 + 1] = vA.y;
        linePositions[e * 6 + 2] = vA.z;
        linePositions[e * 6 + 3] = vB.x;
        linePositions[e * 6 + 4] = vB.y;
        linePositions[e * 6 + 5] = vB.z;
      }
      lineGeo.setAttribute(
        "position",
        new THREE.BufferAttribute(linePositions, 3)
      );
      const lineMat = new THREE.LineBasicMaterial({
        color: isLight ? 0x818cf8 : 0x38bdf8,
        transparent: true,
        opacity: isLight ? 0.35 : 0.22,
      });
      const wireNetwork = new THREE.LineSegments(lineGeo, lineMat);
      sphereGroup.add(wireNetwork);

      // Floating Data Packet Particles along edges
      const particleCount = 28;
      const particleGeo = new THREE.BufferGeometry();
      const particlePositions = new Float32Array(particleCount * 3);
      const particleEdges: {
        edge: [number, number];
        t: number;
        speed: number;
      }[] = [];

      for (let p = 0; p < particleCount; p++) {
        const edge = dualEdges[Math.floor(Math.random() * dualEdges.length)];
        const t = Math.random();
        const speed = 0.25 + Math.random() * 0.45;
        particleEdges.push({ edge, t, speed });
        const vA = dualVerts[edge[0]];
        const vB = dualVerts[edge[1]];
        particlePositions[p * 3 + 0] = vA.x + (vB.x - vA.x) * t;
        particlePositions[p * 3 + 1] = vA.y + (vB.y - vA.y) * t;
        particlePositions[p * 3 + 2] = vA.z + (vB.z - vA.z) * t;
      }

      particleGeo.setAttribute(
        "position",
        new THREE.BufferAttribute(particlePositions, 3)
      );
      const particleMaterial = new THREE.PointsMaterial({
        color: isLight ? 0xf43f5e : 0x67e8f9,
        size: isLight ? 0.11 : 0.09,
        transparent: true,
        opacity: 0.95,
      });
      const particles = new THREE.Points(particleGeo, particleMaterial);
      sphereGroup.add(particles);

      // Orbital Sparkles
      const sparkleCount = 42;
      const sparkleGeo = new THREE.BufferGeometry();
      const sparklePositions = new Float32Array(sparkleCount * 3);
      for (let s = 0; s < sparkleCount; s++) {
        const rad = 2.2 + Math.random() * 1.3;
        const theta = Math.random() * Math.PI * 2;
        const phiAngle = Math.acos(Math.random() * 2 - 1);
        sparklePositions[s * 3 + 0] =
          rad * Math.sin(phiAngle) * Math.cos(theta);
        sparklePositions[s * 3 + 1] =
          rad * Math.sin(phiAngle) * Math.sin(theta);
        sparklePositions[s * 3 + 2] = rad * Math.cos(phiAngle);
      }
      sparkleGeo.setAttribute(
        "position",
        new THREE.BufferAttribute(sparklePositions, 3)
      );
      const sparkles = new THREE.Points(
        sparkleGeo,
        new THREE.PointsMaterial({
          color: isLight ? 0x818cf8 : 0x93c5fd,
          size: 0.065,
          transparent: true,
          opacity: isLight ? 0.55 : 0.45,
        })
      );
      scene.add(sparkles);

      // Cursor Gyro Interaction
      let targetTiltX = 0;
      let targetTiltY = 0;
      let currentTiltX = 0;
      let currentTiltY = 0;
      let cursorVelX = 0;
      let lastPointerX = 0;

      function onPointerMove(e: MouseEvent) {
        if (!canvas) return;
        const rect = canvas.getBoundingClientRect();
        const cx = (e.clientX - rect.left) / rect.width;
        const cy = (e.clientY - rect.top) / rect.height;
        const cursorX = (cx - 0.5) * 2;
        const cursorY = (cy - 0.5) * 2;

        targetTiltY = cursorX * 0.45;
        targetTiltX = -cursorY * 0.35;

        const dx = cursorX - lastPointerX;
        lastPointerX = cursorX;
        cursorVelX = dx * 0.003;
      }

      function onTouchMove(e: TouchEvent) {
        if (e.touches.length > 0) {
          onPointerMove(e.touches[0] as unknown as MouseEvent);
        }
      }

      window.addEventListener("mousemove", onPointerMove, { passive: true });
      window.addEventListener("touchmove", onTouchMove, { passive: true });

      function onResize() {
        if (!canvas || !container) return;
        const nw = Math.max(container.clientWidth || 700, 360);
        const nh = Math.max(container.clientHeight || 640, 560);
        camera.aspect = nw / nh;
        camera.updateProjectionMatrix();
        renderer.setSize(nw, nh);
      }
      window.addEventListener("resize", onResize);

      let lastTime = performance.now();
      const baseRotationSpeed = 0.0042; // Continuous Left-to-Right rotation

      function animate(now: number) {
        if (!canvasRef.current) return;
        const dt = Math.min((now - lastTime) / 1000, 0.05);
        lastTime = now;

        // Smooth continuous left-to-right rotation on Y-axis
        cursorVelX *= 0.94;
        sphereGroup.rotation.y += baseRotationSpeed + cursorVelX;

        // Smooth Gyro tilt
        currentTiltX += (targetTiltX - currentTiltX) * 0.06;
        currentTiltY += (targetTiltY - currentTiltY) * 0.06;
        sphereGroup.rotation.x = currentTiltX;
        sphereGroup.rotation.z = -currentTiltY * 0.35;

        // Subtle zero-gravity breathing (shifted gracefully above center)
        sphereGroup.position.y = 0.32 + Math.sin(now * 0.0014) * 0.08;

        // Packet progression along edges
        const posAttrP = particleGeo.attributes.position;
        const arr = posAttrP.array as Float32Array;
        for (let p = 0; p < particleCount; p++) {
          const item = particleEdges[p];
          item.t += dt * item.speed;
          if (item.t >= 1.0) {
            item.t = 0.0;
            item.edge =
              dualEdges[Math.floor(Math.random() * dualEdges.length)];
          }
          const vA = dualVerts[item.edge[0]];
          const vB = dualVerts[item.edge[1]];
          arr[p * 3 + 0] = vA.x + (vB.x - vA.x) * item.t;
          arr[p * 3 + 1] = vA.y + (vB.y - vA.y) * item.t;
          arr[p * 3 + 2] = vA.z + (vB.z - vA.z) * item.t;
        }
        posAttrP.needsUpdate = true;

        sparkles.rotation.y -= 0.001;

        renderer.render(scene, camera);
        animId = requestAnimationFrame(animate);
      }

      animId = requestAnimationFrame(animate);
    });

    return () => {
      if (animId) cancelAnimationFrame(animId);
      if (renderer) {
        try {
          renderer.dispose();
        } catch (e) {}
      }
    };
  }, [theme]);

  return (
    <div
      ref={containerRef}
      style={{
        position: "relative",
        width: "100%",
        height: "640px",
        minHeight: "560px",
        background: "transparent",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        overflow: "visible",
      }}
    >
      <div
        className="km-sphere-wrapper"
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          zIndex: 1,
        }}
      >
        <canvas
          ref={canvasRef}
          style={{
            width: "100%",
            height: "100%",
            display: "block",
            background: "transparent",
          }}
        />
      </div>
      {/* Single unified cyan ground shadow matching the sphere with synchronous breathing */}
      <div
        aria-hidden="true"
        className="km-sphere-shadow"
        style={{
          position: "absolute",
          bottom: "52px",
          left: "50%",
          transform: "translateX(-50%)",
          width: "320px",
          height: "40px",
          borderRadius: "50%",
          background:
            "radial-gradient(ellipse at center, rgba(6, 182, 212, 0.52) 0%, rgba(56, 189, 248, 0.30) 35%, rgba(14, 165, 233, 0.10) 65%, transparent 80%)",
          filter: "blur(10px)",
          pointerEvents: "none",
          zIndex: 0,
        }}
      />
    </div>
  );
}