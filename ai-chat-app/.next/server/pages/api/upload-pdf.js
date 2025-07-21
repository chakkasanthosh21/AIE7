const CHUNK_PUBLIC_PATH = "server/pages/api/upload-pdf.js";
const runtime = require("../../chunks/[turbopack]_runtime.js");
runtime.loadChunk("server/chunks/[externals]_formidable_2c4bfc0f._.js");
runtime.loadChunk("server/chunks/[root-of-the-server]__ab16907a._.js");
runtime.getOrInstantiateRuntimeModule("[project]/node_modules/next/dist/esm/build/templates/pages-api.js { INNER_PAGE => \"[project]/pages/api/upload-pdf.ts [api] (ecmascript)\" } [api] (ecmascript)", CHUNK_PUBLIC_PATH);
module.exports = runtime.getOrInstantiateRuntimeModule("[project]/node_modules/next/dist/esm/build/templates/pages-api.js { INNER_PAGE => \"[project]/pages/api/upload-pdf.ts [api] (ecmascript)\" } [api] (ecmascript)", CHUNK_PUBLIC_PATH).exports;
