import json, hashlib, os
from html import escape
import config as C
from data_images import IMAGES

CSS = r"""
:root{
  --ink:#0E1B20; --ink-2:#22363C; --ink-3:#304950; --paper:#F7F4EE; --paper-2:#EFEAE0; --card:#FFFFFF;
  --gold:#B08D57; --gold-2:#D6B77F; --gold-deep:#8A6A36; --gold-soft:#F3EBDC; --line:#E4DDD0; --line-dark:rgba(255,255,255,.14);
  --suit:#3F6B5B; --suit-soft:#E6EFEA; --risk:#9E3B2B; --risk-soft:#F6E7E2;
  --muted:#686E69; --on-dark:#E9E4DA; --on-dark-2:rgba(233,228,218,.72);
  --head:"Playfair Display", "El Messiri", Georgia, serif;
  --body:"IBM Plex Sans Arabic", system-ui, -apple-system, "Segoe UI", sans-serif;
  --wrap:1200px; --text:70ch; --radius:14px;
  --shadow:0 1px 2px rgba(14,27,32,.05), 0 12px 32px -12px rgba(14,27,32,.18);
  --shadow-lg:0 2px 4px rgba(14,27,32,.06), 0 30px 60px -20px rgba(14,27,32,.35);
  --ease:cubic-bezier(.2,.7,.2,1);
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--body);font-size:1.0625rem;line-height:1.75;-webkit-font-smoothing:antialiased}
[dir=rtl] body{line-height:1.9}
img{max-width:100%;height:auto;display:block}
a{color:var(--ink);text-decoration-color:var(--gold);text-underline-offset:.22em;text-decoration-thickness:1.5px;transition:color .2s}
a:hover{color:var(--gold-deep)}
:focus-visible{outline:3px solid var(--gold);outline-offset:3px;border-radius:3px}
::selection{background:var(--gold-2);color:var(--ink)}
.wrap{max-width:var(--wrap);margin:0 auto;padding:0 clamp(1rem,4vw,2rem)}
.skip{position:absolute;inset-inline-start:-999px;top:0;background:var(--ink);color:#fff;padding:.5rem 1rem;z-index:50}
.skip:focus{inset-inline-start:0}

/* header */
.site-head{position:sticky;top:0;z-index:20;background:rgba(14,27,32,.94);backdrop-filter:saturate(140%) blur(12px);-webkit-backdrop-filter:saturate(140%) blur(12px);border-bottom:1px solid var(--line-dark);color:var(--on-dark);transition:background .35s var(--ease),border-color .35s}
.home .site-head{position:fixed;inset-inline:0;background:transparent;border-color:transparent;backdrop-filter:none;-webkit-backdrop-filter:none}
.home .site-head.scrolled{background:rgba(14,27,32,.94);border-color:var(--line-dark);backdrop-filter:saturate(140%) blur(12px);-webkit-backdrop-filter:saturate(140%) blur(12px)}
.site-head .wrap{display:flex;align-items:center;gap:1.5rem;min-height:76px;flex-wrap:wrap}
.brand{display:flex;align-items:center;gap:.75rem;text-decoration:none;color:#fff}
.brand:hover{color:#fff}
.brand .mark{flex:none;height:42px;width:auto}
.foot-brand .brand .mark{height:56px}
.brand .bt{font-family:var(--head);font-weight:600;font-size:1.2rem;line-height:1.2}
.brand small{display:block;font-family:var(--body);font-weight:400;font-size:.78rem;color:var(--gold-2);letter-spacing:.02em}
.nav{display:flex;gap:1.4rem;flex-wrap:wrap;margin-inline-start:auto;align-items:center;font-size:.93rem}
.nav a{text-decoration:none;color:var(--on-dark-2);position:relative;padding:.3rem 0}
.nav a:not(.btn):not(.lang)::after{content:"";position:absolute;inset-inline:0;bottom:0;height:1px;background:var(--gold-2);transform:scaleX(0);transition:transform .3s var(--ease)}
.nav a:not(.btn):not(.lang):hover{color:#fff}
.nav a:not(.btn):not(.lang):hover::after{transform:scaleX(1)}
.nav .lang{font-weight:500;color:var(--on-dark);border:1px solid var(--line-dark);padding:.25rem .7rem;border-radius:999px}
.nav .lang:hover{border-color:var(--gold-2);color:#fff}
.nav .btn,.nav .btn:hover{color:var(--ink)}
/* desktop: logo and menu always on one row; spacing tightens as the screen narrows */
@media (min-width:981px){
  .site-head .wrap{flex-wrap:nowrap;gap:1.25rem}
  .nav{flex-wrap:nowrap;white-space:nowrap;gap:clamp(.7rem,1.3vw,1.4rem);font-size:clamp(.84rem,.95vw,.93rem)}
  .brand{flex:none}
}
@media (min-width:981px) and (max-width:1200px){
  .brand small{display:none}
  .nav .btn.small{padding:.5rem .85rem}
}

/* buttons */
.btn{display:inline-flex;align-items:center;gap:.5rem;font-family:var(--body);font-weight:600;font-size:.98rem;text-decoration:none;padding:.9rem 1.6rem;border-radius:999px;border:1.5px solid var(--gold);background:var(--gold);color:var(--ink);line-height:1.3;transition:background .25s,color .25s,border-color .25s,transform .25s var(--ease),box-shadow .25s}
.btn:hover{background:var(--gold-2);border-color:var(--gold-2);color:var(--ink);transform:translateY(-1px);box-shadow:0 10px 24px -10px rgba(176,141,87,.7)}
.btn.ghost{background:transparent;color:var(--ink);border-color:var(--ink)}
.btn.ghost:hover{background:var(--ink);color:#fff;border-color:var(--ink);box-shadow:none}
.dark .btn.ghost,.band .btn.ghost,.hero .btn.ghost,.phero .btn.ghost{color:#fff;border-color:rgba(255,255,255,.55)}
.dark .btn.ghost:hover,.band .btn.ghost:hover,.hero .btn.ghost:hover,.phero .btn.ghost:hover{background:#fff;color:var(--ink);border-color:#fff}
button.btn{font-size:1rem;cursor:pointer}
.btn.small{padding:.5rem 1.05rem;font-size:.88rem}
.actions{display:flex;flex-wrap:wrap;align-items:center;gap:.8rem;margin-top:1.75rem}

/* type */
h1,h2,h3{font-family:var(--head);line-height:1.15;letter-spacing:-.01em;font-weight:600}
[dir=rtl] h1,[dir=rtl] h2,[dir=rtl] h3{letter-spacing:0;line-height:1.45;font-weight:700}
h1{font-size:clamp(2.2rem,5.2vw,4rem);margin:.15em 0 .4em;max-width:20ch}
h2{font-size:clamp(1.6rem,3vw,2.4rem);margin:2.2em 0 .7em;max-width:28ch}
h3{font-size:1.2rem;margin:1.6em 0 .4em}
.wrap > h2::before,.split h2::before,.sec-h::before{content:"";display:block;width:48px;height:2px;background:var(--gold);margin-bottom:1rem}
p,li{max-width:var(--text)}
.lede{font-size:clamp(1.1rem,1.6vw,1.28rem);color:var(--ink-2);max-width:60ch;line-height:1.7}
.note{font-size:.9rem;color:var(--muted)}
.eyebrow{display:inline-block;font-size:.78rem;font-weight:600;letter-spacing:.2em;text-transform:uppercase;color:var(--gold-2);margin:0 0 .6rem}
[dir=rtl] .eyebrow{letter-spacing:.04em;font-size:.9rem}
.crumbs{font-size:.86rem;color:var(--muted);margin:1.6rem 0 0}
.crumbs a{color:inherit;text-decoration:none}
.crumbs a:hover{text-decoration:underline;color:inherit}

/* media helpers */
.cover{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.illus{position:absolute;inset-block-end:.8rem;inset-inline-end:.8rem;z-index:2;font-size:.76rem;font-weight:500;color:#fff;background:rgba(14,27,32,.62);backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px);padding:.2rem .6rem;border-radius:999px;letter-spacing:.02em}

/* home hero */
.hero{position:relative;min-height:min(100svh,920px);display:flex;align-items:flex-end;color:#fff;background:var(--ink);overflow:hidden;isolation:isolate}
.hero .cover{z-index:-2;transform:scale(1.06);animation:heroZoom 18s var(--ease) forwards}
.hero::before{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(180deg,rgba(14,27,32,.55) 0%,rgba(14,27,32,.25) 35%,rgba(14,27,32,.78) 78%,rgba(14,27,32,.96) 100%)}
@keyframes heroZoom{to{transform:scale(1)}}
.hero-grid{display:grid;grid-template-columns:1.15fr .85fr;gap:3.5rem;align-items:end;padding-block:9rem 4.5rem;width:100%}
.hero h1{color:#fff;max-width:17ch}
.hero .lede{color:var(--on-dark)}
.hero .note{color:var(--on-dark-2)}
.ledger{background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.16);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);border-radius:var(--radius);padding:.4rem 1.5rem}
.ledger div{display:grid;grid-template-columns:7.5rem 1fr;gap:1rem;padding:1rem 0;border-bottom:1px solid rgba(255,255,255,.12);align-items:baseline}
.ledger div:last-child{border-bottom:0}
.ledger b{font-family:var(--head);font-size:clamp(1.4rem,2.4vw,1.9rem);font-weight:600;color:var(--gold-2)}
.ledger span{color:var(--on-dark);font-size:.96rem}
.scroll-cue{position:absolute;inset-inline-start:50%;bottom:1.2rem;width:1px;height:48px;background:linear-gradient(var(--gold-2),transparent);opacity:.8}

/* inner page hero */
.phero{position:relative;color:#fff;background:var(--ink);overflow:hidden;isolation:isolate;min-height:clamp(340px,52vh,540px);display:flex;align-items:flex-end}
.phero::before{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(180deg,rgba(14,27,32,.35) 0%,rgba(14,27,32,.55) 45%,rgba(14,27,32,.93) 100%)}
.phero .cover{z-index:-2}
.phero .wrap{width:100%;padding-block:2.5rem 4rem}
.phero .illus{inset-block-end:auto;inset-block-start:1rem}
.phero h1{color:#fff;margin-top:.6rem}
.phero .lede{color:var(--on-dark)}
.phero .crumbs{color:var(--on-dark-2);margin:0}
.phero .actions{margin-top:1.25rem}
.phero .pending{color:var(--ink);max-width:60ch}
.lede-block{margin-top:3rem}
.lede-block > p:first-child{font-size:clamp(1.1rem,1.6vw,1.25rem);color:var(--ink-2)}

/* sections */
.band{position:relative;isolation:isolate;overflow:hidden;background:var(--ink);color:#fff;padding:clamp(4rem,9vw,7rem) 0;margin-top:5rem;text-align:center}
.band .cover{z-index:-2}
.band::before{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(180deg,rgba(14,27,32,.72),rgba(14,27,32,.88))}
.band h2{margin:0 auto;color:#fff;max-width:24ch}
.band h2::before{margin-inline:auto}
.band .actions{justify-content:center}
.band a{color:#fff}
.dark-sec{background:var(--ink);color:var(--on-dark);padding:clamp(3.5rem,7vw,6rem) 0;margin-top:5rem}
.dark-sec h2{color:#fff;margin-top:0}
.dark-sec a{color:#fff}

/* split image + text */
.split{display:grid;grid-template-columns:1fr 1fr;gap:clamp(2rem,5vw,4.5rem);align-items:center;margin:5rem 0 1rem}
.split h2{margin-top:0}
.split .frame{position:relative;aspect-ratio:4/5;border-radius:var(--radius);overflow:hidden;box-shadow:var(--shadow-lg)}
.split .frame::after{content:"";position:absolute;inset:14px;border:1px solid rgba(214,183,127,.55);border-radius:calc(var(--radius) - 6px);pointer-events:none}
.split.rev .frame{order:2}
@media (max-width:860px){.split{grid-template-columns:1fr}.split .frame{aspect-ratio:16/10}.split.rev .frame{order:0}}

.split .frame .cover.top{object-position:50% 20%}

/* client logos */
.clients{list-style:none;padding:0;margin:1.75rem 0 0;display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:.75rem}
.clients li{max-width:none;aspect-ratio:16/10;display:grid;place-items:center;padding:1rem 1.1rem;background:var(--card);border:1px solid var(--line);border-radius:10px;transition:border-color .3s,transform .3s var(--ease)}
.clients li.dark{background:var(--ink);border-color:var(--ink)}
.clients img{width:auto;height:auto;max-width:100%;max-height:58px;object-fit:contain;filter:grayscale(1);opacity:.78;transition:filter .4s,opacity .4s}
.clients li:hover{border-color:var(--gold);transform:translateY(-2px)}
.clients li:hover img{filter:none;opacity:1}
@media (hover:none){.clients img{filter:none;opacity:1}}

/* articles */
.narrow{max-width:860px}
.ahead{margin:1.2rem 0 2rem}
.ahead h1{font-size:clamp(1.9rem,4vw,3rem);max-width:none}
.byline{display:flex;align-items:center;gap:.8rem;margin-top:1.4rem}
.byline img{width:52px;height:52px;border-radius:50%;object-fit:cover;object-position:50% 20%;border:2px solid var(--gold)}
.byline b{display:block;font-family:var(--head)}
.byline span{font-size:.88rem;color:var(--muted)}
.acover{margin:0 0 2.5rem;border-radius:var(--radius);overflow:hidden;box-shadow:var(--shadow-lg)}
.acover img{width:100%}
.prose{font-size:1.1rem}
.prose h2{font-size:clamp(1.45rem,2.6vw,1.9rem);margin:2em 0 .6em}
.prose h2::before{content:"";display:block;width:40px;height:2px;background:var(--gold);margin-bottom:.8rem}
.prose h3{font-size:1.25rem;color:var(--gold-deep)}
.prose blockquote{margin:1.5rem 0;padding:1rem 1.4rem;background:var(--gold-soft);border-inline-start:3px solid var(--gold);border-radius:8px}
.prose li{margin:.3rem 0}

/* lead form */
.lead{background:var(--paper-2);padding:clamp(3.5rem,7vw,6rem) 0;scroll-margin-top:60px;border-top:1px solid var(--line)}
.lead-grid{display:grid;grid-template-columns:.9fr 1.1fr;gap:clamp(2rem,5vw,4.5rem);align-items:start}
.lead h2{margin-top:0}
.lead h2::before{content:"";display:block;width:48px;height:2px;background:var(--gold);margin-bottom:1rem}
.lead .eyebrow{color:#6E5428}
.lead-points{list-style:none;padding:0;margin:1.25rem 0}
.lead-points li{position:relative;padding-inline-start:1.7rem;margin:.5rem 0}
.lead-points li::before{content:"✓";position:absolute;inset-inline-start:0;color:var(--gold-deep);font-weight:700}
.lead-who{display:flex;align-items:center;gap:.9rem;margin-top:1.5rem}
.lead-who img{width:64px;height:64px;border-radius:50%;object-fit:cover;object-position:50% 20%;border:2px solid var(--gold)}
.lead-who b{display:block;font-family:var(--head);font-size:1.1rem}
.lead-who span{color:var(--muted);font-size:.95rem}
.lead-form{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);padding:clamp(1.3rem,3vw,2rem);box-shadow:var(--shadow-lg);display:grid;gap:1rem;position:relative;overflow:hidden}
.lead-form::before{content:"";position:absolute;inset-block-start:0;inset-inline:0;height:3px;background:linear-gradient(90deg,var(--gold),var(--gold-2))}
.frow{display:grid;grid-template-columns:1fr 1fr;gap:1rem}
.lead-form label{display:grid;gap:.35rem;font-weight:500;font-size:.93rem;color:var(--ink-2)}
.lead-form input,.lead-form select,.lead-form textarea{font:inherit;font-size:1rem;color:var(--ink);background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:.8rem .9rem;width:100%;min-height:48px;transition:border-color .2s,box-shadow .2s}
.lead-form textarea{resize:vertical;min-height:96px}
.lead-form input:focus,.lead-form select:focus,.lead-form textarea:focus{outline:none;border-color:var(--gold);box-shadow:0 0 0 3px rgba(176,141,87,.2)}
[dir=rtl] .lead-form input[dir=ltr]{text-align:right}
.wa-btn{justify-content:center;width:100%;background:#17744C;border-color:#17744C;color:#fff;font-size:1.05rem;padding:1rem}
.wa-btn:hover{background:#125C3C;border-color:#125C3C;color:#fff;box-shadow:0 10px 24px -10px rgba(23,116,76,.6)}
.lead-form .note{margin:-.4rem 0 0;text-align:center}
.lead-err{margin:0;color:var(--risk);font-weight:500}
.lead-ok{margin:0;background:var(--suit-soft);border-radius:8px;padding:.7rem .9rem;color:var(--suit);font-weight:500}
@media (max-width:860px){.lead-grid{grid-template-columns:1fr}}
@media (max-width:520px){.frow{grid-template-columns:1fr}}

/* steps */
.steps{counter-reset:s;list-style:none;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:1.25rem;margin:1.5rem 0}
.steps li{counter-increment:s;background:var(--card);border:1px solid var(--line);border-radius:var(--radius);padding:1.5rem 1.4rem;box-shadow:var(--shadow);position:relative;overflow:hidden}
.steps li::before{content:"0" counter(s);font-family:"Playfair Display",Georgia,serif;font-size:2.4rem;font-weight:500;color:var(--gold);display:block;line-height:1;margin-bottom:.8rem}
.steps li::after{content:"";position:absolute;inset-block-start:0;inset-inline:0;height:3px;background:linear-gradient(90deg,var(--gold),var(--gold-2))}
.steps b{display:block;font-family:var(--head);font-weight:600;font-size:1.12rem;margin-bottom:.3rem}

/* four questions */
.q4{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1.25rem}
.q4 div{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);padding:1.5rem 1.6rem;border-inline-start:3px solid var(--gold)}
.q4 h3{margin:0 0 .35rem;color:var(--gold-deep);font-size:1.35rem}
.q4 p{margin:0}
@media (max-width:700px){.q4{grid-template-columns:1fr}}

/* opportunity tiles */
.tiles{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:1rem;margin:1.5rem 0}
.tile{position:relative;isolation:isolate;overflow:hidden;border-radius:var(--radius);aspect-ratio:3/4;display:flex;flex-direction:column;justify-content:flex-end;padding:1.4rem;color:#fff;text-decoration:none;box-shadow:var(--shadow)}
.tile .cover{z-index:-2;transition:transform .9s var(--ease)}
.tile::before{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(180deg,rgba(14,27,32,0) 30%,rgba(14,27,32,.9) 100%);transition:background .4s}
.tile:hover{color:#fff}
.tile:hover .cover{transform:scale(1.07)}
.tile h3{margin:0 0 .3rem;font-size:1.35rem;color:#fff}
.tile p{margin:0;font-size:.9rem;color:var(--on-dark);line-height:1.55}
.tile .go{margin-top:.8rem;font-size:.85rem;font-weight:600;color:var(--gold-2)}
@media (max-width:980px){.tiles{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:520px){.tiles{grid-template-columns:1fr}.tile{aspect-ratio:16/11}}

/* project cards */
.plist{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:1.5rem;margin:1.75rem 0}
.pcard{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);display:flex;flex-direction:column;overflow:hidden;box-shadow:var(--shadow);transition:transform .4s var(--ease),box-shadow .4s var(--ease)}
.pcard:hover{transform:translateY(-4px);box-shadow:var(--shadow-lg)}
.pcard .ph{position:relative;display:block;aspect-ratio:3/2;overflow:hidden;background:var(--paper-2)}
.pcard .ph img{width:100%;height:100%;object-fit:cover;transition:transform .9s var(--ease)}
.pcard:hover .ph img{transform:scale(1.06)}
.pcard .pb{padding:1.3rem 1.4rem 1.4rem;display:flex;flex-direction:column;flex:1}
.pcard h3{margin:0 0 .2rem;font-size:1.3rem}
.pcard h3 a{text-decoration:none}
.pcard .meta{font-size:.85rem;color:var(--gold-deep);margin:0 0 .7rem;font-weight:500}
.pcard p{font-size:.95rem;margin:.2rem 0 .8rem}
.fit{font-size:.87rem;margin:.3rem 0;padding:.35rem .7rem;border-radius:6px;background:var(--suit-soft);border-inline-start:3px solid var(--suit)}
.fit.no{background:var(--risk-soft);border-color:var(--risk)}
.pcard .more{margin-top:auto;padding-top:.9rem;font-size:.92rem;font-weight:600;text-decoration:none;color:var(--gold-deep)}
.pcard .more::after{content:" →"}
[dir=rtl] .pcard .more::after{content:" ←"}

/* project page */
.facts{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:0;border:1px solid var(--line);border-radius:var(--radius);background:var(--card);margin:-2.5rem 0 1.5rem;overflow:hidden;box-shadow:var(--shadow-lg);position:relative;z-index:3}
.facts div{padding:1.1rem 1.25rem;border-inline-end:1px solid var(--line);border-bottom:1px solid var(--line)}
.facts dt{font-size:.78rem;color:var(--muted);text-transform:uppercase;letter-spacing:.08em}
[dir=rtl] .facts dt{text-transform:none;letter-spacing:0;font-size:.85rem}
.facts dd{margin:.15rem 0 0;font-family:var(--head);font-weight:600;font-size:1.05rem}
.fitgrid{display:grid;grid-template-columns:1fr 1fr;gap:1.25rem;margin:1.5rem 0}
.fitbox{padding:1.4rem 1.6rem;border-radius:var(--radius)}
.fitbox.yes{background:var(--suit-soft);border-inline-start:4px solid var(--suit)}
.fitbox.no{background:var(--risk-soft);border-inline-start:4px solid var(--risk)}
.fitbox h2{margin:0 0 .6rem;font-size:1.3rem}
.fitbox ul{margin:0;padding-inline-start:1.2rem}
@media (max-width:760px){.fitgrid{grid-template-columns:1fr}}
.risks{background:var(--risk-soft);border-radius:var(--radius);padding:1.5rem 1.7rem;margin:1.5rem 0}
.risks h2,.strengths h2{margin-top:0;font-size:1.4rem}
.strengths{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);padding:1.5rem 1.7rem;margin:1.5rem 0;box-shadow:var(--shadow)}
.pending{background:var(--gold-soft);border-radius:10px;padding:.9rem 1.1rem;font-size:.95rem;border-inline-start:3px solid var(--gold)}

/* faq */
.faq details{border-top:1px solid var(--line);padding:1.1rem 0}
.faq details:last-child{border-bottom:1px solid var(--line)}
.faq summary{cursor:pointer;font-family:var(--head);font-weight:600;font-size:1.12rem;list-style:none;display:flex;justify-content:space-between;gap:1rem;align-items:center}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";flex:none;width:30px;height:30px;border:1px solid var(--gold);border-radius:50%;display:grid;place-items:center;font-weight:400;color:var(--gold-deep);transition:transform .3s var(--ease),background .3s}
.faq details[open] summary::after{content:"−";background:var(--gold);color:var(--ink)}
.faq details p{margin:.7rem 0 0;color:var(--ink-2)}
.faq > h2::before{content:"";display:block;width:48px;height:2px;background:var(--gold);margin-bottom:1rem}

/* mini assessment + form */
.mini{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);padding:clamp(1.5rem,3vw,2.25rem);margin:2.5rem 0;box-shadow:var(--shadow);position:relative;overflow:hidden}
.mini::before{content:"";position:absolute;inset-block-start:0;inset-inline:0;height:3px;background:linear-gradient(90deg,var(--gold),var(--gold-2))}
.mini h2{margin-top:0}
fieldset{border:0;padding:0;margin:0 0 1.5rem}
legend{font-family:var(--head);font-weight:600;font-size:1.08rem;margin-bottom:.6rem}
.opts{display:flex;flex-wrap:wrap;gap:.55rem}
.opts label{border:1px solid var(--line);border-radius:999px;padding:.5rem 1rem;cursor:pointer;background:var(--paper);font-size:.94rem;transition:border-color .2s,background .2s}
.opts label:hover{border-color:var(--gold)}
.opts input{position:absolute;opacity:0;pointer-events:none}
.opts input:checked + span{font-weight:600}
.opts label:has(input:checked){border-color:var(--gold);background:var(--gold-soft)}
.opts label:has(input:focus-visible){outline:3px solid var(--gold)}
.result{margin-top:1rem;padding:1.5rem;border-radius:var(--radius);background:var(--suit-soft);display:none}
.result.show{display:block}
.result h2{margin-top:0}

.toc{font-size:.95rem;border-inline-start:2px solid var(--gold);padding-inline-start:1rem;margin:1.5rem 0}
.toc a{display:block;text-decoration:none;padding:.15rem 0}
.toc a:hover{text-decoration:underline}

table{border-collapse:collapse;width:100%;background:var(--card);font-size:.95rem}
.tscroll{overflow-x:auto;margin:1.25rem 0;border:1px solid var(--line);border-radius:var(--radius)}
th,td{padding:.8rem 1rem;text-align:start;border-bottom:1px solid var(--line);vertical-align:top}
th{font-family:var(--head);font-weight:600;background:var(--paper-2)}

.related{list-style:none;padding:0;display:flex;flex-wrap:wrap;gap:.6rem}
.related li a{display:inline-block;padding:.45rem 1rem;border:1px solid var(--line);border-radius:999px;text-decoration:none;background:var(--card);font-size:.93rem}
.related li a:hover{border-color:var(--gold);color:var(--gold-deep)}
.guide-list{list-style:none;padding:0;margin:2.5rem 0;display:grid;gap:.75rem}
.guide-list a{display:block;padding:1.1rem 1.3rem;background:var(--card);border:1px solid var(--line);border-radius:var(--radius);text-decoration:none;font-family:var(--head);font-size:1.15rem}
.guide-list a:hover{border-color:var(--gold)}

/* footer */
.site-foot{background:var(--ink);color:var(--on-dark-2);padding:4rem 0 2.5rem;font-size:.92rem;border-top:1px solid var(--line-dark)}
main > .wrap:last-child{padding-bottom:5rem}
.foot-brand{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:1.5rem;padding-bottom:2.5rem;margin-bottom:2.5rem;border-bottom:1px solid var(--line-dark)}
.foot-brand p{margin:0;max-width:44ch;color:var(--on-dark)}
.fcols{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:2rem}
.fcols h3{font-family:var(--body);font-size:.8rem;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:var(--gold-2);margin:0 0 .9rem}
[dir=rtl] .fcols h3{letter-spacing:0;font-size:.95rem}
.fcols a{display:block;color:var(--on-dark-2);text-decoration:none;padding:.3rem 0}
.fcols a:hover{color:#fff}
.legal{margin-top:3rem;padding-top:1.5rem;border-top:1px solid var(--line-dark);font-size:.84rem}
.legal p{max-width:none}

.wa-float{position:fixed;inset-inline-end:1rem;bottom:1rem;z-index:15;background:#17744C;color:#fff;border-radius:999px;padding:.8rem 1.25rem;text-decoration:none;font-weight:600;box-shadow:0 10px 30px -8px rgba(14,27,32,.45)}
.wa-float:hover{color:#fff;background:#125C3C}

/* reveal on scroll (only when JS is running) */
.js .reveal{opacity:1;transform:none}
.js .reveal.in{opacity:1;transform:none}

@media (max-width:980px){.hero-grid{grid-template-columns:1fr;gap:2rem;padding-block:8rem 3.5rem}.facts{grid-template-columns:repeat(2,minmax(0,1fr))}}
/* menu button (mobile) */
.burger{display:none;margin-inline-start:auto;width:46px;height:46px;border:1px solid var(--line-dark);border-radius:12px;background:rgba(255,255,255,.04);color:#fff;cursor:pointer;place-items:center;padding:0}
.burger span,.burger span::before,.burger span::after{display:block;width:20px;height:1.5px;background:currentColor;border-radius:2px;transition:transform .3s var(--ease),opacity .2s}
.burger span{position:relative}
.burger span::before,.burger span::after{content:"";position:absolute;inset-inline-start:0}
.burger span::before{top:-6px}.burger span::after{top:6px}
.site-head.open .burger span{background:transparent}
.site-head.open .burger span::before{transform:translateY(6px) rotate(45deg)}
.site-head.open .burger span::after{transform:translateY(-6px) rotate(-45deg)}

@media (max-width:980px){
  .js .burger{display:grid}
  .js .site-head .wrap{min-height:68px;gap:.8rem}
  .js .nav{display:none;width:100%;margin:0;flex-direction:column;align-items:stretch;gap:0;padding:.25rem 0 1.25rem;font-size:1.05rem;max-height:calc(100svh - 68px);overflow-y:auto}
  .js .site-head.open{background:rgba(14,27,32,.98);border-color:var(--line-dark);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px)}
  .js .site-head.open .nav{display:flex}
  .js .nav a:not(.btn):not(.lang){padding:.85rem .1rem;border-bottom:1px solid var(--line-dark);color:var(--on-dark)}
  .js .nav a:not(.btn):not(.lang)::after{display:none}
  .js .nav .btn.small{margin-top:1rem;justify-content:center;padding:.9rem;font-size:1rem}
  .js .nav .lang{align-self:center;margin-top:.8rem;padding:.5rem 1.4rem}
  html:not(.js) .nav{width:100%;margin-inline-start:0;flex-wrap:nowrap;overflow-x:auto;padding-bottom:.6rem;gap:1rem}
  html:not(.js) .nav a{white-space:nowrap}
}
@media (max-width:760px){
  .hero-grid{padding-block:6.5rem 2.75rem;gap:1.75rem}
  .hero h1{font-size:clamp(2rem,8.5vw,2.6rem)}
  .ledger{display:grid;grid-template-columns:1fr 1fr;padding:0;overflow:hidden}
  .ledger div{display:block;padding:.9rem 1rem;border-bottom:1px solid rgba(255,255,255,.12)}
  .ledger div:nth-child(odd){border-inline-end:1px solid rgba(255,255,255,.12)}
  .ledger div:nth-last-child(-n+2){border-bottom:0}
  .ledger b{display:block;font-size:1.3rem;margin-bottom:.15rem}
  .ledger span{font-size:.85rem;line-height:1.55;display:block}
  .facts{grid-template-columns:repeat(2,minmax(0,1fr));margin-top:-1.5rem}
  .facts div{padding:.85rem .9rem}
  .facts dd{font-size:.95rem}
  .plist{grid-template-columns:1fr}
  .scroll-cue{display:none}
  h2{margin-top:1.9em}
  .split{margin:3.5rem 0 .5rem}
  .band{margin-top:3.5rem}
  .clients{grid-template-columns:repeat(3,minmax(0,1fr));gap:.5rem}
  .clients li{aspect-ratio:4/3;padding:.6rem;border-radius:8px}
  .clients img{max-height:42px}
  .clients li:last-child:nth-child(3n+1){grid-column:2}
  .fcols{grid-template-columns:1fr 1fr;gap:1.5rem 1.25rem}
  .fcols > div:nth-child(2){grid-row:span 2}
  .fcols a{padding:.55rem 0;font-size:.95rem;line-height:1.4}
  .foot-brand{padding-bottom:2rem;margin-bottom:2rem}
  .faq summary{font-size:1.05rem;min-height:44px}
  .opts label{padding:.65rem 1.05rem}
}
@media (max-width:520px){
  .actions .btn{flex:1 1 auto;justify-content:center;text-align:center}
  .phero{min-height:300px}
  .phero .wrap{padding-block:2rem 3.25rem}
  .mini{padding:1.35rem}
  .tile{aspect-ratio:16/10}
}
@media (prefers-reduced-motion:reduce){*,*::before,*::after{transition:none!important;animation:none!important}html{scroll-behavior:auto}.js .reveal{opacity:1;transform:none}.hero .cover{transform:none}}
@media print{.site-head,.site-foot,.wa-float,.band{display:none}.phero,.hero{color:var(--ink);background:none;min-height:0}.phero .cover,.hero .cover{display:none}}

/* conversion sections and booking flow */
.benefit-grid,.audience-grid,.tier-grid{display:grid;gap:1rem;margin:1.5rem 0}
.benefit-grid{grid-template-columns:repeat(3,minmax(0,1fr))}
.audience-grid{grid-template-columns:repeat(3,minmax(0,1fr))}
.tier-grid{grid-template-columns:repeat(4,minmax(0,1fr))}
.benefit-card,.audience-card,.tier-card{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);padding:1.35rem;box-shadow:var(--shadow)}
.benefit-card h3,.audience-card h3,.tier-card h3{margin:.15rem 0 .45rem}
.benefit-card .num{color:var(--gold-deep);font-family:var(--head);font-size:1.35rem}
.market-line{font-weight:600;border-inline-start:3px solid var(--gold);padding:.75rem 1rem;background:var(--gold-soft)}
.developer-strip{display:flex;flex-wrap:wrap;gap:.65rem;list-style:none;padding:0;margin:1.25rem 0}
.developer-strip li{border:1px solid var(--line);border-radius:999px;background:var(--card);padding:.7rem 1.1rem;font-family:var(--head);font-weight:600}
.booking-card{background:var(--card);color:var(--ink);border:1px solid var(--line);border-radius:var(--radius);padding:clamp(1.1rem,2.5vw,1.8rem);box-shadow:var(--shadow-lg)}
.hero .booking-card{background:rgba(255,255,255,.97)}
.booking-form{display:block;position:relative}
.booking-progress{display:flex;gap:.45rem;margin:0 0 1rem}
.booking-progress span{height:4px;flex:1;background:var(--line);border-radius:9px}
.booking-progress span.on{background:var(--gold)}
.booking-step[hidden]{display:none}
.booking-step h2{font-size:1.2rem;margin:.1rem 0 1rem;max-width:none}
.booking-step h2::before{display:none}
.booking-form label,.field-label{display:grid;gap:.35rem;font-size:.9rem;font-weight:600;color:var(--ink-2);margin-bottom:.8rem}
.booking-form input,.booking-form select{font:inherit;font-size:1rem;color:var(--ink);background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:.75rem .8rem;width:100%;min-height:48px}
.booking-form input:focus,.booking-form select:focus{outline:none;border-color:var(--gold);box-shadow:0 0 0 3px rgba(176,141,87,.2)}
.phone-input{display:grid;grid-template-columns:8.25rem 1fr;gap:.5rem;direction:ltr}
.booking-form .phone-input select{direction:ltr;text-align:left;padding-left:2.65rem;background-repeat:no-repeat;background-position:.75rem 50%;background-size:1.45rem auto}
.choice-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.55rem;margin-bottom:.9rem}
.choice-grid label{display:flex;align-items:center;gap:.5rem;margin:0;border:1px solid var(--line);border-radius:10px;padding:.7rem;background:var(--paper);cursor:pointer;min-height:48px}
.choice-grid input{width:auto;min-height:auto;accent-color:var(--gold-deep)}
.consent-row{display:flex!important;grid-template-columns:none!important;align-items:flex-start;gap:.65rem!important;font-weight:400!important}
.consent-row input{width:auto;min-height:auto;margin-top:.35rem}
/* honeypot: display:none so browsers and autofill extensions never fill it; only bots posting raw HTML forms do */
.hp-field{display:none!important}
.booking-error{color:var(--risk);background:var(--risk-soft);border-radius:8px;padding:.65rem .8rem;margin:.6rem 0}
.booking-actions{display:flex;gap:.65rem;flex-wrap:wrap;margin-top:1rem}
.booking-actions .btn{justify-content:center}
/* the card never grows wider than its column, whatever the chip rows contain */
.hero-grid > *,.booking-card,.booking-form,.booking-step{min-width:0}
/* days: one row that scrolls inside the card; times: a grid that wraps, so every time is visible */
.day-chips{display:flex;gap:.5rem;overflow-x:auto;overscroll-behavior-x:contain;scroll-snap-type:x proximity;padding:.2rem .1rem .7rem;margin-bottom:.4rem;scrollbar-width:thin;-webkit-mask-image:linear-gradient(to right,#000 88%,transparent);mask-image:linear-gradient(to right,#000 88%,transparent)}
[dir=rtl] .day-chips{-webkit-mask-image:linear-gradient(to left,#000 88%,transparent);mask-image:linear-gradient(to left,#000 88%,transparent)}
.slot-chips{display:grid;grid-template-columns:repeat(auto-fill,minmax(5.6rem,1fr));gap:.5rem;padding:.2rem 0 .9rem}
.day-chip,.slot-chip{font:inherit;font-size:.95rem;white-space:nowrap;border:1px solid var(--line);border-radius:10px;background:var(--paper);color:var(--ink);padding:.55rem .75rem;min-height:48px;cursor:pointer;transition:border-color .2s,background .2s}
.day-chip{flex:none;scroll-snap-align:start}
.slot-chip{display:flex;flex-direction:column;align-items:center;justify-content:center;line-height:1.2;padding:.45rem .3rem}
.slot-chip small{font-size:.74rem;color:var(--muted);margin-top:.15rem}
.day-chip:hover:not(:disabled),.slot-chip:hover{border-color:var(--gold)}
.day-chip[aria-pressed=true],.slot-chip[aria-pressed=true]{background:var(--ink);border-color:var(--ink);color:#fff}
.slot-chip[aria-pressed=true] small{color:var(--on-dark-2)}
.day-chip:disabled,.slot-chip:disabled{opacity:.42;cursor:not-allowed}
.time-note{font-size:.88rem;color:var(--muted)}
.booking-step .choice-grid{grid-template-columns:repeat(auto-fit,minmax(10.5rem,1fr))}
/* ghost buttons sit on the light card, not on the dark hero */
.hero .booking-card .btn.ghost,.booking-card .btn.ghost{color:var(--ink);border-color:var(--line);background:transparent}
.hero .booking-card .btn.ghost:hover,.booking-card .btn.ghost:hover{background:var(--ink);border-color:var(--ink);color:#fff}
.booking-confirm{background:var(--suit-soft);border-radius:10px;padding:1.1rem}
.booking-confirm h2{margin-top:0}
.booking-confirm .confirmation-copy{font-weight:600;color:var(--suit)}
.booking-confirm .booking-actions .btn{flex:1 1 12rem}
.lang-offer{position:fixed;inset-inline:1rem;top:84px;z-index:24;max-width:420px;margin-inline:auto;background:#fff;border:1px solid var(--line);border-radius:12px;padding:.85rem 1rem;box-shadow:var(--shadow-lg);display:flex;align-items:center;gap:.8rem}
.lang-offer p{margin:0;flex:1;font-size:.9rem;line-height:1.45}
.lang-offer button{border:0;background:transparent;font-size:1.3rem;cursor:pointer;min-width:44px;min-height:44px}
.cookie-banner{position:fixed;inset-inline:1rem;bottom:1rem;z-index:40;max-width:680px;margin-inline:auto;background:var(--ink);color:var(--on-dark);border:1px solid var(--line-dark);border-radius:14px;padding:1rem 1.15rem;box-shadow:var(--shadow-lg)}
.cookie-banner p{margin:0 0 .75rem;font-size:.9rem;line-height:1.55}
.cookie-banner a{color:var(--gold-2)}
.cookie-actions{display:flex;gap:.6rem;flex-wrap:wrap}
.cookie-actions button{min-height:44px}
.mobile-bookbar{display:none}
.calc-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem}
.calculator{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);padding:clamp(1.25rem,3vw,2rem);box-shadow:var(--shadow);margin:2rem 0}
.calculator label{display:grid;gap:.35rem;font-weight:600;font-size:.92rem}
.calculator > .btn{margin-top:1.25rem}
.calculator input,.calculator select{font:inherit;min-height:48px;border:1px solid var(--line);border-radius:10px;background:var(--paper);padding:.7rem .8rem;width:100%}
.calc-results{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.75rem;margin-top:1.25rem}
.calc-results div{background:var(--gold-soft);border-radius:10px;padding:1rem}
.calc-results span{display:block;font-size:.82rem;color:var(--muted)}
.calc-results strong{font-family:var(--head);font-size:1.35rem}
/* tap targets: at least 44px on touch screens (brief 4.7) */
@media (max-width:760px){
  .fcols a{display:flex;align-items:center;min-height:44px;padding:0}
  .legal a,.related li a,.crumbs a,.pcard .more,.tier-card .more,.nav .lang,.consent-row a,.faq details a{display:inline-flex;align-items:center;min-height:44px}
  .consent-row input{flex:none;width:24px;height:24px}
  .brand{min-height:44px}
  .pcard h3 a{display:inline-block;padding-block:.65rem}
  .lang-offer .btn{min-height:44px}
}
@media(max-width:980px){.benefit-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.tier-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:700px){.benefit-grid,.audience-grid,.tier-grid,.calc-grid,.calc-results{grid-template-columns:1fr}.choice-grid{grid-template-columns:1fr}.wa-float{display:none}.mobile-bookbar{position:fixed;display:flex;inset-inline:0;bottom:0;z-index:30;background:var(--ink);border-top:1px solid var(--line-dark);padding:.65rem max(.75rem,env(safe-area-inset-right)) calc(.65rem + env(safe-area-inset-bottom)) max(.75rem,env(safe-area-inset-left));gap:.6rem}.mobile-bookbar .btn{flex:1;justify-content:center;min-height:48px}.mobile-bookbar .wa-mini{flex:0 0 52px;background:#17744C;border-color:#17744C;color:#fff;padding:.7rem}.site-foot{padding-bottom:7rem}}
"""

