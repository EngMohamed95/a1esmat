import json, hashlib
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

.wa-float{position:fixed;inset-inline-end:1rem;bottom:1rem;z-index:15;background:#1F8F5F;color:#fff;border-radius:999px;padding:.8rem 1.25rem;text-decoration:none;font-weight:600;box-shadow:0 10px 30px -8px rgba(14,27,32,.45)}
.wa-float:hover{color:#fff;background:#187650}

/* reveal on scroll (only when JS is running) */
.js .reveal{opacity:0;transform:translateY(22px);transition:opacity .8s var(--ease),transform .8s var(--ease)}
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
"""

CSS_V = None  # set below, after CSS is defined

def img(key, lang, cls="", eager=False, sizes="100vw"):
    """Responsive <img> for an image in data_images.IMAGES."""
    im = IMAGES[key]
    a = escape(im[lang])
    small, big = im.get("w", (900, 1920))
    h = round(small * im.get("h", 2 / 3))
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="/assets/img/{key}-{small}.webp" srcset="/assets/img/{key}-{small}.webp {small}w, /assets/img/{key}-{big}.webp {big}w" '
            f'sizes="{sizes}" width="{small}" height="{h}" alt="{a}" {load} decoding="async">')

def img_url(key):
    return f"{C.DOMAIN}/assets/img/{key}-{IMAGES[key].get('w', (900, 1920))[1]}.webp"

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

NAV = {
    "en": [("/off-plan-properties-dubai/", "Off-plan"), ("/off-plan-villas-dubai/", "Villas"),
           ("/off-plan-townhouses-dubai/", "Townhouses"), ("/projects/", "Projects"),
           ("/investor-assessment/", "Investor assessment")],
    "ar": [("/ar/villas-for-sale-dubai/", "فلل للبيع"), ("/ar/townhouses-for-sale-dubai/", "تاون هاوس"),
           ("/ar/villas-installments-dubai/", "بالتقسيط"), ("/ar/projects/", "المشاريع"),
           ("/ar/investor-assessment/", "التقييم الاستثماري")],
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
            ("Start here", [("/investor-assessment/", "Investor assessment"), ("/book/", "Talk to Ahmed"), ("/blog/", "Marketing articles (Arabic)"), ("/disclaimer/", "Disclaimer"), ("/ar/", "العربية")]),
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
            ("ابدأ من هنا", [("/ar/investor-assessment/", "التقييم الاستثماري"), ("/ar/book/", "تحدث مع أحمد"), ("/blog/", "مقالات في التسويق"), ("/ar/disclaimer/", "إخلاء المسؤولية"), ("/", "English")]),
        ],
        "legal": "يقدم أحمد عصمت استشارات في العقار والأعمال. لا يُعد أي محتوى في هذا الموقع نصيحة مالية أو ضماناً لعائد. معلومات المشاريع مراجعة بالتاريخ المذكور في كل صفحة وقد تتغير، لذا تأكد من الأسعار وخطط الدفع ومواعيد التسليم مع المطور قبل أي التزام. الموقع غير مرتبط بأي مطور ما لم يُذكر خلاف ذلك.",
    },
}

def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>"

def person_schema():
    return {
        "@context": "https://schema.org", "@type": "Person", "@id": C.DOMAIN + "/#ahmed",
        "name": "Ahmed Esmat", "alternateName": "أحمد عصمت", "url": C.DOMAIN + "/",
        "image": img_url("ahmed-esmat-dubai-advisor"),
        "jobTitle": "Real estate and business advisor", "areaServed": "Dubai, United Arab Emirates",
        "sameAs": [C.INSTAGRAM] if C.INSTAGRAM else [],
        "knowsAbout": ["Dubai real estate", "Off-plan property", "Villas and townhouses", "Performance marketing", "Business growth"],
    }

def website_schema():
    return {"@context": "https://schema.org", "@type": "WebSite", "@id": C.DOMAIN + "/#site",
            "url": C.DOMAIN + "/", "name": "Ahmed Esmat", "alternateName": ["A1esmat", "أحمد عصمت"], "inLanguage": ["en", "ar"],
            "publisher": {"@id": C.DOMAIN + "/#ahmed"}, "image": C.DOMAIN + "/assets/img/a1esmat-logo.png"}

def crumbs_schema(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": C.DOMAIN + u} for i, (u, n) in enumerate(items)]}

def faq_schema(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}

def faq_html(faqs, title):
    out = [f'<section class="faq" id="faq"><h2>{title}</h2>']
    for q, a in faqs:
        out.append(f"<details><summary>{escape(q)}</summary><p>{escape(a)}</p></details>")
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

def page(*, lang, path, title, description, body, alt_path=None, schemas=(), og_type="website", og_img="skyline-night", home_page=False):
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
    nav = "".join(f'<a href="{u}">{escape(t)}</a>' for u, t in NAV[lang])
    talk = "تحدث مع أحمد" if rtl else "Talk to Ahmed"
    brand_sub = "استشارات عقارية واستثمارية في دبي" if rtl else "Dubai real estate & business advisory"
    brand = "أحمد عصمت" if rtl else "Ahmed Esmat"
    home = "/ar/" if rtl else "/"
    foot_tag = ("القرار أولاً، ثم المشروع. استشارات مستقلة للمستثمرين وأصحاب الأعمال في دبي." if rtl
                else "The decision first, then the property. Independent advice for investors and business owners in Dubai.")
    f = FOOT[lang]
    cols = "".join(f'<div><h3>{h}</h3>' + "".join(f'<a href="{u}">{escape(t)}</a>' for u, t in links) + "</div>" for h, links in f["cols"])
    lic = C.LICENSE_LINE_AR if rtl else C.LICENSE_LINE_EN
    lic_html = f"<p>{escape(lic)}</p>" if lic else ""
    wa = wa_link("مرحباً أحمد، أريد استشارة بخصوص الاستثمار في دبي" if rtl else "Hi Ahmed, I'd like advice on investing in Dubai")
    wa_float = f'<a class="wa-float" href="{wa}" rel="noopener">{"واتساب" if rtl else "WhatsApp"}</a>' if wa else ""
    ga = ""
    if C.GA4_ID:
        ga = (f'<script async src="https://www.googletagmanager.com/gtag/js?id={C.GA4_ID}"></script>'
              f"<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','{C.GA4_ID}');</script>")
    gsc = f'<meta name="google-site-verification" content="{C.GSC_VERIFICATION}">' if C.GSC_VERIFICATION else ""
    schema_html = "\n".join(ld(s) for s in schemas)
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
<meta property="og:image" content="{C.DOMAIN}/assets/img/{og_img}-1920.webp">
<meta property="og:image:alt" content="{escape(IMAGES[og_img][lang])}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0E1B20">
{gsc}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=El+Messiri:wght@500;600;700&family=IBM+Plex+Sans+Arabic:wght@400;500;600&family=Playfair+Display:wght@500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css?v={CSS_V}">
<link rel="icon" href="/assets/icons/icon-32.png" sizes="32x32" type="image/png">
<link rel="icon" href="/assets/icons/icon-192.png" sizes="192x192" type="image/png">
<link rel="apple-touch-icon" href="/assets/icons/icon-180.png">
{schema_html}
{ga}
</head>
<body{' class="home"' if home_page else ''}>
<script>document.documentElement.classList.add('js')</script>
<a class="skip" href="#main">{skip}</a>
<header class="site-head"><div class="wrap">
<a class="brand" href="{home}"><img class="mark" src="/assets/img/a1esmat-logo-mark.webp" width="118" height="112" alt=""><span class="bt">{brand}<small>{brand_sub}</small></span></a>
<button class="burger" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="{'القائمة' if rtl else 'Menu'}"><span></span></button>
<nav class="nav" id="site-nav" aria-label="{'القائمة الرئيسية' if rtl else 'Main'}">{nav}<a class="btn small" href="{'/ar/book/' if rtl else '/book/'}">{talk}</a><a class="lang" href="{lang_link}" hreflang="{'en' if rtl else 'ar'}" lang="{'en' if rtl else 'ar'}">{lang_label}</a></nav>
</div></header>
<main id="main">
{body}
</main>
<footer class="site-foot"><div class="wrap">
<div class="foot-brand"><a class="brand" href="{home}"><img class="mark" src="/assets/img/a1esmat-logo-mark.webp" width="118" height="112" alt=""><span class="bt">{brand}<small>{brand_sub}</small></span></a><p>{escape(foot_tag)}</p></div>
<div class="fcols">{cols}</div>
<div class="legal">{lic_html}<p>{escape(f['legal'])}</p><p>© 2026 Ahmed Esmat · a1esmat.com</p></div>
</div></footer>
{wa_float}
<script>
(function(){{var h=document.querySelector('.site-head');
var bt=h.querySelector('.burger');bt.addEventListener('click',function(){{var o=h.classList.toggle('open');bt.setAttribute('aria-expanded',o)}});
h.querySelectorAll('.nav a').forEach(function(a){{a.addEventListener('click',function(){{h.classList.remove('open');bt.setAttribute('aria-expanded','false')}})}});
if(document.body.classList.contains('home')){{var s=function(){{h.classList.toggle('scrolled',scrollY>40)}};s();addEventListener('scroll',s,{{passive:true}})}}
var els=document.querySelectorAll('.pcard,.tile,.steps li,.q4 > div,.split,.mini,.fitbox,.strengths,.risks');
if(!('IntersectionObserver' in window))return;
var io=new IntersectionObserver(function(es){{es.forEach(function(e){{if(e.isIntersecting){{e.target.classList.add('in');io.unobserve(e.target)}}}})}},{{rootMargin:'0px 0px -8% 0px'}});
els.forEach(function(el,i){{el.classList.add('reveal');el.style.transitionDelay=(i%4)*70+'ms';io.observe(el)}});
}})();
</script>
</body>
</html>
"""

CSS_V = hashlib.md5(CSS.encode("utf-8")).hexdigest()[:10]
