import { definePluginEntry } from "@openclaw/plugin-sdk";
import { z } from "zod";

export default definePluginEntry((api) => {
  api.registerTool({
    name: "{{tool_name}}",
    description: "{{tool_description}}",
    inputSchema: z.object({}),
    async execute() {
      return {
        ok: true,
        content: [
          {
            type: "text",
            text: "{{tool_success_text}}"
          }
        ]
      };
    }
  });
});