# Country codes for the phone field. Flags are small inline SVGs because flag emoji
# render as plain letters on Windows.
def _teeth(color_bg, color_side, width, teeth):
    h = 20 / (teeth * 2)
    d = f"M0 0H{width}" + "".join(f"L{width + 3} {h * (2 * i + 1):.2f}L{width} {h * (2 * i + 2):.2f}" for i in range(teeth)) + "H0Z"
    return f'<rect width="30" height="20" fill="{color_bg}"/><path d="{d}" fill="{color_side}"/>'

FLAGS = {
    "ae": '<rect width="30" height="20" fill="#00732f"/><rect y="6.67" width="30" height="6.67" fill="#fff"/><rect y="13.33" width="30" height="6.67" fill="#000"/><rect width="8" height="20" fill="#f00"/>',
    "sa": '<rect width="30" height="20" fill="#006c35"/><rect x="7" y="6.5" width="16" height="2.4" rx="1.2" fill="#fff"/><rect x="8" y="12" width="14" height="1.3" fill="#fff"/>',
    "eg": '<rect width="30" height="20" fill="#000"/><rect width="30" height="13.33" fill="#fff"/><rect width="30" height="6.67" fill="#ce1126"/><circle cx="15" cy="10" r="2.2" fill="#c09300"/>',
    "qa": _teeth("#8a1538", "#fff", 8, 9),
    "kw": '<rect width="30" height="20" fill="#ce1126"/><rect width="30" height="13.33" fill="#fff"/><rect width="30" height="6.67" fill="#007a3d"/><path d="M0 0L8 6.67V13.33L0 20Z" fill="#000"/>',
    "bh": _teeth("#ce1126", "#fff", 7, 5),
    "om": '<rect width="30" height="20" fill="#db161b"/><rect x="8" width="22" height="6.67" fill="#fff"/><rect x="8" y="13.33" width="22" height="6.67" fill="#008000"/>',
    "in": '<rect width="30" height="20" fill="#138808"/><rect width="30" height="13.33" fill="#fff"/><rect width="30" height="6.67" fill="#f93"/><circle cx="15" cy="10" r="2.3" fill="none" stroke="#000080" stroke-width=".7"/>',
    "gb": '<rect width="30" height="20" fill="#012169"/><path d="M0 0L30 20M30 0L0 20" stroke="#fff" stroke-width="4"/><path d="M0 0L30 20M30 0L0 20" stroke="#c8102e" stroke-width="1.5"/><path d="M15 0V20M0 10H30" stroke="#fff" stroke-width="6"/><path d="M15 0V20M0 10H30" stroke="#c8102e" stroke-width="3.5"/>',
    "us": '<rect width="30" height="20" fill="#b22234"/>' + "".join(f'<rect y="{20 / 13 * i:.2f}" width="30" height="{20 / 13:.2f}" fill="#fff"/>' for i in range(1, 13, 2)) + '<rect width="12" height="10.77" fill="#3c3b6e"/>',
}
COUNTRIES = [("ae", "+971", "UAE", "الإمارات"), ("sa", "+966", "KSA", "السعودية"), ("eg", "+20", "Egypt", "مصر"),
             ("qa", "+974", "Qatar", "قطر"), ("kw", "+965", "Kuwait", "الكويت"), ("bh", "+973", "Bahrain", "البحرين"),
             ("om", "+968", "Oman", "عُمان"), ("in", "+91", "India", "الهند"), ("gb", "+44", "UK", "بريطانيا"), ("us", "+1", "US / Canada", "أمريكا / كندا")]

