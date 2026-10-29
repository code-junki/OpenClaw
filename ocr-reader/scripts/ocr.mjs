#!/usr/bin/env node
// Minimal OCR helper — reads image, calls llama-server multimodal API
import fs from "node:fs";

const url = process.env.LLAMA_SERVER_URL || "http://localhost:8080/v1/chat/completions";
const model = process.env.LLAMA_MODEL_PATH || "/models/unsloth-Qwen3.6-35B-A3B-GGUF/Qwen3.6-35B-A3B-UD-Q6_K.gguf";
const prompt = process.argv[2] || "What text is on this image? Transcribe everything.";
const image = process.argv[3];

const b64 = fs.readFileSync(image).toString("base64");
const resp = await fetch(url, {
  method: "POST",
  headers: { "Content-Type": "application/json", "Authorization": "Bearer ***" },
  body: JSON.stringify({
    model,
    messages: [{ role: "user", content: [
      { type: "text", text: prompt },
      { type: "image_url", image_url: { url: `data:image/jpeg;base64,${b64}` } }
    ]}],
    max_tokens: 4096, stream: false
  }),
  signal: AbortSignal.timeout(300000)
});

const text = (await resp.json()).choices[0].message.content;
console.log(text);
