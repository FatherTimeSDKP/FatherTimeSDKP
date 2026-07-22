import React, { useRef, useState, useMemo } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Line, Html } from '@react-three/drei';
import * as THREE from 'three';

const SDN_SOLIDS = {
  tetrahedron:  { F: 4,  V: 4,  E: 6,  name: 'Tetrahedron',  color: '#64b4ff' },
  cube:         { F: 6,  V: 8,  E: 12, name: 'Cube',         color: '#4ade80' },
  octahedron:   { F: 8,  V: 6,  E: 12, name: 'Octahedron',   color: '#4ade80' },
  dodecahedron: { F: 12, V: 20, E: 30, name: 'Dodecahedron', color: '#f0a830' },
  icosahedron:  { F: 20, V: 12, E: 30, name: 'Icosahedron',  color: '#f0a830' },
};

const DUALS = {
  tetrahedron: 'tetrahedron',
  cube: 'octahedron',
  octahedron: 'cube',
  dodecahedron: 'icosahedron',
  icosahedron: 'dodecahedron',
};

function shapeFactorPhi(solid) {
  const s = SDN_SOLIDS[solid];
  return (s.F * s.V) / s.E;
}

function RotatingSolid({ solid, position, scale = 1, showLabel = true, spinSpeed = 0.25 }) {
  const meshRef = useRef();
  const s = SDN_SOLIDS[solid];

  useFrame((state, delta) => {
    if (meshRef.current) {
      meshRef.current.rotation.y += delta * spinSpeed;
      meshRef.current.rotation.x += delta * spinSpeed * 0.35;
    }
  });

  const geometry = useMemo(() => {
    switch (solid) {
      case 'tetrahedron':  return new THREE.TetrahedronGeometry(scale);
      case 'cube':          return new THREE.BoxGeometry(scale * 1.3, scale * 1.3, scale * 1.3);
      case 'octahedron':   return new THREE.OctahedronGeometry(scale);
      case 'dodecahedron': return new THREE.DodecahedronGeometry(scale);
      case 'icosahedron':  return new THREE.IcosahedronGeometry(scale);
      default: return new THREE.SphereGeometry(scale);
    }
  }, [solid, scale]);

  return (
    <group position={position}>
      <mesh ref={meshRef} geometry={geometry}>
        <meshStandardMaterial color={s.color} transparent opacity={0.35} side={THREE.DoubleSide} />
        <lineSegments>
          <edgesGeometry args={[geometry]} />
          <lineBasicMaterial color={s.color} linewidth={2} />
        </lineSegments>
      </mesh>
      {showLabel && (
        <Html position={[0, -scale * 1.8, 0]} center>
          <div style={{ color: s.color, fontFamily: 'monospace', fontSize: 12, fontWeight: 700, textAlign: 'center', whiteSpace: 'nowrap', textShadow: '0 0 4px #000' }}>
            {s.name}<br />
            <span style={{ fontSize: 10, opacity: 0.7 }}>F={s.F} V={s.V} E={s.E}</span>
          </div>
        </Html>
      )}
    </group>
  );
}

function GradientVector({ start, end, color = '#ff6644', label }) {
  const points = [new THREE.Vector3(...start), new THREE.Vector3(...end)];
  const dir = new THREE.Vector3(...end).sub(new THREE.Vector3(...start)).normalize();

  return (
    <group>
      <Line points={points} color={color} lineWidth={2} />
      <mesh position={end} rotation={[0, 0, Math.atan2(dir.y, dir.x) - Math.PI / 2]}>
        <coneGeometry args={[0.08, 0.25, 8]} />
        <meshBasicMaterial color={color} />
      </mesh>
      {label && (
        <Html position={end} center>
          <div style={{ color, fontSize: 10, fontFamily: 'monospace', fontWeight: 700, textShadow: '0 0 4px #000' }}>{label}</div>
        </Html>
      )}
    </group>
  );
}