def _flag_url(svg):
    from urllib.parse import quote
    return "url(\"data:image/svg+xml," + quote('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 30 20">' + svg + "</svg>", safe="") + "\")"

CSS += "".join(f'.phone-input select[data-flag={k}]{{background-image:{_flag_url(v)}}}' for k, v in FLAGS.items())

CSS_V = None  # set below, after CSS is defined

def img(key, lang, cls="", eager=False, sizes="100vw"):
    """Responsive <img> for an image in data_images.IMAGES."""
    im = IMAGES[key]
    a = escape(im[lang])
    ws = im.get("w", (600, 900, 1920))
    base = ws[1] if len(ws) > 2 else ws[0]
    h = round(base * im.get("h", 2 / 3))
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    c = f' class="{cls}"' if cls else ""
    srcset = ", ".join(f"/assets/img/{key}-{w}.webp {w}w" for w in ws)
    return (f'<img{c} src="/assets/img/{key}-{base}.webp" srcset="{srcset}" '
            f'sizes="{sizes}" width="{base}" height="{h}" alt="{a}" {load} decoding="async">')

def img_url(key):
    return f"{C.DOMAIN}/assets/img/{key}-{IMAGES[key].get('w', (600, 900, 1920))[-1]}.webp"

def illus(lang):
    return f'<span class="illus">{"صورة توضيحية" if lang == "ar" else "Illustrative image"}</span>'

