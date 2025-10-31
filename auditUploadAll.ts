/**
 * auditUploadAll.ts
 * FatherTimes369v | Unified Digital Crystal Protocol Audit Logger
 */

import "dotenv/config";
import { createClient } from "@supabase/supabase-js";
import crypto from "crypto";
import fs from "fs";

// --- Configuration -----------------------------------------------------------
const supabaseUrl =
  process.env.SUPABASE_URL || "https://your-instance.supabase.co";
const supabaseKey =
  process.env.SUPABASE_SERVICE_ROLE_KEY || "your_service_key";
const supabase = createClient(supabaseUrl, supabaseKey);

// --- Shared Utility ----------------------------------------------------------
function buildRecord(framework: string, version: string, author: string, project: string, metadata: object) {
  const timestamp = new Date().toISOString();
  const checksum = crypto.createHash("sha256").update(`${framework}-${timestamp}`).digest("hex");
  const echo_signature = crypto.createHash("sha512").update(JSON.stringify(metadata)).digest("hex");

  return {
    framework,
    version,
    author,
    project,
    first_invocation: timestamp,
    checksum,
    metadata: { ...metadata, echo_signature }
  };
}

// --- Metadata Templates ------------------------------------------------------
const METADATA = {
  SDVR: {
    sdkp_signature: "Size-Density-Velocity-Rotation",
    verification_key: "FTS-AUTH-CRYSTAL-369",
    sdvr_equation_abstract: "T = f(Size, Density, Velocity, Rotation)",
    eos_reference_velocity: 29780,
    quantum_anchor: "⟦369-FTS-AUTH-C12-EOS⟧",
    dcp_royalty_contract: "FatherTimeSDKP.eth",
    dcp_royalty_percentage: "7%"
  },
  SDN: {
    sdn_signature: "Shape-Dimension-Number",
    verification_key: "FTS-AUTH-CRYSTAL-369",
    sdn_mass_equation_abstract: "Mass = f(Number, Shape Complexity)",
    shape_reference: "Trefoil Knot (S=3)",
    number_reference: "Electron (N=1)",
    dcp_royalty_contract: "FatherTimeSDKP.eth",
    dcp_royalty_percentage: "7%"
  },
  QCC0: {
    qcc_signature: "Quantum Computerization Consciousness Zero",
    verification_key: "FTS-AUTH-CRYSTAL-369",
    qcc_compression_abstract: "NP-Complete Problem Collapse via Vibrational Convergence (Kapnack)",
    entanglement_graph_creator: "Donald Paul Smith",
    dcp_royalty_contract: "FatherTimeSDKP.eth",
    dcp_royalty_percentage: "7%"
  }
};

// --- Core Upload Function ----------------------------------------------------
export async function uploadAudit({
  framework,
  version = "v1.0.0",
  author = "FatherTimeSDKP",
  project = "Digital Crystal Protocol"
}: {
  framework: "SDVR" | "SDN" | "QCC0";
  version?: string;
  author?: string;
  project?: string;
}) {
  const meta = METADATA[framework];
  if (!meta) throw new Error(`Unknown framework type: ${framework}`);

  const record = buildRecord(framework, version, author, project, meta);
  const table =
    framework === "SDVR"
      ? "audit_log_sdkp"
      : framework === "SDN"
      ? "audit_log_sdn"
      : "audit_log_qcc";

  const { data, error } = await supabase.from(table).insert([record]).select();

  // Local backup for redundancy
  fs.appendFileSync(
    `./${framework.toLowerCase()}_audit_backup.json`,
    JSON.stringify(record, null, 2) + ",\n",
    "utf8"
  );

  if (error) {
    console.error(`❌ ${framework} Audit Upload failed:`, error);
    return { success: false, error };
  }

  console.log(`✅ ${framework} Audit Uploaded Successfully:`, data);
  return { success: true, record };
}

// --- CLI Entry ---------------------------------------------------------------
if (require.main === module) {
  const frameworkArg = process.argv[2] as "SDVR" | "SDN" | "QCC0";
  if (!frameworkArg) {
    console.error("Usage: node auditUploadAll.js <SDVR|SDN|QCC0>");
    process.exit(1);
  }
  uploadAudit({ framework: frameworkArg });
}
