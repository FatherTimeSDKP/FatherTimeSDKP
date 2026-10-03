import { NextResponse } from "next/server";
import crypto from "crypto";

export async function POST(req: Request) {
  try {
    // 1. Read raw request text for exact HMAC signature calculation
    const rawBody = await req.text();
    const signature = req.headers.get("x-hub-signature-256");
    const githubEvent = req.headers.get("x-github-event");
    const secret = process.env.WEBHOOK_SECRET;

    // 2. Validate HMAC Signature from GitHub
    if (secret) {
      if (!signature) {
        return NextResponse.json({ error: "Missing signature header" }, { status: 401 });
      }

      const hmac = crypto.createHmac("sha256", secret);
      const expectedSignature = `sha256=${hmac.update(rawBody).digest("hex")}`;

      const signatureBuffer = Buffer.from(signature);
      const expectedBuffer = Buffer.from(expectedSignature);

      if (
        signatureBuffer.length !== expectedBuffer.length ||
        !crypto.timingSafeEqual(signatureBuffer, expectedBuffer)
      ) {
        return NextResponse.json({ error: "Invalid signature verification" }, { status: 401 });
      }
    }

    // 3. Parse JSON payload after successful verification
    const payload = JSON.parse(rawBody);

    // 4. Filter and handle Push events
    if (githubEvent === "push") {
      const commitHash = payload.after;
      const branch = payload.ref;
      const repository = payload.repository?.full_name;
      const pusher = payload.pusher?.name;

      console.log(`[GitHub Webhook] Push verified from ${pusher} in ${repository} (${branch}) - Commit: ${commitHash}`);

      // 5. Structure payload to pass to Kapnack Engine / Gibberlink
      const offChainSyncPayload = {
        event: "push",
        repository,
        branch,
        commitHash,
        pusher,
        canaryWatermark: 33114,
        timestamp: new Date().toISOString(),
      };

      // TODO: Replace with your actual external API fetch call if forwarding to a secondary server
      /*
      await fetch("https://your-offchain-engine.com/sync", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(offChainSyncPayload)
      });
      */

      return NextResponse.json({
        success: true,
        message: "GitHub push event verified and synced",
        data: offChainSyncPayload,
      });
    }

    // Respond OK for unhandled GitHub event types
    return NextResponse.json({ success: true, message: `Event ${githubEvent} received` }, { status: 200 });

  } catch (error: any) {
    console.error("Webhook processing error:", error.message);
    return NextResponse.json({ error: "Internal Server Error" }, { status: 500 });
  }
}
