"use strict";
const fs = require("fs");
const path = require("path");
const root = path.resolve(__dirname, "..", "dist");

function files(dir, out = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) files(full, out); else out.push(full);
  }
  return out;
}

const all = files(root);
const html = all.filter(f => f.endsWith(".html"));
const missing = [], duplicateIds = [], pageErrors = [];
let bookingForms = 0;

function targetFor(url) {
  const clean = decodeURIComponent(url.split("#")[0].split("?")[0]);
  if (!clean || /[+'{}]/.test(clean) || /^(?:https?:|mailto:|tel:|javascript:|data:|\/\/)/i.test(clean)) return null;
  const relative = clean.startsWith("/") ? clean.slice(1) : clean;
  let target = path.join(root, relative);
  if (clean.endsWith("/")) target = path.join(target, "index.html");
  else if (!path.extname(target)) target = path.join(target, "index.html");
  return target;
}

for (const file of html) {
  const source = fs.readFileSync(file, "utf8");
  const rel = path.relative(root, file);
  const h1 = (source.match(/<h1(?:\s|>)/g) || []).length;
  const canonical = (source.match(/<link rel="canonical"/g) || []).length;
  if (h1 !== 1) pageErrors.push(`${rel}: expected one h1, found ${h1}`);
  if (canonical !== 1) pageErrors.push(`${rel}: expected one canonical, found ${canonical}`);
  if (!/<html lang="(?:en|ar)"/.test(source)) pageErrors.push(`${rel}: missing supported html lang`);
  bookingForms += (source.match(/<form class="booking-form"/g) || []).length;
  const ids = [...source.matchAll(/\sid="([^"]+)"/g)].map(m => m[1]);
  const repeated = [...new Set(ids.filter((id, i) => ids.indexOf(id) !== i))];
  if (repeated.length) duplicateIds.push(`${rel}: ${repeated.join(", ")}`);
  for (const match of source.matchAll(/(?:href|src)="([^"]+)"/g)) {
    const target = targetFor(match[1]);
    if (target && !fs.existsSync(target)) missing.push(`${rel} -> ${match[1]}`);
  }
}

console.log(JSON.stringify({ htmlFiles: html.length, bookingForms, missingLinks: missing.length, duplicateIdPages: duplicateIds.length, pageErrors: pageErrors.length }, null, 2));
if (missing.length) console.error("Missing:\n" + missing.join("\n"));
if (duplicateIds.length) console.error("Duplicate IDs:\n" + duplicateIds.join("\n"));
if (pageErrors.length) console.error("Page errors:\n" + pageErrors.join("\n"));
if (missing.length || duplicateIds.length || pageErrors.length || bookingForms < 40) process.exit(1);
