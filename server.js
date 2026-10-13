/** Local development server with a file-backed booking database.
 * Production uses backend/google-apps-script/Code.gs instead.
 */
'use strict';
const http = require('http');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const ROOT = path.join(__dirname, 'dist');
const DATA_DIR = path.join(__dirname, '.local-data');
const DB_FILE = path.join(DATA_DIR, 'bookings.json');
const PORT = Number(process.env.PORT || 8000);
const HOST = process.env.HOST || '127.0.0.1';
const TYPES = {'.html':'text/html; charset=utf-8','.css':'text/css; charset=utf-8','.js':'text/javascript; charset=utf-8','.json':'application/json; charset=utf-8','.svg':'image/svg+xml','.webp':'image/webp','.png':'image/png','.jpg':'image/jpeg','.ico':'image/x-icon','.xml':'application/xml; charset=utf-8','.txt':'text/plain; charset=utf-8'};
const rate = new Map();

function readDb() { try { return JSON.parse(fs.readFileSync(DB_FILE, 'utf8')); } catch (_) { return {leads:[], bookings:[]}; } }
function writeDb(db) { fs.mkdirSync(DATA_DIR, {recursive:true}); const tmp=DB_FILE+'.tmp'; fs.writeFileSync(tmp, JSON.stringify(db,null,2)); fs.renameSync(tmp,DB_FILE); }
function json(res, status, body) { res.writeHead(status, {'Content-Type':'application/json; charset=utf-8','Cache-Control':'no-store','Access-Control-Allow-Origin':'*'}); res.end(JSON.stringify(body)); }
function body(req) { return new Promise((resolve,reject)=>{let b='';req.on('data',c=>{b+=c;if(b.length>50000){reject(new Error('too_large'));req.destroy();}});req.on('end',()=>{try{resolve(JSON.parse(b||'{}'));}catch(e){reject(e);}});}); }
function validLead(x) { return x && !x.honeypot && !x.website && typeof x.name==='string' && x.name.trim().length>=2 && /^\+?\d{7,16}$/.test(String(x.phone||'')) && (x.consent===true || x.consent==='on'); }
function slots(date) {
  if(!/^\d{4}-\d{2}-\d{2}$/.test(date)) return [];
  const horizon=new Date(Date.now()+14*86400000).toLocaleDateString('en-CA',{timeZone:'Asia/Dubai'}); if(date>horizon)return [];
  const noon=new Date(date+'T12:00:00+04:00'), dow=noon.getUTCDay(); if(![1,2,3,4,5,6].includes(dow))return [];
  const db=readDb(), now=Date.now()+3*3600000, result=[];
  for(let m=10*60;m+30<=19*60;m+=45){const hh=String(Math.floor(m/60)).padStart(2,'0'),mm=String(m%60).padStart(2,'0'),time=hh+':'+mm,start=new Date(date+'T'+time+':00+04:00').getTime();if(start<now)continue;const busy=db.bookings.some(b=>b.date===date&&b.time===time&&b.status!=='cancelled');if(!busy)result.push(time);}
  return result;
}
function siteHeaders(){try{const h={};let on=false;for(const line of fs.readFileSync(path.join(ROOT,'_headers'),'utf8').split(/\r?\n/)){if(/^\S/.test(line)){on=line.trim()==='/*';continue;}const m=on&&line.match(/^\s+([^:]+):\s*(.*)$/);if(m&&m[1]!=='Strict-Transport-Security')h[m[1]]=m[2];}return h;}catch(_){return {};}}
function clientKey(req) { return crypto.createHash('sha256').update((req.socket.remoteAddress||'')+'|'+(req.headers['user-agent']||'')).digest('hex').slice(0,20); }
function limited(req) { const k=clientKey(req), now=Date.now(), xs=(rate.get(k)||[]).filter(t=>now-t<60000); xs.push(now); rate.set(k,xs); return xs.length>12; }

async function api(req,res,url){
  if(req.method==='GET' && url.searchParams.get('action')==='slots')return json(res,200,{ok:true,date:url.searchParams.get('date'),slots:slots(url.searchParams.get('date')||'')});
  if(req.method==='GET' && url.searchParams.get('action')==='days'){const days={};for(let i=0;i<=14;i++){const d=new Date(Date.now()+i*86400000).toLocaleDateString('en-CA',{timeZone:'Asia/Dubai'});days[d]=slots(d);}return json(res,200,{ok:true,days});}
  if(limited(req))return json(res,429,{ok:false,error:'rate_limited'}); // only writes are rate-limited
  if(req.method!=='POST')return json(res,405,{ok:false,error:'method_not_allowed'});
  let x;try{x=await body(req);}catch(e){return json(res,400,{ok:false,error:'invalid_json'});} if(!validLead(x))return json(res,422,{ok:false,error:'invalid_lead'});
  const db=readDb(), now=new Date().toISOString(), id=String(x.lead_id||x.leadId||crypto.randomUUID());
  let lead=db.leads.find(l=>l.leadId===id); if(!lead){lead={...x,leadId:id,createdAt:now,status:'lead'};db.leads.push(lead);}else Object.assign(lead,x,{updatedAt:now});
  if(x.action==='lead'){writeDb(db);return json(res,200,{ok:true,lead_id:id,leadId:id});}
  if(x.action==='book'){
    if(!slots(String(x.date||'')).includes(String(x.time||'')))return json(res,200,{ok:false,code:'slot_taken',error:'slot_taken'});
    const bookingId=crypto.randomUUID();db.bookings.push({...x,leadId:id,bookingId,createdAt:now,status:'confirmed'});lead.status='booked';lead.bookingId=bookingId;writeDb(db);return json(res,200,{ok:true,leadId:id,bookingId});
  }
  return json(res,400,{ok:false,error:'unknown_action'});
}
function staticFile(req,res,url){
  let decoded;try{decoded=decodeURIComponent(url.pathname);}catch(e){res.writeHead(400);return res.end('Bad request');}
  let file=path.resolve(ROOT,'.'+decoded);if(file!==path.resolve(ROOT)&&!file.startsWith(path.resolve(ROOT)+path.sep)){res.writeHead(403);return res.end('Forbidden');}
  fs.stat(file,(err,st)=>{if(!err&&st.isDirectory())file=path.join(file,'index.html');fs.readFile(file,(e,data)=>{if(e){const fallback=path.join(ROOT,'404.html');return fs.readFile(fallback,(e2,d)=>{res.writeHead(404,{'Content-Type':'text/html; charset=utf-8'});res.end(e2?'Not found':d);});}res.writeHead(200,{...siteHeaders(),'Content-Type':TYPES[path.extname(file).toLowerCase()]||'application/octet-stream'});res.end(data);});});
}
http.createServer((req,res)=>{const url=new URL(req.url,'http://localhost');if(url.pathname==='/api')return api(req,res,url);staticFile(req,res,url);}).listen(PORT,HOST,()=>console.log(`A1esmat local site: http://${HOST}:${PORT}`));

