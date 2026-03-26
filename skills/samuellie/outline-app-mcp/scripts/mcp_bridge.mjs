import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";

async function run() {
  const action = process.argv[2];
  const toolName = process.argv[3];
  const toolArgsStr = process.argv[4];

  const apiKey = process.env.OUTLINE_API_KEY;
  const outlineUrl = process.env.OUTLINE_URL;

  if (!apiKey) {
    console.error("Error: OUTLINE_API_KEY environment variable is missing.");
    process.exit(1);
  }

  if (!outlineUrl) {
    console.error("Error: OUTLINE_URL environment variable is missing (e.g., https://your-workspace.getoutline.com/mcp).");
    process.exit(1);
  }

  const url = new URL(outlineUrl);

  // Custom fetch function to ensure headers are sent exactly how Outline likes them
  const customFetch = async (input, init) => {
    const headers = new Headers(init.headers || {});
    headers.set("Authorization", `Bearer ${apiKey}`);
    headers.set("Accept", "application/json, text/event-stream");
    headers.set("Content-Type", "application/json");
    
    return fetch(input, {
      ...init,
      headers
    });
  };

  const transport = new StreamableHTTPClientTransport(url, {
    fetch: customFetch
  });

  const client = new Client(
    { name: "openclaw-outline-bridge", version: "1.0.0" },
    { capabilities: {} }
  );

  await client.connect(transport);

  try {
    if (action === "list") {
      const tools = await client.listTools();
      console.log(JSON.stringify(tools, null, 2));
    } else if (action === "call") {
      if (!toolName) {
        console.error("Error: Tool name is required for 'call' action.");
        process.exit(1);
      }
      const args = toolArgsStr ? JSON.parse(toolArgsStr) : {};
      const result = await client.callTool({ name: toolName, arguments: args });
      console.log(JSON.stringify(result, null, 2));
    } else {
      console.error("Unknown action. Use 'list' or 'call <toolName> [argsJson]'.");
    }
  } catch (error) {
    console.error("MCP Request Failed:", error);
  } finally {
    if (transport.close) await transport.close();
  }
}

run().catch(console.error);
