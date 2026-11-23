const fs=require('fs'),vm=require('vm'),assert=require('assert');
const events={},ids={},quiz=[];
class ClassSet{constructor(){this.s=new Set()}toggle(x,on){if(on)this.s.add(x);else this.s.delete(x)}add(x){this.s.add(x)}remove(...xs){xs.forEach(x=>this.s.delete(x))}contains(x){return this.s.has(x)}}
class El{constructor(data={}){this.listeners={};this.classList=new ClassSet();this.attributes={};this.dataset=data;this.style={};this.textContent='';this.disabled=false;this.open=false;this.children={}}addEventListener(n,cb){this.listeners[n]=cb}fire(n,ev={}){if(this.listeners[n])this.listeners[n](ev)}setAttribute(n,v){this.attributes[n]=v}getAttribute(n){return this.attributes[n]}querySelector(n){return this.children[n]}querySelectorAll(n){return this.jump||[]}showModal(){this.open=true}close(){this.open=false}}
const slides=Array.from({length:14},()=>{const o=new El();o.children['.deck-notes']=new El();return o});
for(const x of ['prev','next','counter','bar','progress','notesBtn','outline','outlineBtn','closeDialog'])ids[x]=new El();
ids.outline.jump=Array.from({length:14},(_,i)=>new El({jump:String(i+1)}));
for(let i=0;i<3;i++)quiz.push(new El({correct:i===1?'true':'false'}));
const result=new El();
const document={querySelectorAll(q){if(q==='.slide')return slides;if(q==='.quiz-option')return quiz;return []},getElementById(s){return ids[s]},querySelector(q){if(q==='.quiz-result')return result;return null},addEventListener(n,fn){events[n]=fn}};
const history={replaceState(){}};const location={hash:''};const window={scrollTo(){}};
vm.runInNewContext(fs.readFileSync('assets/deck.js','utf8'),{document,history,location,window,HTMLElement:El,console});
let count=0;function test(msg,fn){fn();count++;console.log('PASS | '+msg)}
test('初始第一頁',()=>assert.equal(ids.counter.textContent,'1 / 14'));
ids.next.fire('click');test('下一頁按鈕',()=>assert.equal(ids.counter.textContent,'2 / 14'));
events.keydown({key:'ArrowRight',target:new El(),preventDefault(){}});test('方向鍵',()=>assert.equal(ids.counter.textContent,'3 / 14'));
ids.outlineBtn.fire('click');test('目錄開啟',()=>assert.equal(ids.outline.open,true));
ids.outline.jump[12].fire('click');test('目錄跳頁',()=>assert.equal(ids.counter.textContent,'13 / 14'));
quiz[1].fire('click');test('問答回饋',()=>assert(result.textContent.includes('答對了')));
ids.notesBtn.fire('click');test('講者筆記切換',()=>assert.equal(ids.notesBtn.attributes['aria-pressed'],'true'));
events.keydown({key:'End',target:new El(),preventDefault(){}});test('End鍵至最後一頁',()=>assert.equal(ids.counter.textContent,'14 / 14'));
events.keydown({key:'Home',target:new El(),preventDefault(){}});test('Home鍵至第一頁',()=>assert.equal(ids.counter.textContent,'1 / 14'));
console.log(`RESULT: ${count}/${count} PASS`);
