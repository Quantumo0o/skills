/**
 * Code Review Intelligence MCP Server
 * Review, explain, and generate code using local AI
 * Main entry point for Apify Actor
 */

import { Actor } from "apify";
import { trackMCP } from "agnost";
import express from "express";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import { z } from "zod";

import { reviewCode, explainCode, generateCode } from "./handlers/code.js";

// PPE charge amounts per tool — MUST match pay_per_event.json exactly
const CHARGE_MAP = {
  review_code: 0.15,
  explain_code: 0.05,
  generate_code: 0.1,
};

async function main() {
  await Actor.init();

  const app = express();
  app.use(express.json());

  const mcpServer = new McpServer({
    name: "code-review-intelligence-mcp",
    version: "1.0.0",
  });

  // --- Register 3 MCP Tools ---

  mcpServer.tool(
    "review_code",
    "Review code for bugs, security issues, performance problems, or readability. Provides specific suggestions with line references.",
    {
      code: z.string().describe("The source code to review"),
      language: z
        .string()
        .optional()
        .describe("Programming language (default: auto-detect)"),
      focus: z
        .enum(["general", "security", "performance", "readability"])
        .optional()
        .describe("Review focus area (default: general)"),
    },
    async ({ code, language, focus }) => {
      const result = await reviewCode(
        code,
        language || "auto",
        focus || "general",
      );
      await chargeForTool("review_code");
      return {
        content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
      };
    },
  );

  mcpServer.tool(
    "explain_code",
    "Explain what code does. Adjustable detail level from brief summary to comprehensive analysis.",
    {
      code: z.string().describe("The source code to explain"),
      detailLevel: z
        .enum(["brief", "medium", "detailed"])
        .optional()
        .describe(
          "Detail level: brief (2-3 sentences), medium (purpose + key parts), detailed (full architecture analysis)",
        ),
    },
    async ({ code, detailLevel }) => {
      const result = await explainCode(code, detailLevel || "medium");
      await chargeForTool("explain_code");
      return {
        content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
      };
    },
  );

  mcpServer.tool(
    "generate_code",
    "Generate new code or refactor existing code based on instructions.",
    {
      instruction: z.string().describe("What to build or how to refactor"),
      existingCode: z
        .string()
        .optional()
        .describe("Existing code to refactor (omit for new code generation)"),
      language: z
        .string()
        .optional()
        .describe("Target programming language (default: python)"),
    },
    async ({ instruction, existingCode, language }) => {
      const result = await generateCode(
        instruction,
        existingCode || null,
        language || "python",
      );
      await chargeForTool("generate_code");
      return {
        content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
      };
    },
  );

  // --- MCP Transport ---

  trackMCP(mcpServer, "49897781-817a-421b-8ba2-5a42387a7458");

  app.post("/mcp", async (req, res) => {
    try {
      const transport = new StreamableHTTPServerTransport({
        sessionIdGenerator: undefined,
      });
      res.on("close", () => transport.close());
      await mcpServer.connect(transport);
      await transport.handleRequest(req, res, req.body);
    } catch (error) {
      console.error("MCP request error:", error);
      if (!res.headersSent) {
        res.status(500).json({
          jsonrpc: "2.0",
          error: {
            code: -32603,
            message: error.message || "Internal server error",
          },
          id: null,
        });
      }
    }
  });

  app.get("/health", (req, res) => {
    res.json({
      status: "ok",
      server: "code-review-intelligence-mcp",
      version: "1.0.0",
    });
  });

  const port = process.env.APIFY_CONTAINER_PORT || 3000;
  app.listen(port, "0.0.0.0", () => {
    console.log(
      `Code Review Intelligence MCP Server listening on http://0.0.0.0:${port}/mcp`,
    );
  });
}

async function chargeForTool(toolName) {
  const amount = CHARGE_MAP[toolName];
  if (amount) {
    try {
      await Actor.charge({ eventName: toolName, count: 1 });
      console.log(`Charged $${amount} for ${toolName}`);
    } catch (e) {
      console.error(`Charge failed for ${toolName}:`, e.message);
    }
  }
}

main().catch((err) => {
  console.error("Fatal error:", err);
  process.exit(1);
});
