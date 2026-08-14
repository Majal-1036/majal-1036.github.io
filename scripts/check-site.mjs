import fs from "node:fs";
import path from "node:path";
import process from "node:process";

const root = path.resolve(import.meta.dirname, "..");
const pages = ["index.html", "research.html", "publications.html", "projects.html", "teaching.html"];
const errors = [];
let referenceCount = 0;

for (const page of pages) {
  const fullPath = path.join(root, page);
  const html = fs.readFileSync(fullPath, "utf8");

  if (!/<html\s+lang="en"/i.test(html)) errors.push(`${page}: missing lang="en"`);
  if (!/<meta\s+name="viewport"/i.test(html)) errors.push(`${page}: missing viewport metadata`);
  if (!/<meta\s+name="description"/i.test(html)) errors.push(`${page}: missing description metadata`);
  if (!/<title>[^<]+<\/title>/i.test(html)) errors.push(`${page}: missing page title`);

  const headings = [...html.matchAll(/<h1(?:\s[^>]*)?>/gi)];
  if (headings.length !== 1) errors.push(`${page}: expected one h1, found ${headings.length}`);

  const ids = [...html.matchAll(/\sid="([^"]+)"/gi)].map((match) => match[1]);
  const duplicateIds = ids.filter((id, index) => ids.indexOf(id) !== index);
  if (duplicateIds.length) errors.push(`${page}: duplicate ids ${[...new Set(duplicateIds)].join(", ")}`);

  for (const match of html.matchAll(/<img\b[^>]*>/gi)) {
    if (!/\salt="[^"]+"/i.test(match[0])) errors.push(`${page}: image missing useful alt text`);
  }

  for (const match of html.matchAll(/(?:href|src)="([^"]+)"/gi)) {
    const ref = match[1];
    if (/^(?:https?:|mailto:|tel:|#)/i.test(ref)) continue;
    const clean = ref.split(/[?#]/, 1)[0];
    if (!clean) continue;
    referenceCount += 1;
    const target = path.resolve(path.dirname(fullPath), clean);
    if (!fs.existsSync(target)) errors.push(`${page}: missing local target ${ref}`);
  }
}

const svgDirectories = [
  path.join(root, "assets", "images", "research"),
  path.join(root, "assets", "images", "projects"),
];

for (const directory of svgDirectories) {
  for (const file of fs.readdirSync(directory).filter((name) => name.endsWith(".svg"))) {
    const svg = fs.readFileSync(path.join(directory, file), "utf8");
    if (!svg.startsWith("<svg") || !svg.trimEnd().endsWith("</svg>")) {
      errors.push(`${file}: malformed SVG wrapper`);
    }
    if (!/<title\b/i.test(svg) || !/<desc\b/i.test(svg)) {
      errors.push(`${file}: missing accessible title or description`);
    }
  }
}

const cvPath = path.join(root, "assets", "files", "Arslan_Majal_CV.pdf");
if (!fs.existsSync(cvPath) || fs.statSync(cvPath).size < 1000) {
  errors.push("CV PDF is missing or empty");
}

if (errors.length) {
  console.error(`Site audit failed with ${errors.length} error(s):`);
  errors.forEach((error) => console.error(`- ${error}`));
  process.exit(1);
}

console.log(`Site audit passed: ${pages.length} pages, ${referenceCount} local references, and ${fs.statSync(cvPath).size} PDF bytes checked.`);
