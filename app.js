'use strict';
const $ = s => document.querySelector(s);
const $$ = s => [...document.querySelectorAll(s)];
const articles = $$('.slide-article');
const search = $('#search');
const chapterFilter = $('#chapter-filter');
const modes = {
  traditional: ['MATH 1.0', '研究问题促进人的理解，理解帮助产生答案，答案又反过来带来新方法和新问题。纯数学中的洞见也支持应用判断。'],
  bypass: ['THE RISK', 'AI 直接产出答案，人的理解可能没有同步增长。应用中的形式化目标也可能偏离真实目的。图中呈现的是作者担心的风险路径。'],
  augment: ['MATH 2.0', 'AI 帮助提出问题、解释证明、建立联系，并支持应用中的判断。答案继续回流为可分享、可复用的理解。']
};
$$('[data-mode]').filter(el=>el.tagName==='BUTTON').forEach(button => button.addEventListener('click', () => {
  $$('.mode-buttons button').forEach(b=>b.setAttribute('aria-pressed', String(b===button)));
  $('#eco-svg').dataset.mode=button.dataset.mode;
  const [tag,text]=modes[button.dataset.mode];
  $('#mode-tag').textContent=tag;
  $('#mode-explanation').textContent=text;
}));
function filter(){
  const query=search.value.trim().toLocaleLowerCase();
  let count=0;
  articles.forEach(article=>{
    const matchesNumber=/^\d+$/.test(query) && Number(query)===Number(article.dataset.page);
    const matchesText=!/^\d+$/.test(query) && article.textContent.toLocaleLowerCase().includes(query);
    const show=(!query || matchesNumber || matchesText) && (chapterFilter.value==='all' || chapterFilter.value===article.dataset.chapter);
    article.hidden=!show;
    if(show)count++;
  });
  $$('.chapter-heading').forEach((header,i)=>header.hidden=!articles.some(a=>a.dataset.chapter===String(i)&&!a.hidden));
  $('#result-count').textContent=`${count} / 27 页`;
  $('#empty-state').hidden=count!==0;
  $('#reset-filter').hidden=!query&&chapterFilter.value==='all';
}
search.addEventListener('input',filter);
chapterFilter.addEventListener('change',filter);
$('#reset-filter').addEventListener('click',()=>{search.value='';chapterFilter.value='all';filter();search.focus();});
function resetForNavigation(){search.value='';chapterFilter.value='all';filter();}
$$('a[href^="#p-"],a[href^="#chapter-"]').forEach(link=>link.addEventListener('click',resetForNavigation));
$('#page-jump').addEventListener('change',e=>{
  if(!e.target.value)return;
  resetForNavigation();
  location.hash='p-'+String(e.target.value).padStart(2,'0');
  e.target.value='';
});
function revealHash(){
  const hash=location.hash;
  if(!/^#(?:p-\d{2}|chapter-\d)$/.test(hash))return;
  const target=$(hash);
  if(target){resetForNavigation();requestAnimationFrame(()=>target.scrollIntoView());}
}
window.addEventListener('hashchange',revealHash);
if(location.hash)requestAnimationFrame(revealHash);
let scrollPending=false;
function updateProgress(){
  const available=document.documentElement.scrollHeight-innerHeight;
  $('#read-progress').style.width=(available>0?Math.min(100,Math.max(0,scrollY/available*100)):0)+'%';
  scrollPending=false;
}
window.addEventListener('scroll',()=>{if(!scrollPending){scrollPending=true;requestAnimationFrame(updateProgress);}},{passive:true});
window.addEventListener('resize',updateProgress);
updateProgress();
const observer=new IntersectionObserver(entries=>{
  const current=entries.filter(e=>e.isIntersecting).sort((a,b)=>a.boundingClientRect.top-b.boundingClientRect.top)[0];
  if(current){
    $$('.page-link').forEach(a=>a.removeAttribute('aria-current'));
    const link=$('.page-link[data-page="'+current.target.dataset.page+'"]');
    if(link)link.setAttribute('aria-current','true');
  }
},{rootMargin:'-5% 0px -65% 0px',threshold:0});
articles.forEach(a=>observer.observe(a));
const dialog=$('#slide-dialog');
let slide=1;
function showSlide(n){
  slide=Math.max(1,Math.min(27,n));
  const image=$('#dialog-image');
  image.src=`slide-${String(slide).padStart(2,'0')}.webp`;
  image.alt=`Math 2.0 原始幻灯片第 ${slide} 页`;
  $('#dialog-title').textContent=`原始幻灯片 · ${String(slide).padStart(2,'0')} / 27`;
  $('#dialog-pdf').href='https://teorth.github.io/tao-web/slides/math-2-0-caltech-2026.pdf#page='+slide;
  $('#previous-slide').disabled=slide===1;
  $('#next-slide').disabled=slide===27;
}
$$('[data-slide]').forEach(button=>button.addEventListener('click',()=>{
  showSlide(Number(button.dataset.slide));dialog.showModal();
}));
$('#close-dialog').addEventListener('click',()=>dialog.close());
$('#previous-slide').addEventListener('click',()=>showSlide(slide-1));
$('#next-slide').addEventListener('click',()=>showSlide(slide+1));
dialog.addEventListener('click',e=>{if(e.target===dialog){const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)dialog.close();}});
dialog.addEventListener('keydown',e=>{if(e.key==='ArrowRight'){showSlide(slide+1);e.preventDefault();}if(e.key==='ArrowLeft'){showSlide(slide-1);e.preventDefault();}});