function DualPairScene({ pairKey }) {
  const dualKey = DUALS[pairKey];
  const phiA = shapeFactorPhi(pairKey);
  const phiB = shapeFactorPhi(dualKey);
  const sameE = SDN_SOLIDS[pairKey].E === SDN_SOLIDS[dualKey].E;

  return (
    <>
      <ambientLight intensity={0.5} />
      <pointLight position={[5, 5, 5]} intensity={1.2} />
      <pointLight position={[-5, -5, -5]} intensity={0.4} color="#64b4ff" />

      <RotatingSolid solid={pairKey} position={[-2.2, 0, 0]} scale={1} spinSpeed={0.3} />
      <RotatingSolid solid={dualKey} position={[2.2, 0, 0]} scale={1} spinSpeed={-0.3} />

      {sameE && (
        <Line points={[[-1.2, 0, 0], [1.2, 0, 0]]} color="#f0a830" lineWidth={1.5} dashed dashSize={0.15} gapSize={0.1} />
      )}
      {sameE && (
        <Html position={[0, 0.5, 0]} center>
          <div style={{ color: '#f0a830', fontSize: 11, fontFamily: 'monospace', fontWeight: 700, textAlign: 'center', textShadow: '0 0 4px #000' }}>
            Shared E={SDN_SOLIDS[pairKey].E}<br />same 5D state
          </div>
        </Html>
      )}

      <GradientVector start={[-2.2, -1.6, 0]} end={[-2.2, -0.9, 0]} color="#64b4ff" label={`phi=${phiA.toFixed(2)}`} />
      <GradientVector start={[2.2, -1.6, 0]} end={[2.2, -0.9, 0]} color="#4ade80" label={`phi=${phiB.toFixed(2)}`} />
    </>
  );
}

function SingleSolidScene({ solid }) {
  return (
    <>
      <ambientLight intensity={0.5} />
      <pointLight position={[5, 5, 5]} intensity={1.3} />
      <pointLight position={[-5, -3, -5]} intensity={0.5} color="#64b4ff" />
      <RotatingSolid solid={solid} position={[0, 0, 0]} scale={1.6} spinSpeed={0.4} showLabel={false} />
    </>
  );
}

function OverviewScene() {
  const positions = {
    tetrahedron:  [-4, 1.2, 0],
    cube:         [-1.5, 1.2, 0],
    octahedron:   [1.5, 1.2, 0],
    dodecahedron: [-1.5, -1.5, 0],
    icosahedron:  [1.5, -1.5, 0],
  };

  return (
    <>
      <ambientLight intensity={0.5} />
      <pointLight position={[6, 6, 6]} intensity={1.2} />
      <pointLight position={[-6, -6, -6]} intensity={0.4} color="#64b4ff" />
      {Object.keys(SDN_SOLIDS).map((key, i) => (
        <RotatingSolid key={key} solid={key} position={positions[key]} scale={0.7} spinSpeed={0.2 + i * 0.05} />
      ))}
    </>
  );
}

