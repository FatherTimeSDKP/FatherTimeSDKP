/**
 * SDVR module stub — matches sdkp_core.js call signature:
 *   sdvr.calculate(qccResult)
 *
 * SDVR = Size × Density × Velocity × Rotation
 * Drop into: FatherTimeSDKP/src/modules/sdvr.js
 *
 * This is a deterministic stub so POST /run-sdkp can complete end-to-end.
 * Replace calculate() body with full SDVR engine when ready.
 */

"use strict";

/** @param {unknown} value @param {number} fallback */
function num(value, fallback = 0) {
  const n = Number(value);
  return Number.isFinite(n) ? n : fallback;
}

/**
 * Pull SDVR parameters from the original request (nested under qccResult.input)
 * or from top-level fields on the QCC result.
 * @param {object} qccResult
 */
function extractParams(qccResult) {
  const src =
    qccResult && typeof qccResult === "object" && qccResult.input
      ? qccResult.input
      : qccResult || {};

  return {
    size: num(src.size ?? src.S, 1.0),
    density: num(src.density ?? src.D, 1.0),
    velocity: num(src.velocity ?? src.V, 0.0),
    rotation: num(src.rotation ?? src.R, 0.0),
    solid: typeof src.solid === "string" ? src.solid : "cube",
  };
}

/**
 * @param {object} qccResult — output of qcc0.process(input)
 * @returns {object} sdvrResult consumed by llal.loop(qccResult, sdvrResult)
 */
function calculate(qccResult) {
  const params = extractParams(qccResult);
  const { size, density, velocity, rotation, solid } = params;

  // Φ_SDVR = S · D · V · R  (macro field magnitude; same product form as framework notes)
  const phi = size * density * velocity * rotation;

  // Lightweight shape factor placeholders (Platonic F·V/E style), stub only
  const shapeTable = {
    tetrahedron: (4 * 4) / 6,
    cube: (6 * 8) / 12,
    octahedron: (8 * 6) / 12,
    dodecahedron: (12 * 20) / 30,
    icosahedron: (20 * 12) / 30,
    sphere: 1,
  };
  const shapeFactor = shapeTable[solid] ?? shapeTable.cube;

  const qccScalar = num(
    qccResult && qccResult.result != null ? qccResult.result : 0,
    0
  );

  return {
    stage: "SDVR Calculate",
    params: { size, density, velocity, rotation, solid },
    phi_SDVR: phi,
    shapeFactor,
    // couple QCC scalar into a simple normalized score for downstream LLAL
    sdvrScore: phi === 0 ? qccScalar : phi * (1 + qccScalar),
    fromQcc: {
      stage: qccResult && qccResult.stage,
      result: qccResult && qccResult.result,
    },
  };
}

module.exports = {
  calculate,
};
