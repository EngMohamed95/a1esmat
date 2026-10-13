'use strict';
const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..','dist');let errors=[],files=[];
function walk(d){for(const e of fs.readdirSync(d,{withFileTypes:true})){const p=path.join(d,e.name);if(e.isDirectory())walk(p);else if(e.name.endsWith('.html'))files.push(p);}}
function target(u){u=u.split(/[?#]/)[0];if(!u||!u.startsWith('/'))return null;const p=path.join(root,u.replace(/^\//,''));if(path.extname(p))return p;return path.join(p,'index.html');}
walk(root);
for(const file of files){const h=fs.readFileSync(file,'utf8'),rel=path.relative(root,file);
  if(!/<html[^>]+lang="(en|ar)"/.test(h))errors.push(rel+': missing language');
  if(!/<meta name="viewport"/.test(h))errors.push(rel+': missing viewport');
  if(!/<title>.+<\/title>/s.test(h))errors.push(rel+': missing title');
  if(/instagram\.com\/a1esmat(?:[\/"'])/.test(h))errors.push(rel+': old Instagram URL');
  if((h.match(/\/assets\/js\/site\.js/g)||[]).length!==1)errors.push(rel+': site.js count is not 1');
  const ids=[...h.matchAll(/\sid="([^"]+)"/g)].map(m=>m[1]),seen=new Set();for(const id of ids){if(seen.has(id)&&id!=='booking')errors.push(rel+': duplicate id '+id);seen.add(id);}
  for(const m of h.matchAll(/(?:href|src)="([^"]+)"/g)){const u=m[1];if(/^(https?:|mailto:|tel:|data:|#)/.test(u))continue;const p=target(u);if(p&&!fs.existsSync(p)&&!u.startsWith('/assets/'))errors.push(rel+': broken internal link '+u);}
}
const must=['index.html','ar/index.html','book/index.html','ar/book/index.html','villas-townhouses-dubai-abu-dhabi/index.html','ar/villas-townhouses-dubai-abu-dhabi/index.html','mortgage-calculator/index.html','ar/mortgage-calculator/index.html','cash-needed-calculator/index.html','ar/cash-needed-calculator/index.html','privacy/index.html','ar/privacy/index.html'];for(const f of must)if(!fs.existsSync(path.join(root,f)))errors.push('missing '+f);
if(errors.length){console.error(errors.join('\n'));process.exit(1);}console.log(`Validated ${files.length} HTML files: structure and internal links OK.`);