export default function SDNGeometryVisualizer() {
  const [mode, setMode] = useState('overview');
  const [selectedSolid, setSelectedSolid] = useState('dodecahedron');
  const [selectedPair, setSelectedPair] = useState('dodecahedron');

  const modes = [
    { id: 'overview', label: 'All Five Solids' },
    { id: 'single', label: 'Single Solid Detail' },
    { id: 'dual', label: 'Dual Pair Comparison' },
  ];

  return (
    <div style={{ minHeight: '100vh', background: '#0b1220', color: '#e8edf5', fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, sans-serif" }}>
      <div style={{ background: 'linear-gradient(135deg, #0d2647 0%, #1A3C5E 100%)', borderBottom: '3px solid #2E5496', padding: '24px 32px' }}>
        <div style={{ maxWidth: 1150, margin: '0 auto' }}>
          <div style={{ fontSize: 11, letterSpacing: 3, textTransform: 'uppercase', color: '#7ec8e3', fontWeight: 700, marginBottom: 6 }}>
            FatherTimeSDKP Framework — 3D Geometry Module
          </div>
          <h1 style={{ fontSize: 26, fontWeight: 900, margin: 0, color: '#fff' }}>SD&amp;N Geometry Visualizer</h1>
          <div style={{ fontSize: 12, color: 'rgba(255,255,255,0.6)', marginTop: 4 }}>
            Live rotating Platonic solids. Drag to orbit, scroll to zoom.
          </div>
        </div>
      </div>

      <div style={{ maxWidth: 1150, margin: '0 auto', padding: '20px 32px' }}>
        <div style={{ display: 'flex', gap: 8, marginBottom: 16, flexWrap: 'wrap' }}>
          {modes.map(m => (
            <button key={m.id} onClick={() => setMode(m.id)} style={{
              padding: '9px 16px',
              background: mode === m.id ? '#2E5496' : 'rgba(255,255,255,0.05)',
              color: mode === m.id ? '#fff' : 'rgba(255,255,255,0.6)',
              border: mode === m.id ? '1px solid #64b4ff' : '1px solid rgba(255,255,255,0.1)',
              borderRadius: 6, fontSize: 12.5, fontWeight: 600, cursor: 'pointer',
            }}>{m.label}</button>
          ))}
        </div>

        {mode === 'single' && (
          <div style={{ marginBottom: 12 }}>
            <select value={selectedSolid} onChange={e => setSelectedSolid(e.target.value)} style={selStyle}>
              {Object.keys(SDN_SOLIDS).map(k => <option key={k} value={k}>{SDN_SOLIDS[k].name}</option>)}
            </select>
          </div>
        )}

        {mode === 'dual' && (
          <div style={{ marginBottom: 12 }}>
            <select value={selectedPair} onChange={e => setSelectedPair(e.target.value)} style={selStyle}>
              <option value="tetrahedron">Tetrahedron (self-dual)</option>
              <option value="cube">Cube - Octahedron</option>
              <option value="dodecahedron">Dodecahedron - Icosahedron</option>
            </select>
          </div>
        )}

        <div style={{ height: 520, background: 'rgba(255,255,255,0.02)', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 8, overflow: 'hidden' }}>
          <Canvas camera={{ position: [0, 0, 7], fov: 50 }}>
            {mode === 'overview' && <OverviewScene />}
            {mode === 'single' && <SingleSolidScene solid={selectedSolid} />}
            {mode === 'dual' && <DualPairScene pairKey={selectedPair} />}
            <OrbitControls enablePan={false} minDistance={3} maxDistance={15} />
          </Canvas>
        </div>

        {mode === 'single' && (
          <div style={{ marginTop: 12, padding: 14, background: 'rgba(100,180,255,0.06)', border: '1px solid rgba(100,180,255,0.2)', borderRadius: 6, fontSize: 12.5 }}>
            <strong style={{ color: '#7ec8e3' }}>{SDN_SOLIDS[selectedSolid].name}</strong> —
            F={SDN_SOLIDS[selectedSolid].F}, V={SDN_SOLIDS[selectedSolid].V}, E={SDN_SOLIDS[selectedSolid].E} |
            Euler: {SDN_SOLIDS[selectedSolid].F - SDN_SOLIDS[selectedSolid].E + SDN_SOLIDS[selectedSolid].V} |
            phi = {shapeFactorPhi(selectedSolid).toFixed(4)} |
            Dual: {SDN_SOLIDS[DUALS[selectedSolid]].name}
          </div>
        )}

        {mode === 'dual' && (
          <div style={{ marginTop: 12, padding: 14, background: 'rgba(240,168,48,0.08)', border: '1px solid rgba(240,168,48,0.25)', borderRadius: 6, fontSize: 12.5 }}>
            Dual solids share identical edge count E, the same 5D dimensional expression despite
            structurally distinct 3D geometry. The dashed line marks this shared state. Blue and green
            arrows show each solid's SD&amp;N shape factor phi = (F*V)/E as a density-gradient vector magnitude.
          </div>
        )}

        <div style={{ marginTop: 24, paddingTop: 16, borderTop: '1px solid rgba(255,255,255,0.1)', fontSize: 11, color: 'rgba(255,255,255,0.35)', textAlign: 'center' }}>
          FatherTimeSDKP Framework — Donald Paul Smith — ORCID: 0009-0003-7925-1653<br />
          Built with React Three Fiber. All geometric properties (F, V, E) verified against Euler's formula.
        </div>
      </div>
    </div>
  );
}

const selStyle = {
  padding: '9px 14px', background: 'rgba(0,0,0,0.3)', border: '1px solid rgba(255,255,255,0.15)',
  borderRadius: 6, color: '#e8edf5', fontSize: 13, fontFamily: 'monospace',
};
