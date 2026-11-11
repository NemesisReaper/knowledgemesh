"use client";

import React, { useEffect, useRef, useState } from "react";

export interface KnowledgeTransformationSceneProps {
  onExploreOkf?: () => void;
  onReadDocs?: () => void;
}

export function KnowledgeTransformationScene({
  onExploreOkf,
  onReadDocs,
}: KnowledgeTransformationSceneProps) {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const containerRef = useRef<HTMLDivElement | null>(null);
  const [phaseDisplay, setPhaseDisplay] = useState<string>(
    "Interconnected 3D Lattice Sphere · Left-to-Right Rotation"
  );

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
        cdn.src = "https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js";
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

      const width = container.clientWidth || 700;
      const height = container.clientHeight || 520;

      // 1. Scene & Atmosphere matching KnowMesh theme
      const scene = new THREE.Scene();
      scene.background = new THREE.Color(0x070b14);
      scene.fog = new THREE.Fog(0x070b14, 10, 26);

      // 2. Camera
      const camera = new THREE.PerspectiveCamera(38, width / height, 0.1, 50);
      camera.position.set(0, 0, 10.5);

      // 3. WebGL Renderer
      renderer = new THREE.WebGLRenderer({
        canvas,
        antialias: true,
        alpha: true,
        powerPreference: "high-performance",
      });
      renderer.setSize(width, height);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
      renderer.toneMapping = THREE.ACESFilmicToneMapping;
      renderer.toneMappingExposure = 1.15;

      // 4. Lighting Rig
      const ambientLight = new THREE.AmbientLight(0x0e1726, 1.8);
      scene.add(ambientLight);

      const keyLight = new THREE.DirectionalLight(0x38bdf8, 3.2);
      keyLight.position.set(-8, 10, 10);
      scene.add(keyLight);

      const rimLight = new THREE.DirectionalLight(0x06b6d4, 2.6);
      rimLight.position.set(9, 6, -7);
      scene.add(rimLight);

      const violetLight = new THREE.PointLight(0xa855f7, 2.0, 25);
      violetLight.position.set(0, -6, 4);
      scene.add(violetLight);

      const innerCoreLight = new THREE.PointLight(0x38bdf8, 3.0, 9);
      innerCoreLight.position.set(0, 0, 0);
      scene.add(innerCoreLight);

      // 5. Build Interconnected 3D Sphere
      const SPHERE_RADIUS = 3.15;
      const STRUT_RADIUS = 0.042;
      const NODE_RADIUS = 0.072;

      const baseGeo = new THREE.IcosahedronGeometry(SPHERE_RADIUS, 2);
      const posAttr = baseGeo.attributes.position;
      const indexAttr = baseGeo.index;

      const uniqueVerts: any[] = [];
      const vertMap = new Map();
      function getVertIndex(x: number, y: number, z: number) {
        const key = x.toFixed(3) + "," + y.toFixed(3) + "," + z.toFixed(3);
        if (vertMap.has(key)) return vertMap.get(key);
        const idx = uniqueVerts.length;
        uniqueVerts.push(new THREE.Vector3(x, y, z));
        vertMap.set(key, idx);
        return idx;
      }

      const edgeSet = new Set();
      const uniqueEdges: [number, number][] = [];

      for (let i = 0; i < indexAttr.count; i += 3) {
        const ia = indexAttr.getX(i);
        const ib = indexAttr.getX(i + 1);
        const ic = indexAttr.getX(i + 2);

        const va = getVertIndex(posAttr.getX(ia), posAttr.getY(ia), posAttr.getZ(ia));
        const vb = getVertIndex(posAttr.getX(ib), posAttr.getY(ib), posAttr.getZ(ib));
        const vc = getVertIndex(posAttr.getX(ic), posAttr.getY(ic), posAttr.getZ(ic));

        const addEdge = (u: number, v: number) => {
          const min = Math.min(u, v);
          const max = Math.max(u, v);
          const k = min + "_" + max;
          if (!edgeSet.has(k)) {
            edgeSet.add(k);
            uniqueEdges.push([min, max]);
          }
        };

        addEdge(va, vb);
        addEdge(vb, vc);
        addEdge(vc, va);
      }

      // Organic Voronoi-cellular tangential perturbation
      for (let i = 0; i < uniqueVerts.length; i++) {
        const v = uniqueVerts[i];
        const norm = v.clone().normalize();
        const tangentDisplacement = new THREE.Vector3(
          Math.sin(i * 1.95 + 0.4),
          Math.cos(i * 2.65 + 0.9),
          Math.sin(i * 3.35 + 1.3)
        )
          .cross(norm)
          .multiplyScalar(0.24);
        v.add(tangentDisplacement).normalize().multiplyScalar(SPHERE_RADIUS);
      }

      // Crystalline Ice-Cyan Physical Material
      const latticeMaterial = new THREE.MeshPhysicalMaterial({
        color: 0x7dd3fc,
        emissive: 0x0284c7,
        emissiveIntensity: 0.22,
        roughness: 0.12,
        metalness: 0.28,
        transmission: 0.6,
        thickness: 0.5,
        transparent: true,
        opacity: 0.92,
        clearcoat: 1.0,
        clearcoatRoughness: 0.08,
        ior: 1.52,
      });

      const sphereGroup = new THREE.Group();
      scene.add(sphereGroup);

      // Instanced Struts (cylinders)
      const cylinderUnitGeo = new THREE.CylinderGeometry(STRUT_RADIUS, STRUT_RADIUS, 1.0, 10);
      const instancedStruts = new THREE.InstancedMesh(
        cylinderUnitGeo,
        latticeMaterial,
        uniqueEdges.length
      );
      instancedStruts.castShadow = true;
      instancedStruts.receiveShadow = true;

      const dummy = new THREE.Object3D();
      const upVector = new THREE.Vector3(0, 1, 0);

      for (let e = 0; e < uniqueEdges.length; e++) {
        const [idxA, idxB] = uniqueEdges[e];
        const vA = uniqueVerts[idxA];
        const vB = uniqueVerts[idxB];

        const midpoint = new THREE.Vector3().addVectors(vA, vB).multiplyScalar(0.5);
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

      // Instanced Nodes (spheres at intersections)
      const sphereUnitGeo = new THREE.SphereGeometry(NODE_RADIUS, 14, 14);
      const nodeMaterial = new THREE.MeshPhysicalMaterial({
        color: 0x93c5fd,
        emissive: 0x38bdf8,
        emissiveIntensity: 0.35,
        roughness: 0.1,
        metalness: 0.35,
        clearcoat: 1.0,
        clearcoatRoughness: 0.05,
      });
      const instancedNodes = new THREE.InstancedMesh(
        sphereUnitGeo,
        nodeMaterial,
        uniqueVerts.length
      );

      for (let n = 0; n < uniqueVerts.length; n++) {
        dummy.position.copy(uniqueVerts[n]);
        dummy.quaternion.set(0, 0, 0, 1);
        dummy.scale.set(1.0, 1.0, 1.0);
        dummy.updateMatrix();
        instancedNodes.setMatrixAt(n, dummy.matrix);
      }
      instancedNodes.instanceMatrix.needsUpdate = true;
      sphereGroup.add(instancedNodes);

      // Internal Suspended Core
      const innerWireGeo = new THREE.IcosahedronGeometry(1.1, 1);
      const innerWireMat = new THREE.MeshBasicMaterial({
        color: 0x38bdf8,
        wireframe: true,
        transparent: true,
        opacity: 0.35,
      });
      const innerWireMesh = new THREE.Mesh(innerWireGeo, innerWireMat);
      sphereGroup.add(innerWireMesh);

      const innerGlowGeo = new THREE.SphereGeometry(0.35, 24, 24);
      const innerGlowMat = new THREE.MeshStandardMaterial({
        color: 0x38bdf8,
        emissive: 0x0284c7,
        emissiveIntensity: 1.5,
        roughness: 0.2,
      });
      const innerGlowMesh = new THREE.Mesh(innerGlowGeo, innerGlowMat);
      sphereGroup.add(innerGlowMesh);

      // Streaming Data Particles along the lattice
      const particleCount = 40;
      const particleGeo = new THREE.BufferGeometry();
      const particlePositions = new Float32Array(particleCount * 3);
      const particleEdges: number[] = [];
      const particleProgress = new Float32Array(particleCount);
      const particleSpeeds = new Float32Array(particleCount);

      for (let p = 0; p < particleCount; p++) {
        particleEdges.push(Math.floor(Math.random() * uniqueEdges.length));
        particleProgress[p] = Math.random();
        particleSpeeds[p] = 0.25 + Math.random() * 0.45;
      }
      particleGeo.setAttribute("position", new THREE.BufferAttribute(particlePositions, 3));
      const particleMaterial = new THREE.PointsMaterial({
        color: 0x38bdf8,
        size: 0.12,
        transparent: true,
        opacity: 0.95,
      });
      const particlePoints = new THREE.Points(particleGeo, particleMaterial);
      sphereGroup.add(particlePoints);

      // Ambient Sparkles in surrounding space
      const sparkleCount = 50;
      const sparkleGeo = new THREE.BufferGeometry();
      const sparklePositions = new Float32Array(sparkleCount * 3);
      for (let s = 0; s < sparkleCount; s++) {
        sparklePositions[s * 3] = (Math.random() - 0.5) * 14.0;
        sparklePositions[s * 3 + 1] = (Math.random() - 0.5) * 10.0;
        sparklePositions[s * 3 + 2] = (Math.random() - 0.5) * 8.0;
      }
      sparkleGeo.setAttribute("position", new THREE.BufferAttribute(sparklePositions, 3));
      const sparkles = new THREE.Points(
        sparkleGeo,
        new THREE.PointsMaterial({
          color: 0x8bbcff,
          size: 0.07,
          transparent: true,
          opacity: 0.35,
        })
      );
      scene.add(sparkles);

      // Interactive Cursor Tracking
      let cursorX = 0,
        cursorY = 0;
      let targetTiltX = 0,
        targetTiltZ = 0;
      let cursorVelX = 0,
        lastClientX = 0;

      const onMouseMove = (e: MouseEvent) => {
        const rect = canvas.getBoundingClientRect();
        cursorX = ((e.clientX - rect.left) / rect.width - 0.5) * 2;
        cursorY = ((e.clientY - rect.top) / rect.height - 0.5) * 2;

        const dx = e.clientX - lastClientX;
        lastClientX = e.clientX;
        cursorVelX = dx * 0.0015;
      };

      const onMouseLeave = () => {
        cursorX = 0;
        cursorY = 0;
      };

      canvas.addEventListener("mousemove", onMouseMove);
      canvas.addEventListener("mouseleave", onMouseLeave);

      const onResize = () => {
        if (!container || !renderer || !camera) return;
        const w = container.clientWidth || 700;
        const h = container.clientHeight || 520;
        camera.aspect = w / h;
        camera.updateProjectionMatrix();
        renderer.setSize(w, h);
      };
      window.addEventListener("resize", onResize);

      // 6. Animation Loop: Left-to-Right Continuous Rotation + Cursor Gyro Reaction
      function animate(now: number) {
        if (!canvasRef.current) return;

        // Continuous Rotation: Left to Right (+Y rotation moves front face left to right)
        const baseSpeed = 0.0065;
        sphereGroup.rotation.y += baseSpeed + cursorVelX;
        cursorVelX *= 0.94; // damping inertia

        // Interactive Cursor Tilt
        targetTiltX = cursorY * 0.55;
        targetTiltZ = -cursorX * 0.4;
        sphereGroup.rotation.x += (targetTiltX - sphereGroup.rotation.x) * 0.06;
        sphereGroup.rotation.z += (targetTiltZ - sphereGroup.rotation.z) * 0.06;

        // Internal core counter-rotation & pulsation
        innerWireMesh.rotation.y -= 0.012;
        innerWireMesh.rotation.x += 0.006;
        innerCoreLight.intensity = 2.4 + Math.sin(now * 0.003) * 0.8;

        // Animate data flow particles along edges
        const pArr = particlePoints.geometry.attributes.position.array;
        for (let p = 0; p < particleCount; p++) {
          particleProgress[p] = (particleProgress[p] + particleSpeeds[p] * 0.014) % 1.0;
          const edge = uniqueEdges[particleEdges[p]];
          const vA = uniqueVerts[edge[0]];
          const vB = uniqueVerts[edge[1]];
          const pr = particleProgress[p];

          pArr[p * 3] = vA.x + (vB.x - vA.x) * pr;
          pArr[p * 3 + 1] = vA.y + (vB.y - vA.y) * pr;
          pArr[p * 3 + 2] = vA.z + (vB.z - vA.z) * pr;
        }
        particlePoints.geometry.attributes.position.needsUpdate = true;

        // Sparkles gentle rotation
        sparkles.rotation.y = now * 0.00015;

        // Parallax Camera gliding
        camera.position.x += (cursorX * 0.55 - camera.position.x) * 0.05;
        camera.position.y += (-cursorY * 0.35 - camera.position.y) * 0.05;
        camera.lookAt(0, 0, 0);

        renderer.render(scene, camera);
        animId = requestAnimationFrame(animate);
      }

      animId = requestAnimationFrame(animate);
    });

    return () => {
      if (animId) cancelAnimationFrame(animId);
      if (renderer) renderer.dispose();
    };
  }, []);

  return (
    <div
      ref={containerRef}
      style={{
        position: "relative",
        width: "100%",
        height: "100%",
        minHeight: 520,
        overflow: "hidden",
      }}
    >
      <canvas
        ref={canvasRef}
        style={{
          display: "block",
          width: "100%",
          height: "100%",
        }}
      />
      <div
        style={{
          position: "absolute",
          top: 14,
          left: 18,
          display: "inline-flex",
          alignItems: "center",
          gap: 8,
          padding: "5px 14px",
          background: "rgba(11, 18, 32, 0.85)",
          backdropFilter: "blur(8px)",
          borderRadius: 999,
          border: "1px solid rgba(56, 189, 248, 0.45)",
          fontSize: 11.5,
          color: "#38bdf8",
          fontWeight: 600,
          zIndex: 10,
          pointerEvents: "none",
        }}
      >
        <span style={{ color: "#38D399" }}>●</span> <span>{phaseDisplay}</span>
      </div>

      <div className="km-okf-center-badge">
        <span className="km-okf-pill">KNOWMESH</span>
        <span style={{ fontSize: 9.5, color: "#94A3B8", letterSpacing: "0.06em" }}>
          INTERCONNECTED 3D SPHERE
        </span>
      </div>

      <div className="km-zone-label km-zone-left">
        ◄ ROTATING LEFT TO RIGHT
      </div>
      <div className="km-zone-label km-zone-right">
        CURSOR-RESPONSIVE GYRO ►
      </div>
    </div>
  );
}