def phero(key, lang, inner, badge=False):
    """Full-width image header for inner pages."""
    return (f'<section class="phero">{img(key, lang, "cover", eager=True)}{illus(lang) if badge else ""}'
            f'<div class="wrap">{inner}</div></section>')

def wa_link(text=""):
    if not C.WHATSAPP:
        return None
    from urllib.parse import quote
    return f"https://wa.me/{C.WHATSAPP}" + (f"?text={quote(text)}" if text else "")

GUIDES_LIVE = False  # set by build.py

NAV = {
    "en": [("/#services", "Services"), ("/#developers", "Developers"), ("/projects/", "Projects"),
           ("/#how-it-works", "How it works"), ("/#contact", "Contact"), ("/blog/", "Insights · Marketing")],
    "ar": [("/ar/#services", "الخدمات"), ("/ar/#developers", "المطورون"), ("/ar/projects/", "المشاريع"),
           ("/ar/#how-it-works", "كيف نعمل"), ("/ar/#contact", "تواصل"), ("/blog/", "رؤى · تسويق")],
}

FOOT = {
    "en": {
        "cols": [
            ("Opportunities", [("/off-plan-properties-dubai/", "Off plan properties Dubai"), ("/off-plan-villas-dubai/", "Off plan villas Dubai"),
                               ("/off-plan-townhouses-dubai/", "Off plan townhouses Dubai"), ("/villa-projects-dubai/", "Villa projects Dubai"),
                               ("/new-off-plan-projects-dubai/", "New off plan projects Dubai")]),
            ("Projects", [("/projects/the-valley-emaar/", "The Valley by Emaar"), ("/projects/damac-lagoons/", "DAMAC Lagoons"),
                          ("/projects/tilal-al-ghaf/", "Tilal Al Ghaf"), ("/projects/elysian-mansions-tilal-al-ghaf/", "Elysian Mansions"),
                          ("/projects/palm-jebel-ali-villas/", "Palm Jebel Ali villas"), ("/projects/the-oasis-emaar/", "The Oasis by Emaar"),
                          ("/projects/nad-al-sheba-gardens/", "Nad Al Sheba Gardens"), ("/projects/sobha-hartland-villas/", "Sobha Hartland villas")]),
            ("Start here", [("/investor-assessment/", "Investor assessment"), ("/book/", "Book a consultation"), ("/mortgage-calculator/", "Monthly payment calculator"), ("/cash-needed-calculator/", "Cash needed calculator"), ("/blog/", "Insights · Marketing"), ("/privacy/", "Privacy"), ("/disclaimer/", "Disclaimer"), ("/ar/", "العربية")]),
        ],
        "legal": "Ahmed Esmat provides real estate and business advisory. Nothing on this site is financial advice or a guarantee of returns. Project information is checked on the date shown on each page and may change; confirm prices, payment plans and handover dates with the developer before any commitment. Not affiliated with any developer unless stated.",
    },
    "ar": {
        "cols": [
            ("الفرص", [("/ar/villas-for-sale-dubai/", "فلل للبيع في دبي"), ("/ar/townhouses-for-sale-dubai/", "تاون هاوس للبيع في دبي"),
                       ("/ar/villas-installments-dubai/", "فلل للبيع في دبي بالتقسيط"), ("/ar/new-projects-dubai/", "مشاريع عقارية جديدة في دبي"),
                       ("/ar/buy-villa-dubai/", "تملك فيلا في دبي")]),
            ("المشاريع", [("/ar/projects/the-valley-emaar/", "The Valley من إعمار"), ("/ar/projects/damac-lagoons/", "DAMAC Lagoons داماك لاجونز"),
                          ("/ar/projects/tilal-al-ghaf/", "تلال الغاف Tilal Al Ghaf"), ("/ar/projects/elysian-mansions-tilal-al-ghaf/", "Elysian Mansions"),
                          ("/ar/projects/palm-jebel-ali-villas/", "فلل نخلة جبل علي"), ("/ar/projects/the-oasis-emaar/", "The Oasis من إعمار"),
                          ("/ar/projects/nad-al-sheba-gardens/", "حدائق ند الشبا"), ("/ar/projects/sobha-hartland-villas/", "فلل شوبا هارتلاند")]),
            ("ابدأ من هنا", [("/ar/investor-assessment/", "التقييم الاستثماري"), ("/ar/book/", "احجز استشارة"), ("/ar/mortgage-calculator/", "حاسبة القسط الشهري"), ("/ar/cash-needed-calculator/", "حاسبة الكاش المطلوب"), ("/blog/", "رؤى · تسويق"), ("/ar/privacy/", "الخصوصية"), ("/ar/disclaimer/", "إخلاء المسؤولية"), ("/", "English")]),
        ],
        "legal": "يقدم أحمد عصمت استشارات في العقار والأعمال. لا يُعد أي محتوى في هذا الموقع نصيحة مالية أو ضماناً لعائد. معلومات المشاريع مراجعة بالتاريخ المذكور في كل صفحة وقد تتغير، لذا تأكد من الأسعار وخطط الدفع ومواعيد التسليم مع المطور قبل أي التزام. الموقع غير مرتبط بأي مطور ما لم يُذكر خلاف ذلك.",
    },
}

