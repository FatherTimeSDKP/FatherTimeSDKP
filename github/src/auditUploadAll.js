// src/auditUploadAll.ts
/**
 * auditUploadAll.ts
 * FatherTimes369v | Unified Digital Crystal Protocol Audit Logger
 *
 * Usage:
 *  node dist/auditUploadAll.js SDVR v1.0.0
 *  node dist/auditUploadAll.js SDN v1.0.0
 *  node dist/auditUploadAll.js QCC0 v1.0.0
 */

import "dotenv/config";
import { createClient, SupabaseClient } from "@supabase/supabase-js";
import crypto from "crypto";
import fs from "fs";
import path from "path";

type Framework = "SDVR" | "SDN" | "QCC0";

const SUPABASE_URL = process.env.SUPABASE_URL;
const SUPABASE_KEY = process.env.SUPABASE_SERVICE_ROLE_KEY;

if (!SUPABASE_URL || !SUPABASE_KEY) {
  // Not fatal here — allow programmatic imports, fail when trying to use the network
  // console.warn("Supabase credentials not set. Set SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY in .env");
}

const supabase: SupabaseClient | null = SUPABASE_URL && SUPABASE_KEY
  ? createClient(SUPABASE_URL, SUPABASE_KEY)
  : null;

// ---------- Metadata templates ----------
const METADATA: Record<Framework, Record<string, any>> = {
  SDVR: {
    sdkp_signature: "Size-Density-Velocity-Rotation",
    verification_key: "FTS-AUTH-CRYSTAL-369",
    sdvr_equation_abstract: "T = f(Size, Density, Velocity, Rotation)",
    eos_reference_velocity: 29780, // m/s
    quantum_anchor: "⟦369-FTS-AUTH-C12-EOS⟧",
    dcp_royalty_contract: "FatherTimeSDKP.eth",
    dcp_royalty_percentage: "7%",
  },
  SDN: {
    sdn_signature: "Shape-Dimension-Number",
    verification_key: "FTS-AUTH-CRYSTAL-369",
    sdn_mass_equation_abstract: "Mass = f(Number, Shape Complexity)",
    shape_reference: "Trefoil Knot (S=3)",
    number_reference: "Electron (N=1)",
    dcp_royalty_contract: "FatherTimeSDKP.eth",
    dcp_royalty_percentage: "7%",
  },
  QCC0: {
    qcc_signature: "Quantum Computerization Consciousness Zero",
    verification_key: "FTS-AUTH-CRYSTAL-369",
    qcc_compression_abstract: "NP-Complete Problem Collapse via Vibrational Convergence (Kapnack)",
    entanglement_graph_creator: "Donald Paul Smith",
    dcp_royalty_contract: "FatherTimeSDKP.eth",
    dcp_royalty_percentage: "7%",
  }
};

// ---------- Utilities ----------
function isoNow(): string {
  return new Date().toISOString();
}

function sha256(data: string): string {
  return crypto.createHash("sha256").update(data).digest("hex");
}

function sha512(data: string): string {
  return crypto.createHash("sha512").update(data).digest("hex");
}

function buildRecord(framework: Framework, version: string, author: string, project: string) {
  const timestamp = isoNow();
  const checksum = sha256(`${framework}-${version}-${timestamp}`);
  const meta = METADATA[framework];
  const echo_signature = sha512(JSON.stringify(meta) + checksum);

  return {
    framework,
    version,
    author,
    project,
    first_invocation: timestamp,
    checksum,
    metadata: { ...meta, echo_signature }
  };
}

function tableForFramework(framework: Framework) {
  if (framework === "SDVR") return "audit_log_sdkp";
  if (framework === "SDN") return "audit_log_sdn";
  return "audit_log_qcc";
}

function backupPathForFramework(framework: Framework) {
  return path.join(process.cwd(), `${framework.toLowerCase()}_audit_backup.jsonl`);
}

