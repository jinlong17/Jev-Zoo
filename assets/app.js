// The JSON loaded here is a build projection of catalog/catalog.json, never a second registry.
const zh = document.body.dataset.locale === 'zh';
const $ = (selector, node = document) => node.querySelector(selector);
const $$ = (selector, node = document) => [...node.querySelectorAll(selector)];
const text = (en, cn) => zh ? cn : en;
const escapeHTML = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const localized = value => typeof value === 'object' ? (value[zh ? 'zh' : 'en'] || value.en || '') : value;
const types = {model:['Models','模型'],paper:['Papers','论文'],tool:['Tools & SDKs','工具与 SDK'],framework:['Frameworks','框架'],benchmark:['Benchmarks','基准'],dataset:['Data','数据'],component:['Agent components','Agent 组件'],application:['Applications & demos','应用与演示'],service:['Services','商业服务'],recipe:['Recipes','配方'],directory:['Discovery lists','资源索引']};
const uses = {routing:['Routing','路由'],judging:['Judging','评判'],verification:['Verification & safety','验证与安全'],memory:['Memory & retrieval','记忆与检索'],training:['Training & distillation','训练与蒸馏'],evaluation:['Evaluation & calibration','评测与校准'],deployment:['Inference & deployment','推理与部署'],automation:['Agents & automation','Agent 与自动化'],simulation:['Games & simulation','游戏与模拟'],discovery:['Resource discovery','资源发现']};
$('.menu-toggle')?.addEventListener('click', e => { const opened = $('.main-nav').classList.toggle('open'); e.currentTarget.setAttribute('aria-expanded', opened); });
$('.filter-mobile-toggle')?.addEventListener('click', e => { const opened = $('.filter-content').classList.toggle('open'); e.currentTarget.setAttribute('aria-expanded', opened); });
const copy = async (value, button, done) => {
  const original = button.textContent;
  try { await navigator.clipboard.writeText(value); button.textContent = done; }
  catch { button.textContent = text('Copy from address bar', '请从地址栏复制'); }
  setTimeout(() => button.textContent = original, 1700);
};
$('.copy-code')?.addEventListener('click', e => copy($('.code-panel code').textContent, e.currentTarget, text('Copied', '已复制')));
document.addEventListener('keydown', e => { if(e.key === '/' && !/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName) && !e.ctrlKey && !e.metaKey) { const input = $('#catalog-search') || $('#home-search'); if(input) {e.preventDefault();input.focus();} } });
if(document.body.dataset.page === 'catalog') {
  const keys = ['q','type','use','modality','openness','form','evidence','runtime','tier','sort','page'];
  let state = {}, data;
  const restore = () => {const params = new URLSearchParams(location.search);state = Object.fromEntries(keys.map(k => [k, params.get(k) || '']));state.page = Math.max(1, Number(state.page) || 1);state.sort ||= 'relevance';};
  const sync = () => {
    const params = new URLSearchParams();
    keys.forEach(k => {if(state[k] && !(k==='sort' && state[k]==='relevance') && !(k==='page' && state[k]===1))params.set(k,state[k]);});
    const query = params.toString();history.replaceState(null,'',location.pathname+(query?'?'+query:''));
    const language = $('[data-language-switch]'); if(language)language.href = language.href.split('?')[0]+(query?'?'+query:'');
    $('#catalog-search').value = state.q;
    $('#sort').value = state.sort;
    $$('[data-filter]').forEach(el => el.value = state[el.dataset.filter]);
    $$('.type-filter').forEach(el => {const active = el.dataset.type === state.type;el.classList.toggle('active',active);el.setAttribute('aria-pressed',active);});
    if(['modality','openness','form','evidence','runtime','tier'].some(k=>state[k]))$('.advanced-filters').open=true;
  };
  const card = r => {
    const state = r.runtime;
    let badge = text('Needs verification','待核验'), style = 'muted';
    if(state.fully_evaluated){badge=text('Evaluated in a listed scope','已在列明范围评测');style='verified';}
    else if(state.smoke_tested){badge=text('Smoke tested','Smoke 已通过');style='verified';}
    else if(r.evidence_level==='primary_source'){badge=text('Primary source checked','一手来源已核验');style='';}
    else if(r.evidence_level==='link_checked')badge=text('Link checked','链接已检查');
    const url = document.body.dataset.base+'resources/'+r.slug+'/';
    return `<article class="resource-row"><div class="resource-symbol" aria-hidden="true">${escapeHTML(r.name[0].toUpperCase())}</div><div class="resource-body"><div class="resource-meta">${escapeHTML(types[r.resource_type][+zh])} <span>·</span> ${escapeHTML(r.publisher)}</div><h3><a href="${url}">${escapeHTML(r.name)}</a></h3><p>${escapeHTML(localized(r.description))}</p><div class="resource-foot"><span class="badge ${style}">${badge}</span><span>${escapeHTML(r.purposes.slice(0,2).map(u=>uses[u][+zh]).join(' · '))}</span></div></div><a class="row-arrow" href="${url}" aria-label="${escapeHTML(r.name)}">↗</a></article>`;
  };
  const matches = r => {
    const words = state.q.toLocaleLowerCase().trim().split(/\s+/).filter(Boolean);
    if(!words.every(w=>r._search.includes(w)))return false;
    const groupedType = state.type==='tools'?['tool','framework']:state.type==='data'?['dataset','benchmark']:state.type?[state.type]:[];
    if(groupedType.length&&!groupedType.includes(r.resource_type))return false;
    if(state.use&&!r.purposes.includes(state.use))return false;
    if(state.modality&&!r.modalities.includes(state.modality))return false;
    if(state.openness&&!r.openness.includes(state.openness))return false;
    if(state.form&&r.service_form!==state.form)return false;
    if(state.evidence&&r.evidence_level!==state.evidence)return false;
    if(state.tier&&r.tier!==state.tier)return false;
    if(state.runtime==='implemented'&&!r.runtime.adapter_implemented)return false;
    if(state.runtime==='smoke'&&!r.runtime.smoke_tested)return false;
    if(state.runtime==='evaluated'&&!r.runtime.fully_evaluated)return false;
    if(state.runtime==='unimplemented'&&r.runtime.adapter_implemented)return false;
    return r.tier!=='excluded';
  };
  const render = (scroll=false) => {
    let records = data.resources.filter(matches);
    if(state.sort==='name')records.sort((a,b)=>a.name.localeCompare(b.name));
    else if(state.sort==='verified')records.sort((a,b)=>(b.verified_on||'').localeCompare(a.verified_on||'')||a.name.localeCompare(b.name));
    const pages = Math.max(1, Math.ceil(records.length/24)); state.page = Math.min(state.page,pages);
    sync();
    $('#result-count').textContent = text(`${records.length.toLocaleString()} resources`,`${records.length.toLocaleString()} 项资源`);
    $('#resource-list').innerHTML = records.slice((state.page-1)*24,state.page*24).map(card).join('');
    $('#empty-state').hidden = records.length!==0;
    $('#pagination').hidden = records.length===0;
    $('#pagination').innerHTML = `<button type="button" data-page-direction="-1" ${state.page===1?'disabled':''}>← ${text('Previous','上一页')}</button><span>${text('Page','第')} ${state.page} / ${pages} ${zh?'页':''}</span><button type="button" data-page-direction="1" ${state.page===pages?'disabled':''}>${text('Next','下一页')} →</button>`;
    $('#active-filters').innerHTML = keys.filter(k=>state[k]&&!['sort','page'].includes(k)).map(k=>{
      let value = state[k];if(k==='type')value=types[value]?.[+zh]||({tools:text('Tools','工具'),data:text('Benchmarks & data','基准与数据')}[value])||value;
      else if(k==='use')value=uses[value]?.[+zh]||value;
      else if(k!=='q')value=$(`[data-filter="${k}"]`)?.selectedOptions[0]?.textContent||value;
      return `<button class="filter-chip" type="button" data-remove-filter="${k}" aria-label="${escapeHTML(text('Remove ','移除筛选：')+value)}">${escapeHTML(value)} <span aria-hidden="true">×</span></button>`;
    }).join('');
    if(scroll)$('.catalog-toolbar').scrollIntoView({behavior:'instant',block:'start'});
  };
  const change = (key,value) => {state[key]=value;state.page=1;render();};
  const clear = () => {state=Object.fromEntries(keys.map(k=>[k,'']));state.page=1;state.sort='relevance';render();};
  restore();
  try {
    const response = await fetch(document.body.dataset.catalogUrl);if(!response.ok)throw new Error('Catalog HTTP '+response.status);
    data=await response.json();
    data.resources.forEach(r=>r._search=[r.name,r.publisher,r.id,...r.aliases,...r.source_record_ids,...r.purposes,...r.purposes.flatMap(u=>uses[u]),r.original_category||'',r.description.en,r.description.zh].join(' ').toLocaleLowerCase());
    render();
    let timer;$('#catalog-search').addEventListener('input', e=>{clearTimeout(timer);timer=setTimeout(()=>change('q',e.target.value),90);});
    $('#sort').addEventListener('change', e=>change('sort',e.target.value));
    $$('[data-filter]').forEach(el=>el.addEventListener('change',()=>change(el.dataset.filter,el.value)));
    $$('.type-filter').forEach(el=>el.addEventListener('click',()=>change('type',el.dataset.type)));
    $$('.clear-filters').forEach(el=>el.addEventListener('click',clear));
    $('#active-filters').addEventListener('click',e=>{const button=e.target.closest('[data-remove-filter]');if(button)change(button.dataset.removeFilter,'');});
    $('#pagination').addEventListener('click',e=>{const button=e.target.closest('[data-page-direction]');if(button){state.page+=Number(button.dataset.pageDirection);render(true);}});
    $('.share-button').addEventListener('click',e=>copy(location.href,e.currentTarget,text('Copied','已复制')));
    window.addEventListener('popstate',()=>{restore();render();});
  } catch(error) {
    $('#result-count').textContent=text('Interactive catalog unavailable. Static resource links remain available. Serve the build over HTTP.','交互目录加载失败；静态资源入口仍可使用。请通过 HTTP 启动构建目录。');
    $('#result-count').dataset.loadError=error.message;
  }
}