def script_json(obj):
    """JSON safe to place inside a <script> element."""
    return json.dumps(obj, ensure_ascii=False).replace("</", "<\\/")

def ld(obj):
    return '<script type="application/ld+json">' + script_json(obj) + "</script>"

def person_schema():
    same_as = [x for x in (C.INSTAGRAM, getattr(C, "LINKEDIN", "")) if x]
    return {
        "@context": "https://schema.org", "@type": "Person", "@id": C.DOMAIN + "/#ahmed",
        "name": "Ahmed Esmat", "alternateName": "أحمد عصمت", "url": C.DOMAIN + "/",
        "image": img_url("ahmed-esmat-dubai-advisor"),
        "jobTitle": "Real estate and business advisor", "areaServed": ["Dubai", "Abu Dhabi"],
        "sameAs": same_as,
        "knowsAbout": ["Dubai real estate", "Off-plan property", "Villas and townhouses", "Performance marketing", "Business growth"],
    }

def service_schema():
    return {"@context": "https://schema.org", "@type": ["ProfessionalService", "RealEstateAgent"], "@id": C.DOMAIN + "/#service",
            "name": "Ahmed Esmat Real Estate & Business Advisory", "url": C.DOMAIN + "/",
            "image": img_url("ahmed-esmat-dubai-advisor"), "areaServed": ["Dubai", "Abu Dhabi"],
            "founder": {"@id": C.DOMAIN + "/#ahmed"},
            "sameAs": [x for x in (C.INSTAGRAM, getattr(C, "LINKEDIN", "")) if x],
            **({"telephone": "+" + C.WHATSAPP} if C.WHATSAPP else {}), **({"email": C.EMAIL} if C.EMAIL else {}),
            **({"legalName": C.LEGAL_ENTITY_EN} if getattr(C, "LEGAL_ENTITY_EN", "") else {}),
            **({"address": {"@type": "PostalAddress", "streetAddress": C.ADDRESS_STREET, "addressLocality": C.ADDRESS_LOCALITY,
                            "addressCountry": C.ADDRESS_COUNTRY}} if getattr(C, "ADDRESS_STREET", "") else {})}