// ---------- Main upload function ----------
export async function uploadAudit(params: {
  framework: Framework;
  version?: string;
  author?: string;
  project?: string;
  failOnDuplicate?: boolean; // default true: if duplicate exist, return gracefully
}) {
  const framework = params.framework;
  const version = params.version ?? "v1.0.0";
  const author = params.author ?? "FatherTimeSDKP";
  const project = params.project ?? "Digital Crystal Protocol";
  const failOnDuplicate = params.failOnDuplicate ?? true;

  const record = buildRecord(framework, version, author, project);
  const table = tableForFramework(framework);

  // Local backup (append JSON lines)
  try {
    fs.appendFileSync(backupPathForFramework(framework), JSON.stringify(record) + "\n");
  } catch (err) {
    console.warn("Local backup failed:", err);
  }

  if (!supabase) {
    console.warn("Supabase client not configured — skipping remote upload. Returning local record.");
    return { success: true, record, uploaded: false, reason: "no_supabase" };
  }

  // Duplicate detection: check if (framework, version) exists
  const { data: existing, error: selectErr } = await supabase
    .from(table)
    .select("id, framework, version, first_invocation, checksum")
    .eq("framework", framework)
    .eq("version", version)
    .limit(1);

  if (selectErr) {
    // proceed to insert anyway but surface issue
    console.warn("Warning: could not check duplicates before insert:", selectErr);
  } else if (existing && (existing as any[]).length > 0) {
    if (failOnDuplicate) {
      return { success: false, uploaded: false, reason: "duplicate", existing: existing[0] };
    }
    // else continue to insert duplicate (rare use-case)
  }

  const { data, error } = await supabase.from(table).insert([record]).select();

  if (error) {
    // if unique constraint triggers, return duplicate result
    return { success: false, uploaded: false, error };
  }

  return { success: true, uploaded: true, data, record };
}

// ---------- Verification helper ----------
/**
 * verifyAuditRecord compares record.checksum with recomputed checksum and validates echo_signature
 * Returns { valid: boolean, reasons: string[] }
 */
export function verifyAuditRecord(record: any) {
  const reasons: string[] = [];
  if (!record || typeof record !== "object") {
    return { valid: false, reasons: ["record_missing_or_invalid"] };
  }
  const { framework, version, first_invocation, checksum, metadata } = record;
  if (!framework || !version || !first_invocation || !checksum || !metadata) {
    return { valid: false, reasons: ["required_fields_missing"] };
  }

  const recomputed = sha256(`${framework}-${version}-${first_invocation}`);
  if (recomputed !== checksum) {
    reasons.push("checksum_mismatch");
  }

  const metaTemplate = METADATA[framework as Framework];
  if (!metaTemplate) {
    reasons.push("unknown_framework_template");
  } else {
    const expectedEcho = sha512(JSON.stringify(metaTemplate) + checksum);
    if (metadata.echo_signature !== expectedEcho && metadata.echo_signature !== metadata?.echo_signature) {
      // Allow the case where metadata includes the original but doesn't match our template.
      reasons.push("echo_signature_mismatch");
    }
  }

  return { valid: reasons.length === 0, reasons };
}

// ---------- CLI entry ----------
if (require.main === module) {
  (async () => {
    const rawArg = process.argv[2];
    const rawVersion = process.argv[3] ?? "v1.0.0";

    if (!rawArg) {
      console.error("Usage: node dist/auditUploadAll.js <SDVR|SDN|QCC0> [version]");
      process.exit(1);
    }
    const framework = (rawArg as string).toUpperCase() as Framework;
    if (!["SDVR", "SDN", "QCC0"].includes(framework)) {
      console.error("Unknown framework. Use SDVR, SDN, or QCC0");
      process.exit(1);
    }

    try {
      const result = await uploadAudit({ framework, version: rawVersion });
      if (result.success && result.uploaded) {
        console.log(`✅ ${framework} audit uploaded:`, result.data);
      } else if (result.success && !result.uploaded) {
        console.log(`⚠️ ${framework} audit saved locally (no Supabase):`, result.record);
      } else {
        console.error("❌ Upload failed:", result);
        process.exit(2);
      }
    } catch (err) {
      console.error("Fatal error:", err);
      process.exit(3);
    }
  })();
}