def website_schema():
    return {"@context": "https://schema.org", "@type": "WebSite", "@id": C.DOMAIN + "/#site",
            "url": C.DOMAIN + "/", "name": "Ahmed Esmat", "alternateName": ["A1esmat", "أحمد عصمت"], "inLanguage": ["en", "ar"],
            "publisher": {"@id": C.DOMAIN + "/#ahmed"}, "image": C.DOMAIN + "/assets/img/a1esmat-logo.png"}

def crumbs_schema(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": C.DOMAIN + u} for i, (u, n) in enumerate(items)]}

def faq_schema(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": f[0], "acceptedAnswer": {"@type": "Answer", "text": f[1]}} for f in faqs]}

def faq_html(faqs, title):
    """faqs: (question, answer) or (question, answer, link_url, link_text)."""
    out = [f'<section class="faq" id="faq"><h2>{title}</h2>']
    for f in faqs:
        q, a = f[0], f[1]
        link = f' <a href="{f[2]}">{escape(f[3])}</a>' if len(f) > 3 else ""
        out.append(f"<details><summary>{escape(q)}</summary><p>{escape(a)}{link}</p></details>")
    out.append("</section>")
    return "\n".join(out)

def crumbs_html(items, lang):
    sep = " / "
    parts = []
    for i, (u, n) in enumerate(items):
        if i == len(items) - 1:
            parts.append(f'<span aria-current="page">{escape(n)}</span>')
        else:
            parts.append(f'<a href="{u}">{escape(n)}</a>')
    label = "مسار الصفحة" if lang == "ar" else "Breadcrumb"
    return f'<nav class="crumbs" aria-label="{label}">{sep.join(parts)}</nav>'

LEAD = {
    "ar": {"eyebrow": "تواصل مباشر", "h": "تحدث مع أحمد", "p": "اترك بياناتك وسيفتح واتساب برسالة جاهزة تصل لأحمد مباشرة. أخبرنا بما تفكر فيه، وسنرد عليك بالأسئلة التي تهم وضعك.",
           "points": ["الرد مباشرة على واتساب", "بدون أي التزام", "نبدأ من هدفك وميزانيتك، لا من المشروع"],
           "name": "الاسم", "phone": "رقم الهاتف", "phone_ph": "مثال: 971501234567+", "interest": "ما الذي تبحث عنه؟", "budget": "الميزانية التقريبية (درهم)",
           "msg": "رسالتك (اختياري)", "msg_ph": "مثلاً: أبحث عن فيلا لعائلتي خلال سنة…", "send": "إرسال عبر واتساب",
           "note": "عند الضغط سيفتح واتساب برسالة جاهزة، اضغط إرسال فقط.", "ok": "تم تجهيز رسالتك في واتساب. إذا لم يفتح تلقائياً، اضغط الزر مرة أخرى.",
           "err": "من فضلك اكتب الاسم ورقم هاتف صحيح.",
           "interests": ["شراء فيلا أو تاون هاوس", "استثمار في مشروع قيد الإنشاء", "مقارنة مشاريع", "استشارة تسويق ونمو أعمال", "أخرى"],
           "budgets": ["لم أحدد بعد", "أقل من 2 مليون", "من 2 إلى 5 ملايين", "من 5 إلى 15 مليون", "أكثر من 15 مليون"],
           "wa": {"hi": "مرحباً أحمد، أنا", "phone": "الهاتف", "interest": "أبحث عن", "budget": "الميزانية", "msg": "الرسالة", "page": "من صفحة"}},
    "en": {"eyebrow": "Direct contact", "h": "Talk to Ahmed", "p": "Leave your details and WhatsApp opens with a ready message to Ahmed. Tell us what you're weighing up and we'll reply with the questions that matter for your situation.",
           "points": ["Reply directly on WhatsApp", "No obligation", "We start from your goal and budget, not a project"],
           "name": "Name", "phone": "Phone number", "phone_ph": "e.g. +971501234567", "interest": "What are you looking for?", "budget": "Approximate budget (AED)",
           "msg": "Message (optional)", "msg_ph": "e.g. Looking for a family villa within a year…", "send": "Send via WhatsApp",
           "note": "WhatsApp opens with your message ready. Just tap send.", "ok": "Your WhatsApp message is ready. If it didn't open, tap the button again.",
           "err": "Please enter your name and a valid phone number.",
           "interests": ["Buying a villa or townhouse", "Off-plan investment", "Comparing projects", "Marketing & business growth advice", "Other"],
           "budgets": ["Not decided yet", "Under 2M", "2M – 5M", "5M – 15M", "Over 15M"],
           "wa": {"hi": "Hi Ahmed, I'm", "phone": "Phone", "interest": "Looking for", "budget": "Budget", "msg": "Message", "page": "From page"}},
}

def lead_form(lang, topic="", interest=0):
    """Contact form shown on every page; submit opens WhatsApp with the details."""
    if not C.WHATSAPP:
        return ""
    L = LEAD[lang]
    opts = lambda xs, sel=-1: "".join(f'<option{" selected" if i == sel else ""}>{escape(x)}</option>' for i, x in enumerate(xs))
    pts = "".join(f"<li>{escape(x)}</li>" for x in L["points"])
    msg = escape(topic)
    return f"""<section class="lead" id="contact"><div class="wrap lead-grid">
<div class="lead-intro"><p class="eyebrow">{L['eyebrow']}</p><h2>{L['h']}</h2><p>{escape(L['p'])}</p><ul class="lead-points">{pts}</ul>
<div class="lead-who"><img src="/assets/img/ahmed-esmat-dubai-advisor-600.webp" width="600" height="600" alt="{'أحمد عصمت' if lang == 'ar' else 'Ahmed Esmat'}" loading="lazy" decoding="async"><div><b>{'أحمد عصمت' if lang == 'ar' else 'Ahmed Esmat'}</b><span dir="ltr">+{C.WHATSAPP[:3]} {C.WHATSAPP[3:5]} {C.WHATSAPP[5:8]} {C.WHATSAPP[8:]}</span></div></div></div>
<form class="lead-form" data-wa="{C.WHATSAPP}" data-l='{escape(json.dumps(L["wa"], ensure_ascii=False))}' novalidate>
<div class="frow"><label>{L['name']}<input name="name" autocomplete="name" required maxlength="80"></label>
<label>{L['phone']}<input name="phone" type="tel" inputmode="tel" autocomplete="tel" dir="ltr" required placeholder="{L['phone_ph']}" maxlength="25"></label></div>
<div class="frow"><label>{L['interest']}<select name="interest">{opts(L['interests'], interest)}</select></label>
<label>{L['budget']}<select name="budget">{opts(L['budgets'], 0)}</select></label></div>
<label>{L['msg']}<textarea name="msg" rows="3" maxlength="600" placeholder="{L['msg_ph']}">{msg}</textarea></label>
<p class="lead-err" role="alert" hidden>{L['err']}</p>
<button class="btn wa-btn" type="submit"><svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.7-1.4.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.8 11.9 11.9 0 0 0 4.6 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.2 2.2 2.2 0 0 0 .2-1.2c-.1-.1-.3-.2-.5-.3Z"/></svg>{L['send']}</button>
<p class="note">{L['note']}</p><p class="lead-ok" role="status" hidden>{L['ok']}</p>
</form></div></section>"""

BOOKING_TEXT = {
    "en": {
        "eyebrow": "Book a consultation", "heading": "Choose a time to talk", "intro": "Share the essentials, then choose an available 30-minute slot.",
        "trust": ["30 minutes", "Online or in person", "No obligation"], "details": "1. Your details", "time": "2. Pick a day and an hour", "done": "3. Confirmation",
        "name": "Full name", "phone": "Mobile / WhatsApp", "email": "Email (optional)", "interest": "I am interested in", "emirate": "Emirate", "budget": "Budget in AED", "purpose": "Purpose", "timeline": "When do you plan to buy?",
        "interests": [("villa", "Villa"), ("townhouse", "Townhouse"), ("offplan", "Off-plan launch"), ("unsure", "Not sure")],
        "emirates": [("dubai", "Dubai"), ("abu-dhabi", "Abu Dhabi"), ("both", "Both")],
        "budgets": [("under-2", "Under 2M"), ("2-3", "2M–3M"), ("3-5", "3M–5M"), ("5-8", "5M–8M"), ("8-12", "8M–12M"), ("over-12", "Over 12M")],
        "purposes": [("live", "Live in it"), ("invest", "Invest"), ("both", "Both")],
        "timelines": [("0-3", "Within 3 months"), ("3-6", "3–6 months"), ("6-12", "6–12 months"), ("exploring", "Just exploring")],
        "consent": "I agree to be contacted about my enquiry and to the privacy notice.", "continue": "Continue", "minute": "Takes about one minute.",
        "meeting": "Meeting type", "meetings": [("phone", "Phone / WhatsApp call"), ("video", "Video call"), ("person", "In person (Dubai)")],
        "confirm": "Confirm booking", "back": "Back", "dubai_time": "Dubai time (UTC+4)", "loading": "Checking availability…", "pick_day": "Choose a day to see available times.",
        "required": "Please complete all required fields and enter a valid mobile number.", "slot_required": "Please choose a day, time and meeting type.", "taken": "This time was just taken. Please pick another.",
        "name_invalid": "Please write your name using letters only.", "too_many": "You already have upcoming consultations. Message Ahmed on WhatsApp to change one.", "booked": "You're booked", "request": "Your consultation request is ready", "fallback": "The live calendar is not connected yet. Send the prepared WhatsApp message to complete your request.",
        "calendar": "Add to calendar", "google": "Google Calendar", "whatsapp": "Message Ahmed on WhatsApp", "change": "Change the time", "privacy": "/privacy/"
    },
    "ar": {
        "eyebrow": "احجز استشارة", "heading": "اختر موعدًا للحديث", "intro": "شارك المعلومات الأساسية، ثم اختر موعدًا متاحًا لمدة 30 دقيقة.",
        "trust": ["30 دقيقة", "عن بُعد أو وجاهيًا", "دون التزام"], "details": "1. بياناتك", "time": "2. اختر اليوم والساعة", "done": "3. التأكيد",
        "name": "الاسم الكامل", "phone": "رقم الموبايل / واتساب", "email": "البريد الإلكتروني (اختياري)", "interest": "أنا مهتم بـ", "emirate": "الإمارة", "budget": "الميزانية بالدرهم", "purpose": "الغرض", "timeline": "متى تخطط للشراء؟",
        "interests": [("villa", "فيلا"), ("townhouse", "تاون هاوس"), ("offplan", "إطلاق جديد"), ("unsure", "غير متأكد")],
        "emirates": [("dubai", "دبي"), ("abu-dhabi", "أبوظبي"), ("both", "كلاهما")],
        "budgets": [("under-2", "أقل من 2 مليون"), ("2-3", "2–3 ملايين"), ("3-5", "3–5 ملايين"), ("5-8", "5–8 ملايين"), ("8-12", "8–12 مليونًا"), ("over-12", "أكثر من 12 مليونًا")],
        "purposes": [("live", "للسكن"), ("invest", "للاستثمار"), ("both", "كلاهما")],
        "timelines": [("0-3", "خلال 3 أشهر"), ("3-6", "خلال 3–6 أشهر"), ("6-12", "خلال 6–12 شهرًا"), ("exploring", "أستكشف فقط")],
        "consent": "أوافق على التواصل معي بشأن استفساري وعلى إشعار الخصوصية.", "continue": "متابعة", "minute": "يستغرق نحو دقيقة واحدة.",
        "meeting": "نوع المقابلة", "meetings": [("phone", "مكالمة هاتف / واتساب"), ("video", "مكالمة فيديو"), ("person", "مقابلة شخصية في دبي")],
        "confirm": "تأكيد الموعد", "back": "رجوع", "dubai_time": "بتوقيت دبي (UTC+4)", "loading": "جارٍ التحقق من المواعيد…", "pick_day": "اختر يومًا لعرض الساعات المتاحة.",
        "required": "يرجى إكمال الحقول المطلوبة وإدخال رقم موبايل صحيح.", "slot_required": "يرجى اختيار اليوم والساعة ونوع المقابلة.", "taken": "حُجز هذا الموعد للتو. اختر موعدًا آخر.",
        "name_invalid": "يرجى كتابة الاسم بالحروف فقط.", "too_many": "لديك مواعيد قادمة بالفعل. راسل أحمد على واتساب لتغيير أحدها.", "booked": "تم حجز موعدك", "request": "طلب الاستشارة جاهز", "fallback": "التقويم المباشر غير متصل بعد. أرسل رسالة واتساب الجاهزة لإكمال الطلب.",
        "calendar": "أضف إلى التقويم", "google": "تقويم Google", "whatsapp": "راسل أحمد على واتساب", "change": "غيّر الموعد", "privacy": "/ar/privacy/"
    },
}

def booking_form(lang, topic="", interest="", compact=False, anchor="contact", heading=None):
    """Reusable three-step booking form. Backend URL is optional by design."""
    L = BOOKING_TEXT[lang]
    option_html = lambda items, sel="": "".join(f'<option value="{escape(v)}"{" selected" if v == sel else ""}>{escape(t)}</option>' for v, t in items)
    radio_html = lambda name, items: '<div class="choice-grid">' + "".join(
        f'<label><input type="radio" name="{name}" value="{escape(v)}" required> {escape(t)}</label>' for v, t in items) + '</div>'
    trust = " · ".join(L["trust"])
    # The closed select shows flag + code only (site.js swaps the full names in while the list is open)
    countries = "".join(f'<option value="{code}" data-flag="{k}" data-full="{code} {ar if lang == "ar" else en}">{code if i == 0 else code + " " + (ar if lang == "ar" else en)}</option>'
                        for i, (k, code, en, ar) in enumerate(COUNTRIES))
    head = heading or L["heading"]
    form = f"""<div class="booking-card">
<form class="booking-form" data-lang="{lang}" data-wa="{C.WHATSAPP}" data-endpoint="{escape(getattr(C, 'BOOKING_ENDPOINT', ''))}" data-labels='{escape(json.dumps(L, ensure_ascii=False))}' novalidate>
<div class="booking-progress" aria-hidden="true"><span class="on"></span><span></span><span></span></div>
<input type="hidden" name="topic" value="{escape(topic)}"><input type="hidden" name="lead_id"><input type="hidden" name="tier"><input type="hidden" name="landing_url"><input type="hidden" name="language" value="{lang}">
<input type="hidden" name="utm_source"><input type="hidden" name="utm_medium"><input type="hidden" name="utm_campaign"><input type="hidden" name="utm_content"><input type="hidden" name="fbclid">
<label class="hp-field" aria-hidden="true">Company website<input name="website" tabindex="-1" autocomplete="off"></label>
<div class="booking-step" data-step="1"><h2>{L['details']}</h2>
<label>{L['name']}<input name="name" autocomplete="name" required maxlength="80"></label>
<label>{L['phone']}<span class="phone-input"><select name="country_code" data-flag="ae" aria-label="{'كود الدولة' if lang=='ar' else 'Country code'}">{countries}</select><input name="phone" type="tel" inputmode="tel" autocomplete="tel-national" dir="ltr" required maxlength="20"></span></label>
<label>{L['email']}<input name="email" type="email" autocomplete="email" maxlength="120"></label>
<div class="frow"><label>{L['interest']}<select name="interest" required>{option_html(L['interests'], interest)}</select></label><label>{L['emirate']}<select name="emirate" required>{option_html(L['emirates'])}</select></label></div>
<div class="frow"><label>{L['budget']}<select name="budget" required>{option_html(L['budgets'])}</select></label><label>{L['purpose']}<select name="purpose" required>{option_html(L['purposes'])}</select></label></div>
<label>{L['timeline']}<select name="timeline" required>{option_html(L['timelines'])}</select></label>
<label class="consent-row"><input type="checkbox" name="consent" required><span>{L['consent']} <a href="{L['privacy']}">{'إشعار الخصوصية' if lang=='ar' else 'Privacy notice'}</a></span></label>
<p class="booking-error" role="alert" hidden></p><button class="btn booking-next" type="button">{L['continue']}</button><p class="note">{L['minute']}</p></div>
<div class="booking-step" data-step="2" hidden><h2>{L['time']}</h2><p class="time-note">{L['dubai_time']} <span class="visitor-zone"></span></p><div class="day-chips" role="group"></div><p class="slot-status note">{L['pick_day']}</p><div class="slot-chips" role="group"></div><span class="field-label">{L['meeting']}</span>{radio_html('meeting_type', L['meetings'])}
<p class="booking-error" role="alert" hidden></p><div class="booking-actions"><button class="btn ghost booking-back" type="button">{L['back']}</button><button class="btn booking-confirm-btn" type="button">{L['confirm']}</button></div></div>
<div class="booking-step booking-confirm" data-step="3" hidden><h2>{L['done']}</h2><p class="confirmation-copy"></p><div class="booking-actions"><a class="btn ics-link" href="#" hidden download="consultation.ics">{L['calendar']}</a><a class="btn ghost google-link" href="https://calendar.google.com/" hidden target="_blank" rel="noopener">{L['google']}</a><a class="btn wa-confirm" href="https://wa.me/{C.WHATSAPP}" target="_blank" rel="noopener">{L['whatsapp']}</a><button class="btn ghost booking-change" type="button">{L['change']}</button></div></div>
</form><p class="time-note booking-trust">{escape(trust)}</p></div>"""
    if compact:
        return form
    return f'<section class="lead" id="{anchor}"><div class="wrap lead-grid"><div class="lead-intro"><p class="eyebrow">{L["eyebrow"]}</p><h2>{escape(head)}</h2><p>{escape(L["intro"])}</p><ul class="lead-points">' + "".join(f'<li>{escape(x)}</li>' for x in L['trust']) + f'</ul></div>{form}</div></section>'

WA_ICON = '<svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.7-1.4.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.8 11.9 11.9 0 0 0 4.6 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.2 2.2 2.2 0 0 0 .2-1.2c-.1-.1-.3-.2-.5-.3Z"/></svg>'

# All old call sites now receive the shared booking component.
def lead_form(lang, topic="", interest=0, heading=None):
    interest_map = {0: "villa", 1: "offplan", 2: "unsure", 3: "unsure"}
    return booking_form(lang, topic=topic, interest=interest_map.get(interest, ""), heading=heading)

def page(*, lang, path, title, description, body, alt_path=None, schemas=(), og_type="website", og_img="skyline-night", home_page=False,
         lead=True, lead_topic="", lead_interest=0, lead_heading=None, minimal_header=False):
    rtl = lang == "ar"
    canonical = C.DOMAIN + path
    alt = ""
    if alt_path:
        en_p, ar_p = (path, alt_path) if lang == "en" else (alt_path, path)
        alt = (f'<link rel="alternate" hreflang="en" href="{C.DOMAIN}{en_p}">\n'
               f'<link rel="alternate" hreflang="ar" href="{C.DOMAIN}{ar_p}">\n'
               f'<link rel="alternate" hreflang="x-default" href="{C.DOMAIN}{en_p}">')
    lang_link = alt_path or ("/" if rtl else "/ar/")
    lang_label = "English" if rtl else "العربية"
    nav_items = list(NAV[lang])
    if GUIDES_LIVE:  # brief 4.5: real-estate section, shown once the first guide is published
        nav_items.insert(-1, ("/ar/guides/", "أدلة الشراء") if rtl else ("/guides/", "Buying guides"))
    nav = "".join(f'<a href="{u}">{escape(t)}</a>' for u, t in nav_items)
    lead_html = lead_form(lang, lead_topic, lead_interest, lead_heading) if lead else ""
    talk = "احجز استشارة" if rtl else "Book a consultation"
    brand_sub = "استشارات عقارية في دبي وأبوظبي" if rtl else "Dubai & Abu Dhabi real estate advisory"
    brand = "أحمد عصمت" if rtl else "Ahmed Esmat"
    home = "/ar/" if rtl else "/"
    foot_tag = ("القرار أولاً، ثم المشروع. استشارات مستقلة في دبي وأبوظبي." if rtl
                else "The decision first, then the property. Independent advice across Dubai and Abu Dhabi.")
    f = FOOT[lang]
    cols = "".join(f'<div><h3>{h}</h3>' + "".join(f'<a href="{u}">{escape(t)}</a>' for u, t in links) + "</div>" for h, links in f["cols"])
    lic = C.LICENSE_LINE_AR if rtl else C.LICENSE_LINE_EN
    lic_html = f"<p>{escape(lic)}</p>" if lic else ""
    social_html = f'<p><a href="{escape(C.INSTAGRAM)}" rel="noopener">Instagram · @a1esmat.investment</a></p>' if C.INSTAGRAM else ""
    wa = wa_link("مرحباً أحمد، أريد استشارة بخصوص الاستثمار في دبي" if rtl else "Hi Ahmed, I'd like advice on investing in Dubai")
    wa_float = f'<a class="wa-float contact-track" href="{wa}" rel="noopener">{"واتساب" if rtl else "WhatsApp"}</a>' if wa else ""
    book_href = "#contact" if (lead_html or 'id="contact"' in body) else ("/ar/book/" if rtl else "/book/")
    mobile_bar = (f'<div class="mobile-bookbar"><a class="btn" href="{book_href}">{talk}</a><a class="btn wa-mini contact-track" href="{wa}" aria-label="WhatsApp" rel="noopener">{WA_ICON}</a></div>' if wa else "")
    tracking_enabled = bool(C.GA4_ID or getattr(C, "META_PIXEL_ID", "") or getattr(C, "CLARITY_ID", ""))
    site_cfg = json.dumps({"ga4": C.GA4_ID, "meta": getattr(C, "META_PIXEL_ID", ""), "clarity": getattr(C, "CLARITY_ID", ""),
                           "bookingEndpoint": getattr(C, "BOOKING_ENDPOINT", ""), "lang": lang,
                           "timezone": getattr(C, "BOOKING_TIMEZONE", "Asia/Dubai"), "days": getattr(C, "BOOKING_DAYS", [1,2,3,4,5,6]),
                           "start": getattr(C, "BOOKING_START", "10:00"), "end": getattr(C, "BOOKING_END", "19:00"),
                           "slot": getattr(C, "BOOKING_SLOT_MINUTES", 30), "buffer": getattr(C, "BOOKING_BUFFER_MINUTES", 15),
                           "notice": getattr(C, "BOOKING_MIN_NOTICE_HOURS", 3), "horizon": getattr(C, "BOOKING_HORIZON_DAYS", 14)}, ensure_ascii=False).replace("</", "<\\/")
    cookie = ""
    if tracking_enabled:
        cookie = (f'<div class="cookie-banner" role="dialog" aria-label="Cookie preferences" hidden><p>'
                  f'{"نستخدم ملفات أساسية، وبموافقتك نستخدم التحليلات لقياس أداء الموقع." if rtl else "We use essential storage and, with your permission, analytics to measure site performance."} '
                  f'<a href="{"/ar/privacy/" if rtl else "/privacy/"}">{"الخصوصية" if rtl else "Privacy"}</a></p><div class="cookie-actions">'
                  f'<button class="btn cookie-accept" type="button">{"قبول التحليلات" if rtl else "Accept analytics"}</button>'
                  f'<button class="btn ghost cookie-reject" type="button">{"الأساسية فقط" if rtl else "Essential only"}</button></div></div>')
    nav_inner = (f'<a class="lang" href="{lang_link}" hreflang="{"en" if rtl else "ar"}" lang="{"en" if rtl else "ar"}">{lang_label}</a>' if minimal_header else
                 f'{nav}<a class="btn small" href="{"#contact" if lead_html else ("/ar/book/" if rtl else "/book/")}">{talk}</a><a class="lang" href="{lang_link}" hreflang="{"en" if rtl else "ar"}" lang="{"en" if rtl else "ar"}">{lang_label}</a>')
    burger = "" if minimal_header else f'<button class="burger" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="{"القائمة" if rtl else "Menu"}"><span></span></button>'
    gsc = f'<meta name="google-site-verification" content="{C.GSC_VERIFICATION}">' if C.GSC_VERIFICATION else ""
    schema_html = "\n".join(ld(s) for s in schemas)
    preload_fonts = "\n".join(f'<link rel="preload" href="/assets/fonts/{f}" as="font" type="font/woff2" crossorigin>' for f in PRELOAD[lang])
    skip = "انتقل إلى المحتوى" if rtl else "Skip to content"
    return f"""<!doctype html>
<html lang="{lang}" dir="{'rtl' if rtl else 'ltr'}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(description)}">
<link rel="canonical" href="{canonical}">
{alt}
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:locale" content="{'ar_AE' if rtl else 'en_AE'}">
<meta property="og:site_name" content="Ahmed Esmat">
<meta property="og:image" content="{img_url(og_img)}">
<meta property="og:image:alt" content="{escape(IMAGES[og_img][lang])}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0E1B20">
<meta name="robots" content="max-image-preview:large">
{gsc}
{preload_fonts}
<style>{INLINE_CSS[lang]}</style>
<link rel="icon" href="/assets/icons/icon-32.png" sizes="32x32" type="image/png">
<link rel="icon" href="/assets/icons/icon-192.png" sizes="192x192" type="image/png">
<link rel="apple-touch-icon" href="/assets/icons/icon-180.png">
{schema_html}
<script>window.A1CFG={site_cfg};</script>
</head>
<body{' class="home"' if home_page else ''}>
<script>document.documentElement.classList.add('js')</script>
<a class="skip" href="#main">{skip}</a>
<header class="site-head"><div class="wrap">
<a class="brand" href="{home}"><img class="mark" src="/assets/img/a1esmat-logo-mark.webp" width="118" height="112" alt=""><span class="bt">{brand}<small>{brand_sub}</small></span></a>
{burger}
<nav class="nav" id="site-nav" aria-label="{'القائمة الرئيسية' if rtl else 'Main'}">{nav_inner}</nav>
</div></header>
<main id="main">
{body}
{lead_html}
</main>
<footer class="site-foot"><div class="wrap">
<div class="foot-brand"><a class="brand" href="{home}"><img class="mark" src="/assets/img/a1esmat-logo-mark.webp" width="118" height="112" alt=""><span class="bt">{brand}<small>{brand_sub}</small></span></a><p>{escape(foot_tag)}</p></div>
<div class="fcols">{cols}</div>
<div class="legal">{lic_html}{social_html}<p>{escape(f['legal'])}</p><p>© 2026 Ahmed Esmat · a1esmat.com</p></div>
</div></footer>
{wa_float}
{mobile_bar}
{cookie}
<script src="/assets/js/site.js?v={JS_V}" defer></script>
</body>
</html>
"""

CSS_V = hashlib.md5(CSS.encode("utf-8")).hexdigest()[:10]
# Cache-busting version for site.js: changes whenever the file changes (assets are cached for a year)
JS_V = hashlib.md5(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "js", "site.js"), "rb").read()).hexdigest()[:10]

# Self-hosted fonts + CSS inlined into every page: no render-blocking requests
import os as _os, re as _re
_FONTS = open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "static", "fonts", "fonts.css"), encoding="utf-8").read()

def _minify(css):
    css = _re.sub(r"/\*.*?\*/", "", css, flags=_re.S)
    css = _re.sub(r"\s+", " ", css)
    css = _re.sub(r"\s*([{};,>])\s*", r"\1", css)
    return css.replace(";}", "}").strip()

PRELOAD = {"ar": ["ibm-plex-sans-arabic-400-arabic.woff2", "el-messiri-600-arabic.woff2"],
           "en": ["ibm-plex-sans-arabic-400-latin.woff2", "playfair-display-500-latin.woff2"]}

def _fonts_for(lang):
    # preload + font-display:optional -> fonts never swap in after first paint, so they cause no layout shift (CLS)
    faces = _FONTS.replace("font-display:swap", "font-display:optional").strip().splitlines()
    # Latin text inside Arabic headings uses Playfair; skip El Messiri's Latin file entirely
    return "\n".join(f for f in faces if "el-messiri-600-latin" not in f)

INLINE_CSS = {l: _minify(_fonts_for(l) + CSS) for l in ("ar", "en")}
