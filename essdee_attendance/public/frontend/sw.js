var Nt=Object.defineProperty,Mt=Object.defineProperties;var Lt=Object.getOwnPropertyDescriptors;var Te=Object.getOwnPropertySymbols;var Pt=Object.prototype.hasOwnProperty,Bt=Object.prototype.propertyIsEnumerable;var Ae=(t,e,n)=>e in t?Nt(t,e,{enumerable:!0,configurable:!0,writable:!0,value:n}):t[e]=n,Re=(t,e)=>{for(var n in e||(e={}))Pt.call(e,n)&&Ae(t,n,e[n]);if(Te)for(var n of Te(e))Bt.call(e,n)&&Ae(t,n,e[n]);return t},ke=(t,e)=>Mt(t,Lt(e));var c=(t,e,n)=>new Promise((r,s)=>{var i=l=>{try{o(n.next(l))}catch(h){s(h)}},a=l=>{try{o(n.throw(l))}catch(h){s(h)}},o=l=>l.done?r(l.value):Promise.resolve(l.value).then(i,a);o((n=n.apply(t,e)).next())});try{self["workbox:core:7.0.0"]&&_()}catch(t){}const Ut=(t,...e)=>{let n=t;return e.length>0&&(n+=` :: ${JSON.stringify(e)}`),n},$t=Ut;class p extends Error{constructor(e,n){const r=$t(e,n);super(r),this.name=e,this.details=n}}const w={googleAnalytics:"googleAnalytics",precache:"precache-v2",prefix:"workbox",runtime:"runtime",suffix:typeof registration!="undefined"?registration.scope:""},J=t=>[w.prefix,t,w.suffix].filter(e=>e&&e.length>0).join("-"),xt=t=>{for(const e of Object.keys(w))t(e)},V={updateDetails:t=>{xt(e=>{typeof t[e]=="string"&&(w[e]=t[e])})},getGoogleAnalyticsName:t=>t||J(w.googleAnalytics),getPrecacheName:t=>t||J(w.precache),getPrefix:()=>w.prefix,getRuntimeName:t=>t||J(w.runtime),getSuffix:()=>w.suffix};function De(t,e){const n=e();return t.waitUntil(n),n}try{self["workbox:precaching:7.0.0"]&&_()}catch(t){}const Ft="__WB_REVISION__";function jt(t){if(!t)throw new p("add-to-cache-list-unexpected-type",{entry:t});if(typeof t=="string"){const i=new URL(t,location.href);return{cacheKey:i.href,url:i.href}}const{revision:e,url:n}=t;if(!n)throw new p("add-to-cache-list-unexpected-type",{entry:t});if(!e){const i=new URL(n,location.href);return{cacheKey:i.href,url:i.href}}const r=new URL(n,location.href),s=new URL(n,location.href);return r.searchParams.set(Ft,e),{cacheKey:r.href,url:s.href}}class Ht{constructor(){this.updatedURLs=[],this.notUpdatedURLs=[],this.handlerWillStart=r=>c(this,[r],function*({request:e,state:n}){n&&(n.originalRequest=e)}),this.cachedResponseWillBeUsed=s=>c(this,[s],function*({event:e,state:n,cachedResponse:r}){if(e.type==="install"&&n&&n.originalRequest&&n.originalRequest instanceof Request){const i=n.originalRequest.url;r?this.notUpdatedURLs.push(i):this.updatedURLs.push(i)}return r})}}class Kt{constructor({precacheController:e}){this.cacheKeyWillBeUsed=s=>c(this,[s],function*({request:n,params:r}){const i=(r==null?void 0:r.cacheKey)||this._precacheController.getCacheKeyForURL(n.url);return i?new Request(i,{headers:n.headers}):n}),this._precacheController=e}}let M;function Vt(){if(M===void 0){const t=new Response("");if("body"in t)try{new Response(t.body),M=!0}catch(e){M=!1}M=!1}return M}function Wt(t,e){return c(this,null,function*(){let n=null;if(t.url&&(n=new URL(t.url).origin),n!==self.location.origin)throw new p("cross-origin-copy-response",{origin:n});const r=t.clone(),i={headers:new Headers(r.headers),status:r.status,statusText:r.statusText},a=Vt()?r.body:yield r.blob();return new Response(a,i)})}const qt=t=>new URL(String(t),location.href).href.replace(new RegExp(`^${location.origin}`),"");function Oe(t,e){const n=new URL(t);for(const r of e)n.searchParams.delete(r);return n.href}function zt(t,e,n,r){return c(this,null,function*(){const s=Oe(e.url,n);if(e.url===s)return t.match(e,r);const i=Object.assign(Object.assign({},r),{ignoreSearch:!0}),a=yield t.keys(e,i);for(const o of a){const l=Oe(o.url,n);if(s===l)return t.match(o,r)}})}let Gt=class{constructor(){this.promise=new Promise((e,n)=>{this.resolve=e,this.reject=n})}};const Jt=new Set;function Yt(){return c(this,null,function*(){for(const t of Jt)yield t()})}function Xt(t){return new Promise(e=>setTimeout(e,t))}try{self["workbox:strategies:7.0.0"]&&_()}catch(t){}function $(t){return typeof t=="string"?new Request(t):t}class Qt{constructor(e,n){this._cacheKeys={},Object.assign(this,n),this.event=n.event,this._strategy=e,this._handlerDeferred=new Gt,this._extendLifetimePromises=[],this._plugins=[...e.plugins],this._pluginStateMap=new Map;for(const r of this._plugins)this._pluginStateMap.set(r,{});this.event.waitUntil(this._handlerDeferred.promise)}fetch(e){return c(this,null,function*(){const{event:n}=this;let r=$(e);if(r.mode==="navigate"&&n instanceof FetchEvent&&n.preloadResponse){const a=yield n.preloadResponse;if(a)return a}const s=this.hasCallback("fetchDidFail")?r.clone():null;try{for(const a of this.iterateCallbacks("requestWillFetch"))r=yield a({request:r.clone(),event:n})}catch(a){if(a instanceof Error)throw new p("plugin-error-request-will-fetch",{thrownErrorMessage:a.message})}const i=r.clone();try{let a;a=yield fetch(r,r.mode==="navigate"?void 0:this._strategy.fetchOptions);for(const o of this.iterateCallbacks("fetchDidSucceed"))a=yield o({event:n,request:i,response:a});return a}catch(a){throw s&&(yield this.runCallbacks("fetchDidFail",{error:a,event:n,originalRequest:s.clone(),request:i.clone()})),a}})}fetchAndCachePut(e){return c(this,null,function*(){const n=yield this.fetch(e),r=n.clone();return this.waitUntil(this.cachePut(e,r)),n})}cacheMatch(e){return c(this,null,function*(){const n=$(e);let r;const{cacheName:s,matchOptions:i}=this._strategy,a=yield this.getCacheKey(n,"read"),o=Object.assign(Object.assign({},i),{cacheName:s});r=yield caches.match(a,o);for(const l of this.iterateCallbacks("cachedResponseWillBeUsed"))r=(yield l({cacheName:s,matchOptions:i,cachedResponse:r,request:a,event:this.event}))||void 0;return r})}cachePut(e,n){return c(this,null,function*(){const r=$(e);yield Xt(0);const s=yield this.getCacheKey(r,"write");if(!n)throw new p("cache-put-with-no-response",{url:qt(s.url)});const i=yield this._ensureResponseSafeToCache(n);if(!i)return!1;const{cacheName:a,matchOptions:o}=this._strategy,l=yield self.caches.open(a),h=this.hasCallback("cacheDidUpdate"),u=h?yield zt(l,s.clone(),["__WB_REVISION__"],o):null;try{yield l.put(s,h?i.clone():i)}catch(d){if(d instanceof Error)throw d.name==="QuotaExceededError"&&(yield Yt()),d}for(const d of this.iterateCallbacks("cacheDidUpdate"))yield d({cacheName:a,oldResponse:u,newResponse:i.clone(),request:s,event:this.event});return!0})}getCacheKey(e,n){return c(this,null,function*(){const r=`${e.url} | ${n}`;if(!this._cacheKeys[r]){let s=e;for(const i of this.iterateCallbacks("cacheKeyWillBeUsed"))s=$(yield i({mode:n,request:s,event:this.event,params:this.params}));this._cacheKeys[r]=s}return this._cacheKeys[r]})}hasCallback(e){for(const n of this._strategy.plugins)if(e in n)return!0;return!1}runCallbacks(e,n){return c(this,null,function*(){for(const r of this.iterateCallbacks(e))yield r(n)})}*iterateCallbacks(e){for(const n of this._strategy.plugins)if(typeof n[e]=="function"){const r=this._pluginStateMap.get(n);yield i=>{const a=Object.assign(Object.assign({},i),{state:r});return n[e](a)}}}waitUntil(e){return this._extendLifetimePromises.push(e),e}doneWaiting(){return c(this,null,function*(){let e;for(;e=this._extendLifetimePromises.shift();)yield e})}destroy(){this._handlerDeferred.resolve(null)}_ensureResponseSafeToCache(e){return c(this,null,function*(){let n=e,r=!1;for(const s of this.iterateCallbacks("cacheWillUpdate"))if(n=(yield s({request:this.request,response:n,event:this.event}))||void 0,r=!0,!n)break;return r||n&&n.status!==200&&(n=void 0),n})}}class Zt{constructor(e={}){this.cacheName=V.getRuntimeName(e.cacheName),this.plugins=e.plugins||[],this.fetchOptions=e.fetchOptions,this.matchOptions=e.matchOptions}handle(e){const[n]=this.handleAll(e);return n}handleAll(e){e instanceof FetchEvent&&(e={event:e,request:e.request});const n=e.event,r=typeof e.request=="string"?new Request(e.request):e.request,s="params"in e?e.params:void 0,i=new Qt(this,{event:n,request:r,params:s}),a=this._getResponse(i,r,n),o=this._awaitComplete(a,i,r,n);return[a,o]}_getResponse(e,n,r){return c(this,null,function*(){yield e.runCallbacks("handlerWillStart",{event:r,request:n});let s;try{if(s=yield this._handle(n,e),!s||s.type==="error")throw new p("no-response",{url:n.url})}catch(i){if(i instanceof Error){for(const a of e.iterateCallbacks("handlerDidError"))if(s=yield a({error:i,event:r,request:n}),s)break}if(!s)throw i}for(const i of e.iterateCallbacks("handlerWillRespond"))s=yield i({event:r,request:n,response:s});return s})}_awaitComplete(e,n,r,s){return c(this,null,function*(){let i,a;try{i=yield e}catch(o){}try{yield n.runCallbacks("handlerDidRespond",{event:s,request:r,response:i}),yield n.doneWaiting()}catch(o){o instanceof Error&&(a=o)}if(yield n.runCallbacks("handlerDidComplete",{event:s,request:r,response:i,error:a}),n.destroy(),a)throw a})}}class v extends Zt{constructor(e={}){e.cacheName=V.getPrecacheName(e.cacheName),super(e),this._fallbackToNetwork=e.fallbackToNetwork!==!1,this.plugins.push(v.copyRedirectedCacheableResponsesPlugin)}_handle(e,n){return c(this,null,function*(){const r=yield n.cacheMatch(e);return r||(n.event&&n.event.type==="install"?yield this._handleInstall(e,n):yield this._handleFetch(e,n))})}_handleFetch(e,n){return c(this,null,function*(){let r;const s=n.params||{};if(this._fallbackToNetwork){const i=s.integrity,a=e.integrity,o=!a||a===i;r=yield n.fetch(new Request(e,{integrity:e.mode!=="no-cors"?a||i:void 0})),i&&o&&e.mode!=="no-cors"&&(this._useDefaultCacheabilityPluginIfNeeded(),yield n.cachePut(e,r.clone()))}else throw new p("missing-precache-entry",{cacheName:this.cacheName,url:e.url});return r})}_handleInstall(e,n){return c(this,null,function*(){this._useDefaultCacheabilityPluginIfNeeded();const r=yield n.fetch(e);if(!(yield n.cachePut(e,r.clone())))throw new p("bad-precaching-response",{url:e.url,status:r.status});return r})}_useDefaultCacheabilityPluginIfNeeded(){let e=null,n=0;for(const[r,s]of this.plugins.entries())s!==v.copyRedirectedCacheableResponsesPlugin&&(s===v.defaultPrecacheCacheabilityPlugin&&(e=r),s.cacheWillUpdate&&n++);n===0?this.plugins.push(v.defaultPrecacheCacheabilityPlugin):n>1&&e!==null&&this.plugins.splice(e,1)}}v.defaultPrecacheCacheabilityPlugin={cacheWillUpdate(e){return c(this,arguments,function*({response:t}){return!t||t.status>=400?null:t})}};v.copyRedirectedCacheableResponsesPlugin={cacheWillUpdate(e){return c(this,arguments,function*({response:t}){return t.redirected?yield Wt(t):t})}};class en{constructor({cacheName:e,plugins:n=[],fallbackToNetwork:r=!0}={}){this._urlsToCacheKeys=new Map,this._urlsToCacheModes=new Map,this._cacheKeysToIntegrities=new Map,this._strategy=new v({cacheName:V.getPrecacheName(e),plugins:[...n,new Kt({precacheController:this})],fallbackToNetwork:r}),this.install=this.install.bind(this),this.activate=this.activate.bind(this)}get strategy(){return this._strategy}precache(e){this.addToCacheList(e),this._installAndActiveListenersAdded||(self.addEventListener("install",this.install),self.addEventListener("activate",this.activate),this._installAndActiveListenersAdded=!0)}addToCacheList(e){const n=[];for(const r of e){typeof r=="string"?n.push(r):r&&r.revision===void 0&&n.push(r.url);const{cacheKey:s,url:i}=jt(r),a=typeof r!="string"&&r.revision?"reload":"default";if(this._urlsToCacheKeys.has(i)&&this._urlsToCacheKeys.get(i)!==s)throw new p("add-to-cache-list-conflicting-entries",{firstEntry:this._urlsToCacheKeys.get(i),secondEntry:s});if(typeof r!="string"&&r.integrity){if(this._cacheKeysToIntegrities.has(s)&&this._cacheKeysToIntegrities.get(s)!==r.integrity)throw new p("add-to-cache-list-conflicting-integrities",{url:i});this._cacheKeysToIntegrities.set(s,r.integrity)}if(this._urlsToCacheKeys.set(i,s),this._urlsToCacheModes.set(i,a),n.length>0){const o=`Workbox is precaching URLs without revision info: ${n.join(", ")}
This is generally NOT safe. Learn more at https://bit.ly/wb-precache`;console.warn(o)}}}install(e){return De(e,()=>c(this,null,function*(){const n=new Ht;this.strategy.plugins.push(n);for(const[i,a]of this._urlsToCacheKeys){const o=this._cacheKeysToIntegrities.get(a),l=this._urlsToCacheModes.get(i),h=new Request(i,{integrity:o,cache:l,credentials:"same-origin"});yield Promise.all(this.strategy.handleAll({params:{cacheKey:a},request:h,event:e}))}const{updatedURLs:r,notUpdatedURLs:s}=n;return{updatedURLs:r,notUpdatedURLs:s}}))}activate(e){return De(e,()=>c(this,null,function*(){const n=yield self.caches.open(this.strategy.cacheName),r=yield n.keys(),s=new Set(this._urlsToCacheKeys.values()),i=[];for(const a of r)s.has(a.url)||(yield n.delete(a),i.push(a.url));return{deletedURLs:i}}))}getURLsToCacheKeys(){return this._urlsToCacheKeys}getCachedURLs(){return[...this._urlsToCacheKeys.keys()]}getCacheKeyForURL(e){const n=new URL(e,location.href);return this._urlsToCacheKeys.get(n.href)}getIntegrityForCacheKey(e){return this._cacheKeysToIntegrities.get(e)}matchPrecache(e){return c(this,null,function*(){const n=e instanceof Request?e.url:e,r=this.getCacheKeyForURL(n);if(r)return(yield self.caches.open(this.strategy.cacheName)).match(r)})}createHandlerBoundToURL(e){const n=this.getCacheKeyForURL(e);if(!n)throw new p("non-precached-url",{url:e});return r=>(r.request=new Request(e),r.params=Object.assign({cacheKey:n},r.params),this.strategy.handle(r))}}let Y;const ze=()=>(Y||(Y=new en),Y);try{self["workbox:routing:7.0.0"]&&_()}catch(t){}const Ge="GET",x=t=>t&&typeof t=="object"?t:{handle:t};class P{constructor(e,n,r=Ge){this.handler=x(n),this.match=e,this.method=r}setCatchHandler(e){this.catchHandler=x(e)}}class tn extends P{constructor(e,n,r){const s=({url:i})=>{const a=e.exec(i.href);if(a&&!(i.origin!==location.origin&&a.index!==0))return a.slice(1)};super(s,n,r)}}class nn{constructor(){this._routes=new Map,this._defaultHandlerMap=new Map}get routes(){return this._routes}addFetchListener(){self.addEventListener("fetch",e=>{const{request:n}=e,r=this.handleRequest({request:n,event:e});r&&e.respondWith(r)})}addCacheListener(){self.addEventListener("message",e=>{if(e.data&&e.data.type==="CACHE_URLS"){const{payload:n}=e.data,r=Promise.all(n.urlsToCache.map(s=>{typeof s=="string"&&(s=[s]);const i=new Request(...s);return this.handleRequest({request:i,event:e})}));e.waitUntil(r),e.ports&&e.ports[0]&&r.then(()=>e.ports[0].postMessage(!0))}})}handleRequest({request:e,event:n}){const r=new URL(e.url,location.href);if(!r.protocol.startsWith("http"))return;const s=r.origin===location.origin,{params:i,route:a}=this.findMatchingRoute({event:n,request:e,sameOrigin:s,url:r});let o=a&&a.handler;const l=e.method;if(!o&&this._defaultHandlerMap.has(l)&&(o=this._defaultHandlerMap.get(l)),!o)return;let h;try{h=o.handle({url:r,request:e,event:n,params:i})}catch(d){h=Promise.reject(d)}const u=a&&a.catchHandler;return h instanceof Promise&&(this._catchHandler||u)&&(h=h.catch(d=>c(this,null,function*(){if(u)try{return yield u.handle({url:r,request:e,event:n,params:i})}catch(m){m instanceof Error&&(d=m)}if(this._catchHandler)return this._catchHandler.handle({url:r,request:e,event:n});throw d}))),h}findMatchingRoute({url:e,sameOrigin:n,request:r,event:s}){const i=this._routes.get(r.method)||[];for(const a of i){let o;const l=a.match({url:e,sameOrigin:n,request:r,event:s});if(l)return o=l,(Array.isArray(o)&&o.length===0||l.constructor===Object&&Object.keys(l).length===0||typeof l=="boolean")&&(o=void 0),{route:a,params:o}}return{}}setDefaultHandler(e,n=Ge){this._defaultHandlerMap.set(n,x(e))}setCatchHandler(e){this._catchHandler=x(e)}registerRoute(e){this._routes.has(e.method)||this._routes.set(e.method,[]),this._routes.get(e.method).push(e)}unregisterRoute(e){if(!this._routes.has(e.method))throw new p("unregister-route-but-not-found-with-method",{method:e.method});const n=this._routes.get(e.method).indexOf(e);if(n>-1)this._routes.get(e.method).splice(n,1);else throw new p("unregister-route-route-not-registered")}}let L;const rn=()=>(L||(L=new nn,L.addFetchListener(),L.addCacheListener()),L);function sn(t,e,n){let r;if(typeof t=="string"){const i=new URL(t,location.href),a=({url:o})=>o.href===i.href;r=new P(a,e,n)}else if(t instanceof RegExp)r=new tn(t,e,n);else if(typeof t=="function")r=new P(t,e,n);else if(t instanceof P)r=t;else throw new p("unsupported-route-type",{moduleName:"workbox-routing",funcName:"registerRoute",paramName:"capture"});return rn().registerRoute(r),r}function an(t,e=[]){for(const n of[...t.searchParams.keys()])e.some(r=>r.test(n))&&t.searchParams.delete(n);return t}function*on(t,{ignoreURLParametersMatching:e=[/^utm_/,/^fbclid$/],directoryIndex:n="index.html",cleanURLs:r=!0,urlManipulation:s}={}){const i=new URL(t,location.href);i.hash="",yield i.href;const a=an(i,e);if(yield a.href,n&&a.pathname.endsWith("/")){const o=new URL(a.href);o.pathname+=n,yield o.href}if(r){const o=new URL(a.href);o.pathname+=".html",yield o.href}if(s){const o=s({url:i});for(const l of o)yield l.href}}class cn extends P{constructor(e,n){const r=({request:s})=>{const i=e.getURLsToCacheKeys();for(const a of on(s.url,n)){const o=i.get(a);if(o){const l=e.getIntegrityForCacheKey(o);return{cacheKey:o,integrity:l}}}};super(r,e.strategy)}}function ln(t){const e=ze(),n=new cn(e,t);sn(n)}const un="-precache-",hn=(n,...r)=>c(void 0,[n,...r],function*(t,e=un){const i=(yield self.caches.keys()).filter(a=>a.includes(e)&&a.includes(self.registration.scope)&&a!==t);return yield Promise.all(i.map(a=>self.caches.delete(a))),i});function dn(){self.addEventListener("activate",t=>{const e=V.getPrecacheName();t.waitUntil(hn(e).then(n=>{}))})}function fn(t){ze().precache(t)}function pn(t,e){fn(t),ln(e)}function gn(){self.addEventListener("activate",()=>self.clients.claim())}var Ne={};/**
 * @license
 * Copyright 2017 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const Je=function(t){const e=[];let n=0;for(let r=0;r<t.length;r++){let s=t.charCodeAt(r);s<128?e[n++]=s:s<2048?(e[n++]=s>>6|192,e[n++]=s&63|128):(s&64512)===55296&&r+1<t.length&&(t.charCodeAt(r+1)&64512)===56320?(s=65536+((s&1023)<<10)+(t.charCodeAt(++r)&1023),e[n++]=s>>18|240,e[n++]=s>>12&63|128,e[n++]=s>>6&63|128,e[n++]=s&63|128):(e[n++]=s>>12|224,e[n++]=s>>6&63|128,e[n++]=s&63|128)}return e},mn=function(t){const e=[];let n=0,r=0;for(;n<t.length;){const s=t[n++];if(s<128)e[r++]=String.fromCharCode(s);else if(s>191&&s<224){const i=t[n++];e[r++]=String.fromCharCode((s&31)<<6|i&63)}else if(s>239&&s<365){const i=t[n++],a=t[n++],o=t[n++],l=((s&7)<<18|(i&63)<<12|(a&63)<<6|o&63)-65536;e[r++]=String.fromCharCode(55296+(l>>10)),e[r++]=String.fromCharCode(56320+(l&1023))}else{const i=t[n++],a=t[n++];e[r++]=String.fromCharCode((s&15)<<12|(i&63)<<6|a&63)}}return e.join("")},Ye={byteToCharMap_:null,charToByteMap_:null,byteToCharMapWebSafe_:null,charToByteMapWebSafe_:null,ENCODED_VALS_BASE:"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",get ENCODED_VALS(){return this.ENCODED_VALS_BASE+"+/="},get ENCODED_VALS_WEBSAFE(){return this.ENCODED_VALS_BASE+"-_."},HAS_NATIVE_SUPPORT:typeof atob=="function",encodeByteArray(t,e){if(!Array.isArray(t))throw Error("encodeByteArray takes an array as a parameter");this.init_();const n=e?this.byteToCharMapWebSafe_:this.byteToCharMap_,r=[];for(let s=0;s<t.length;s+=3){const i=t[s],a=s+1<t.length,o=a?t[s+1]:0,l=s+2<t.length,h=l?t[s+2]:0,u=i>>2,d=(i&3)<<4|o>>4;let m=(o&15)<<2|h>>6,U=h&63;l||(U=64,a||(m=64)),r.push(n[u],n[d],n[m],n[U])}return r.join("")},encodeString(t,e){return this.HAS_NATIVE_SUPPORT&&!e?btoa(t):this.encodeByteArray(Je(t),e)},decodeString(t,e){return this.HAS_NATIVE_SUPPORT&&!e?atob(t):mn(this.decodeStringToByteArray(t,e))},decodeStringToByteArray(t,e){this.init_();const n=e?this.charToByteMapWebSafe_:this.charToByteMap_,r=[];for(let s=0;s<t.length;){const i=n[t.charAt(s++)],o=s<t.length?n[t.charAt(s)]:0;++s;const h=s<t.length?n[t.charAt(s)]:64;++s;const d=s<t.length?n[t.charAt(s)]:64;if(++s,i==null||o==null||h==null||d==null)throw new bn;const m=i<<2|o>>4;if(r.push(m),h!==64){const U=o<<4&240|h>>2;if(r.push(U),d!==64){const Ot=h<<6&192|d;r.push(Ot)}}}return r},init_(){if(!this.byteToCharMap_){this.byteToCharMap_={},this.charToByteMap_={},this.byteToCharMapWebSafe_={},this.charToByteMapWebSafe_={};for(let t=0;t<this.ENCODED_VALS.length;t++)this.byteToCharMap_[t]=this.ENCODED_VALS.charAt(t),this.charToByteMap_[this.byteToCharMap_[t]]=t,this.byteToCharMapWebSafe_[t]=this.ENCODED_VALS_WEBSAFE.charAt(t),this.charToByteMapWebSafe_[this.byteToCharMapWebSafe_[t]]=t,t>=this.ENCODED_VALS_BASE.length&&(this.charToByteMap_[this.ENCODED_VALS_WEBSAFE.charAt(t)]=t,this.charToByteMapWebSafe_[this.ENCODED_VALS.charAt(t)]=t)}}};class bn extends Error{constructor(){super(...arguments),this.name="DecodeBase64StringError"}}const wn=function(t){const e=Je(t);return Ye.encodeByteArray(e,!0)},Xe=function(t){return wn(t).replace(/\./g,"")},yn=function(t){try{return Ye.decodeString(t,!0)}catch(e){console.error("base64Decode failed: ",e)}return null};/**
 * @license
 * Copyright 2022 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function _n(){if(typeof self!="undefined")return self;if(typeof window!="undefined")return window;if(typeof global!="undefined")return global;throw new Error("Unable to locate global object.")}/**
 * @license
 * Copyright 2022 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const In=()=>_n().__FIREBASE_DEFAULTS__,vn=()=>{if(typeof process=="undefined"||typeof Ne=="undefined")return;const t=Ne.__FIREBASE_DEFAULTS__;if(t)return JSON.parse(t)},En=()=>{if(typeof document=="undefined")return;let t;try{t=document.cookie.match(/__FIREBASE_DEFAULTS__=([^;]+)/)}catch(n){return}const e=t&&yn(t[1]);return e&&JSON.parse(e)},Cn=()=>{try{return In()||vn()||En()}catch(t){console.info(`Unable to get __FIREBASE_DEFAULTS__ due to: ${t}`);return}},Qe=()=>{var t;return(t=Cn())===null||t===void 0?void 0:t.config};/**
 * @license
 * Copyright 2017 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */class Sn{constructor(){this.reject=()=>{},this.resolve=()=>{},this.promise=new Promise((e,n)=>{this.resolve=e,this.reject=n})}wrapCallback(e){return(n,r)=>{n?this.reject(n):this.resolve(r),typeof e=="function"&&(this.promise.catch(()=>{}),e.length===1?e(n):e(n,r))}}}function Ze(){try{return typeof indexedDB=="object"}catch(t){return!1}}function et(){return new Promise((t,e)=>{try{let n=!0;const r="validate-browser-context-for-indexeddb-analytics-module",s=self.indexedDB.open(r);s.onsuccess=()=>{s.result.close(),n||self.indexedDB.deleteDatabase(r),t(!0)},s.onupgradeneeded=()=>{n=!1},s.onerror=()=>{var i;e(((i=s.error)===null||i===void 0?void 0:i.message)||"")}}catch(n){e(n)}})}/**
 * @license
 * Copyright 2017 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const Tn="FirebaseError";class N extends Error{constructor(e,n,r){super(n),this.code=e,this.customData=r,this.name=Tn,Object.setPrototypeOf(this,N.prototype),Error.captureStackTrace&&Error.captureStackTrace(this,W.prototype.create)}}class W{constructor(e,n,r){this.service=e,this.serviceName=n,this.errors=r}create(e,...n){const r=n[0]||{},s=`${this.service}/${e}`,i=this.errors[e],a=i?An(i,r):"Error",o=`${this.serviceName}: ${a} (${s}).`;return new N(s,o,r)}}function An(t,e){return t.replace(Rn,(n,r)=>{const s=e[r];return s!=null?String(s):`<${r}?>`})}const Rn=/\{\$([^}]+)}/g;function oe(t,e){if(t===e)return!0;const n=Object.keys(t),r=Object.keys(e);for(const s of n){if(!r.includes(s))return!1;const i=t[s],a=e[s];if(Me(i)&&Me(a)){if(!oe(i,a))return!1}else if(i!==a)return!1}for(const s of r)if(!n.includes(s))return!1;return!0}function Me(t){return t!==null&&typeof t=="object"}/**
 * @license
 * Copyright 2021 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function tt(t){return t&&t._delegate?t._delegate:t}class T{constructor(e,n,r){this.name=e,this.instanceFactory=n,this.type=r,this.multipleInstances=!1,this.serviceProps={},this.instantiationMode="LAZY",this.onInstanceCreated=null}setInstantiationMode(e){return this.instantiationMode=e,this}setMultipleInstances(e){return this.multipleInstances=e,this}setServiceProps(e){return this.serviceProps=e,this}setInstanceCreatedCallback(e){return this.onInstanceCreated=e,this}}/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const C="[DEFAULT]";/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */class kn{constructor(e,n){this.name=e,this.container=n,this.component=null,this.instances=new Map,this.instancesDeferred=new Map,this.instancesOptions=new Map,this.onInitCallbacks=new Map}get(e){const n=this.normalizeInstanceIdentifier(e);if(!this.instancesDeferred.has(n)){const r=new Sn;if(this.instancesDeferred.set(n,r),this.isInitialized(n)||this.shouldAutoInitialize())try{const s=this.getOrInitializeService({instanceIdentifier:n});s&&r.resolve(s)}catch(s){}}return this.instancesDeferred.get(n).promise}getImmediate(e){var n;const r=this.normalizeInstanceIdentifier(e==null?void 0:e.identifier),s=(n=e==null?void 0:e.optional)!==null&&n!==void 0?n:!1;if(this.isInitialized(r)||this.shouldAutoInitialize())try{return this.getOrInitializeService({instanceIdentifier:r})}catch(i){if(s)return null;throw i}else{if(s)return null;throw Error(`Service ${this.name} is not available`)}}getComponent(){return this.component}setComponent(e){if(e.name!==this.name)throw Error(`Mismatching Component ${e.name} for Provider ${this.name}.`);if(this.component)throw Error(`Component for ${this.name} has already been provided`);if(this.component=e,!!this.shouldAutoInitialize()){if(On(e))try{this.getOrInitializeService({instanceIdentifier:C})}catch(n){}for(const[n,r]of this.instancesDeferred.entries()){const s=this.normalizeInstanceIdentifier(n);try{const i=this.getOrInitializeService({instanceIdentifier:s});r.resolve(i)}catch(i){}}}}clearInstance(e=C){this.instancesDeferred.delete(e),this.instancesOptions.delete(e),this.instances.delete(e)}delete(){return c(this,null,function*(){const e=Array.from(this.instances.values());yield Promise.all([...e.filter(n=>"INTERNAL"in n).map(n=>n.INTERNAL.delete()),...e.filter(n=>"_delete"in n).map(n=>n._delete())])})}isComponentSet(){return this.component!=null}isInitialized(e=C){return this.instances.has(e)}getOptions(e=C){return this.instancesOptions.get(e)||{}}initialize(e={}){const{options:n={}}=e,r=this.normalizeInstanceIdentifier(e.instanceIdentifier);if(this.isInitialized(r))throw Error(`${this.name}(${r}) has already been initialized`);if(!this.isComponentSet())throw Error(`Component ${this.name} has not been registered yet`);const s=this.getOrInitializeService({instanceIdentifier:r,options:n});for(const[i,a]of this.instancesDeferred.entries()){const o=this.normalizeInstanceIdentifier(i);r===o&&a.resolve(s)}return s}onInit(e,n){var r;const s=this.normalizeInstanceIdentifier(n),i=(r=this.onInitCallbacks.get(s))!==null&&r!==void 0?r:new Set;i.add(e),this.onInitCallbacks.set(s,i);const a=this.instances.get(s);return a&&e(a,s),()=>{i.delete(e)}}invokeOnInitCallbacks(e,n){const r=this.onInitCallbacks.get(n);if(r)for(const s of r)try{s(e,n)}catch(i){}}getOrInitializeService({instanceIdentifier:e,options:n={}}){let r=this.instances.get(e);if(!r&&this.component&&(r=this.component.instanceFactory(this.container,{instanceIdentifier:Dn(e),options:n}),this.instances.set(e,r),this.instancesOptions.set(e,n),this.invokeOnInitCallbacks(r,e),this.component.onInstanceCreated))try{this.component.onInstanceCreated(this.container,e,r)}catch(s){}return r||null}normalizeInstanceIdentifier(e=C){return this.component?this.component.multipleInstances?e:C:e}shouldAutoInitialize(){return!!this.component&&this.component.instantiationMode!=="EXPLICIT"}}function Dn(t){return t===C?void 0:t}function On(t){return t.instantiationMode==="EAGER"}/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */class Nn{constructor(e){this.name=e,this.providers=new Map}addComponent(e){const n=this.getProvider(e.name);if(n.isComponentSet())throw new Error(`Component ${e.name} has already been registered with ${this.name}`);n.setComponent(e)}addOrOverwriteComponent(e){this.getProvider(e.name).isComponentSet()&&this.providers.delete(e.name),this.addComponent(e)}getProvider(e){if(this.providers.has(e))return this.providers.get(e);const n=new kn(e,this);return this.providers.set(e,n),n}getProviders(){return Array.from(this.providers.values())}}/**
 * @license
 * Copyright 2017 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */var f;(function(t){t[t.DEBUG=0]="DEBUG",t[t.VERBOSE=1]="VERBOSE",t[t.INFO=2]="INFO",t[t.WARN=3]="WARN",t[t.ERROR=4]="ERROR",t[t.SILENT=5]="SILENT"})(f||(f={}));const Mn={debug:f.DEBUG,verbose:f.VERBOSE,info:f.INFO,warn:f.WARN,error:f.ERROR,silent:f.SILENT},Ln=f.INFO,Pn={[f.DEBUG]:"log",[f.VERBOSE]:"log",[f.INFO]:"info",[f.WARN]:"warn",[f.ERROR]:"error"},Bn=(t,e,...n)=>{if(e<t.logLevel)return;const r=new Date().toISOString(),s=Pn[e];if(s)console[s](`[${r}]  ${t.name}:`,...n);else throw new Error(`Attempted to log a message with an invalid logType (value: ${e})`)};class Un{constructor(e){this.name=e,this._logLevel=Ln,this._logHandler=Bn,this._userLogHandler=null}get logLevel(){return this._logLevel}set logLevel(e){if(!(e in f))throw new TypeError(`Invalid value "${e}" assigned to \`logLevel\``);this._logLevel=e}setLogLevel(e){this._logLevel=typeof e=="string"?Mn[e]:e}get logHandler(){return this._logHandler}set logHandler(e){if(typeof e!="function")throw new TypeError("Value assigned to `logHandler` must be a function");this._logHandler=e}get userLogHandler(){return this._userLogHandler}set userLogHandler(e){this._userLogHandler=e}debug(...e){this._userLogHandler&&this._userLogHandler(this,f.DEBUG,...e),this._logHandler(this,f.DEBUG,...e)}log(...e){this._userLogHandler&&this._userLogHandler(this,f.VERBOSE,...e),this._logHandler(this,f.VERBOSE,...e)}info(...e){this._userLogHandler&&this._userLogHandler(this,f.INFO,...e),this._logHandler(this,f.INFO,...e)}warn(...e){this._userLogHandler&&this._userLogHandler(this,f.WARN,...e),this._logHandler(this,f.WARN,...e)}error(...e){this._userLogHandler&&this._userLogHandler(this,f.ERROR,...e),this._logHandler(this,f.ERROR,...e)}}const $n=(t,e)=>e.some(n=>t instanceof n);let Le,Pe;function xn(){return Le||(Le=[IDBDatabase,IDBObjectStore,IDBIndex,IDBCursor,IDBTransaction])}function Fn(){return Pe||(Pe=[IDBCursor.prototype.advance,IDBCursor.prototype.continue,IDBCursor.prototype.continuePrimaryKey])}const nt=new WeakMap,ce=new WeakMap,rt=new WeakMap,X=new WeakMap,pe=new WeakMap;function jn(t){const e=new Promise((n,r)=>{const s=()=>{t.removeEventListener("success",i),t.removeEventListener("error",a)},i=()=>{n(y(t.result)),s()},a=()=>{r(t.error),s()};t.addEventListener("success",i),t.addEventListener("error",a)});return e.then(n=>{n instanceof IDBCursor&&nt.set(n,t)}).catch(()=>{}),pe.set(e,t),e}function Hn(t){if(ce.has(t))return;const e=new Promise((n,r)=>{const s=()=>{t.removeEventListener("complete",i),t.removeEventListener("error",a),t.removeEventListener("abort",a)},i=()=>{n(),s()},a=()=>{r(t.error||new DOMException("AbortError","AbortError")),s()};t.addEventListener("complete",i),t.addEventListener("error",a),t.addEventListener("abort",a)});ce.set(t,e)}let le={get(t,e,n){if(t instanceof IDBTransaction){if(e==="done")return ce.get(t);if(e==="objectStoreNames")return t.objectStoreNames||rt.get(t);if(e==="store")return n.objectStoreNames[1]?void 0:n.objectStore(n.objectStoreNames[0])}return y(t[e])},set(t,e,n){return t[e]=n,!0},has(t,e){return t instanceof IDBTransaction&&(e==="done"||e==="store")?!0:e in t}};function Kn(t){le=t(le)}function Vn(t){return t===IDBDatabase.prototype.transaction&&!("objectStoreNames"in IDBTransaction.prototype)?function(e,...n){const r=t.call(Q(this),e,...n);return rt.set(r,e.sort?e.sort():[e]),y(r)}:Fn().includes(t)?function(...e){return t.apply(Q(this),e),y(nt.get(this))}:function(...e){return y(t.apply(Q(this),e))}}function Wn(t){return typeof t=="function"?Vn(t):(t instanceof IDBTransaction&&Hn(t),$n(t,xn())?new Proxy(t,le):t)}function y(t){if(t instanceof IDBRequest)return jn(t);if(X.has(t))return X.get(t);const e=Wn(t);return e!==t&&(X.set(t,e),pe.set(e,t)),e}const Q=t=>pe.get(t);function q(t,e,{blocked:n,upgrade:r,blocking:s,terminated:i}={}){const a=indexedDB.open(t,e),o=y(a);return r&&a.addEventListener("upgradeneeded",l=>{r(y(a.result),l.oldVersion,l.newVersion,y(a.transaction),l)}),n&&a.addEventListener("blocked",l=>n(l.oldVersion,l.newVersion,l)),o.then(l=>{i&&l.addEventListener("close",()=>i()),s&&l.addEventListener("versionchange",h=>s(h.oldVersion,h.newVersion,h))}).catch(()=>{}),o}function Z(t,{blocked:e}={}){const n=indexedDB.deleteDatabase(t);return e&&n.addEventListener("blocked",r=>e(r.oldVersion,r)),y(n).then(()=>{})}const qn=["get","getKey","getAll","getAllKeys","count"],zn=["put","add","delete","clear"],ee=new Map;function Be(t,e){if(!(t instanceof IDBDatabase&&!(e in t)&&typeof e=="string"))return;if(ee.get(e))return ee.get(e);const n=e.replace(/FromIndex$/,""),r=e!==n,s=zn.includes(n);if(!(n in(r?IDBIndex:IDBObjectStore).prototype)||!(s||qn.includes(n)))return;const i=function(a,...o){return c(this,null,function*(){const l=this.transaction(a,s?"readwrite":"readonly");let h=l.store;return r&&(h=h.index(o.shift())),(yield Promise.all([h[n](...o),s&&l.done]))[0]})};return ee.set(e,i),i}Kn(t=>ke(Re({},t),{get:(e,n,r)=>Be(e,n)||t.get(e,n,r),has:(e,n)=>!!Be(e,n)||t.has(e,n)}));/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */class Gn{constructor(e){this.container=e}getPlatformInfoString(){return this.container.getProviders().map(n=>{if(Jn(n)){const r=n.getImmediate();return`${r.library}/${r.version}`}else return null}).filter(n=>n).join(" ")}}function Jn(t){const e=t.getComponent();return(e==null?void 0:e.type)==="VERSION"}const ue="@firebase/app",Ue="0.10.9";/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const I=new Un("@firebase/app"),Yn="@firebase/app-compat",Xn="@firebase/analytics-compat",Qn="@firebase/analytics",Zn="@firebase/app-check-compat",er="@firebase/app-check",tr="@firebase/auth",nr="@firebase/auth-compat",rr="@firebase/database",sr="@firebase/database-compat",ir="@firebase/functions",ar="@firebase/functions-compat",or="@firebase/installations",cr="@firebase/installations-compat",lr="@firebase/messaging",ur="@firebase/messaging-compat",hr="@firebase/performance",dr="@firebase/performance-compat",fr="@firebase/remote-config",pr="@firebase/remote-config-compat",gr="@firebase/storage",mr="@firebase/storage-compat",br="@firebase/firestore",wr="@firebase/vertexai-preview",yr="@firebase/firestore-compat",_r="firebase";/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const he="[DEFAULT]",Ir={[ue]:"fire-core",[Yn]:"fire-core-compat",[Qn]:"fire-analytics",[Xn]:"fire-analytics-compat",[er]:"fire-app-check",[Zn]:"fire-app-check-compat",[tr]:"fire-auth",[nr]:"fire-auth-compat",[rr]:"fire-rtdb",[sr]:"fire-rtdb-compat",[ir]:"fire-fn",[ar]:"fire-fn-compat",[or]:"fire-iid",[cr]:"fire-iid-compat",[lr]:"fire-fcm",[ur]:"fire-fcm-compat",[hr]:"fire-perf",[dr]:"fire-perf-compat",[fr]:"fire-rc",[pr]:"fire-rc-compat",[gr]:"fire-gcs",[mr]:"fire-gcs-compat",[br]:"fire-fst",[yr]:"fire-fst-compat",[wr]:"fire-vertex","fire-js":"fire-js",[_r]:"fire-js-all"};/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const F=new Map,vr=new Map,de=new Map;function $e(t,e){try{t.container.addComponent(e)}catch(n){I.debug(`Component ${e.name} failed to register with FirebaseApp ${t.name}`,n)}}function O(t){const e=t.name;if(de.has(e))return I.debug(`There were multiple attempts to register component ${e}.`),!1;de.set(e,t);for(const n of F.values())$e(n,t);for(const n of vr.values())$e(n,t);return!0}function ge(t,e){const n=t.container.getProvider("heartbeat").getImmediate({optional:!0});return n&&n.triggerHeartbeat(),t.container.getProvider(e)}/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const Er={"no-app":"No Firebase App '{$appName}' has been created - call initializeApp() first","bad-app-name":"Illegal App name: '{$appName}'","duplicate-app":"Firebase App named '{$appName}' already exists with different options or config","app-deleted":"Firebase App named '{$appName}' already deleted","server-app-deleted":"Firebase Server App has been deleted","no-options":"Need to provide options, when not being deployed to hosting via source.","invalid-app-argument":"firebase.{$appName}() takes either no argument or a Firebase App instance.","invalid-log-argument":"First argument to `onLog` must be null or a function.","idb-open":"Error thrown when opening IndexedDB. Original error: {$originalErrorMessage}.","idb-get":"Error thrown when reading from IndexedDB. Original error: {$originalErrorMessage}.","idb-set":"Error thrown when writing to IndexedDB. Original error: {$originalErrorMessage}.","idb-delete":"Error thrown when deleting from IndexedDB. Original error: {$originalErrorMessage}.","finalization-registry-not-supported":"FirebaseServerApp deleteOnDeref field defined but the JS runtime does not support FinalizationRegistry.","invalid-server-app-environment":"FirebaseServerApp is not for use in browser environments."},E=new W("app","Firebase",Er);/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */class Cr{constructor(e,n,r){this._isDeleted=!1,this._options=Object.assign({},e),this._config=Object.assign({},n),this._name=n.name,this._automaticDataCollectionEnabled=n.automaticDataCollectionEnabled,this._container=r,this.container.addComponent(new T("app",()=>this,"PUBLIC"))}get automaticDataCollectionEnabled(){return this.checkDestroyed(),this._automaticDataCollectionEnabled}set automaticDataCollectionEnabled(e){this.checkDestroyed(),this._automaticDataCollectionEnabled=e}get name(){return this.checkDestroyed(),this._name}get options(){return this.checkDestroyed(),this._options}get config(){return this.checkDestroyed(),this._config}get container(){return this._container}get isDeleted(){return this._isDeleted}set isDeleted(e){this._isDeleted=e}checkDestroyed(){if(this.isDeleted)throw E.create("app-deleted",{appName:this._name})}}function st(t,e={}){let n=t;typeof e!="object"&&(e={name:e});const r=Object.assign({name:he,automaticDataCollectionEnabled:!1},e),s=r.name;if(typeof s!="string"||!s)throw E.create("bad-app-name",{appName:String(s)});if(n||(n=Qe()),!n)throw E.create("no-options");const i=F.get(s);if(i){if(oe(n,i.options)&&oe(r,i.config))return i;throw E.create("duplicate-app",{appName:s})}const a=new Nn(s);for(const l of de.values())a.addComponent(l);const o=new Cr(n,r,a);return F.set(s,o),o}function Sr(t=he){const e=F.get(t);if(!e&&t===he&&Qe())return st();if(!e)throw E.create("no-app",{appName:t});return e}function D(t,e,n){var r;let s=(r=Ir[t])!==null&&r!==void 0?r:t;n&&(s+=`-${n}`);const i=s.match(/\s|\//),a=e.match(/\s|\//);if(i||a){const o=[`Unable to register library "${s}" with version "${e}":`];i&&o.push(`library name "${s}" contains illegal characters (whitespace or "/")`),i&&a&&o.push("and"),a&&o.push(`version name "${e}" contains illegal characters (whitespace or "/")`),I.warn(o.join(" "));return}O(new T(`${s}-version`,()=>({library:s,version:e}),"VERSION"))}/**
 * @license
 * Copyright 2021 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const Tr="firebase-heartbeat-database",Ar=1,B="firebase-heartbeat-store";let te=null;function it(){return te||(te=q(Tr,Ar,{upgrade:(t,e)=>{switch(e){case 0:try{t.createObjectStore(B)}catch(n){console.warn(n)}}}}).catch(t=>{throw E.create("idb-open",{originalErrorMessage:t.message})})),te}function Rr(t){return c(this,null,function*(){try{const n=(yield it()).transaction(B),r=yield n.objectStore(B).get(at(t));return yield n.done,r}catch(e){if(e instanceof N)I.warn(e.message);else{const n=E.create("idb-get",{originalErrorMessage:e==null?void 0:e.message});I.warn(n.message)}}})}function xe(t,e){return c(this,null,function*(){try{const r=(yield it()).transaction(B,"readwrite");yield r.objectStore(B).put(e,at(t)),yield r.done}catch(n){if(n instanceof N)I.warn(n.message);else{const r=E.create("idb-set",{originalErrorMessage:n==null?void 0:n.message});I.warn(r.message)}}})}function at(t){return`${t.name}!${t.options.appId}`}/**
 * @license
 * Copyright 2021 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const kr=1024,Dr=30*24*60*60*1e3;class Or{constructor(e){this.container=e,this._heartbeatsCache=null;const n=this.container.getProvider("app").getImmediate();this._storage=new Mr(n),this._heartbeatsCachePromise=this._storage.read().then(r=>(this._heartbeatsCache=r,r))}triggerHeartbeat(){return c(this,null,function*(){var e,n,r;try{const i=this.container.getProvider("platform-logger").getImmediate().getPlatformInfoString(),a=Fe();return console.log("heartbeats",(e=this._heartbeatsCache)===null||e===void 0?void 0:e.heartbeats),((n=this._heartbeatsCache)===null||n===void 0?void 0:n.heartbeats)==null&&(this._heartbeatsCache=yield this._heartbeatsCachePromise,((r=this._heartbeatsCache)===null||r===void 0?void 0:r.heartbeats)==null)||this._heartbeatsCache.lastSentHeartbeatDate===a||this._heartbeatsCache.heartbeats.some(o=>o.date===a)?void 0:(this._heartbeatsCache.heartbeats.push({date:a,agent:i}),this._heartbeatsCache.heartbeats=this._heartbeatsCache.heartbeats.filter(o=>{const l=new Date(o.date).valueOf();return Date.now()-l<=Dr}),this._storage.overwrite(this._heartbeatsCache))}catch(s){I.warn(s)}})}getHeartbeatsHeader(){return c(this,null,function*(){var e;try{if(this._heartbeatsCache===null&&(yield this._heartbeatsCachePromise),((e=this._heartbeatsCache)===null||e===void 0?void 0:e.heartbeats)==null||this._heartbeatsCache.heartbeats.length===0)return"";const n=Fe(),{heartbeatsToSend:r,unsentEntries:s}=Nr(this._heartbeatsCache.heartbeats),i=Xe(JSON.stringify({version:2,heartbeats:r}));return this._heartbeatsCache.lastSentHeartbeatDate=n,s.length>0?(this._heartbeatsCache.heartbeats=s,yield this._storage.overwrite(this._heartbeatsCache)):(this._heartbeatsCache.heartbeats=[],this._storage.overwrite(this._heartbeatsCache)),i}catch(n){return I.warn(n),""}})}}function Fe(){return new Date().toISOString().substring(0,10)}function Nr(t,e=kr){const n=[];let r=t.slice();for(const s of t){const i=n.find(a=>a.agent===s.agent);if(i){if(i.dates.push(s.date),je(n)>e){i.dates.pop();break}}else if(n.push({agent:s.agent,dates:[s.date]}),je(n)>e){n.pop();break}r=r.slice(1)}return{heartbeatsToSend:n,unsentEntries:r}}class Mr{constructor(e){this.app=e,this._canUseIndexedDBPromise=this.runIndexedDBEnvironmentCheck()}runIndexedDBEnvironmentCheck(){return c(this,null,function*(){return Ze()?et().then(()=>!0).catch(()=>!1):!1})}read(){return c(this,null,function*(){if(yield this._canUseIndexedDBPromise){const n=yield Rr(this.app);return n!=null&&n.heartbeats?n:{heartbeats:[]}}else return{heartbeats:[]}})}overwrite(e){return c(this,null,function*(){var n;if(yield this._canUseIndexedDBPromise){const s=yield this.read();return xe(this.app,{lastSentHeartbeatDate:(n=e.lastSentHeartbeatDate)!==null&&n!==void 0?n:s.lastSentHeartbeatDate,heartbeats:e.heartbeats})}else return})}add(e){return c(this,null,function*(){var n;if(yield this._canUseIndexedDBPromise){const s=yield this.read();return xe(this.app,{lastSentHeartbeatDate:(n=e.lastSentHeartbeatDate)!==null&&n!==void 0?n:s.lastSentHeartbeatDate,heartbeats:[...s.heartbeats,...e.heartbeats]})}else return})}}function je(t){return Xe(JSON.stringify({version:2,heartbeats:t})).length}/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function Lr(t){O(new T("platform-logger",e=>new Gn(e),"PRIVATE")),O(new T("heartbeat",e=>new Or(e),"PRIVATE")),D(ue,Ue,t),D(ue,Ue,"esm2017"),D("fire-js","")}Lr("");var Pr="firebase",Br="10.13.0";/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */D(Pr,Br,"app");const ot="@firebase/installations",me="0.6.8";/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const ct=1e4,lt=`w:${me}`,ut="FIS_v2",Ur="https://firebaseinstallations.googleapis.com/v1",$r=60*60*1e3,xr="installations",Fr="Installations";/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const jr={"missing-app-config-values":'Missing App configuration value: "{$valueName}"',"not-registered":"Firebase Installation is not registered.","installation-not-found":"Firebase Installation not found.","request-failed":'{$requestName} request failed with error "{$serverCode} {$serverStatus}: {$serverMessage}"',"app-offline":"Could not process request. Application offline.","delete-pending-registration":"Can't delete installation while there is a pending registration request."},A=new W(xr,Fr,jr);function ht(t){return t instanceof N&&t.code.includes("request-failed")}/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function dt({projectId:t}){return`${Ur}/projects/${t}/installations`}function ft(t){return{token:t.token,requestStatus:2,expiresIn:Kr(t.expiresIn),creationTime:Date.now()}}function pt(t,e){return c(this,null,function*(){const r=(yield e.json()).error;return A.create("request-failed",{requestName:t,serverCode:r.code,serverMessage:r.message,serverStatus:r.status})})}function gt({apiKey:t}){return new Headers({"Content-Type":"application/json",Accept:"application/json","x-goog-api-key":t})}function Hr(t,{refreshToken:e}){const n=gt(t);return n.append("Authorization",Vr(e)),n}function mt(t){return c(this,null,function*(){const e=yield t();return e.status>=500&&e.status<600?t():e})}function Kr(t){return Number(t.replace("s","000"))}function Vr(t){return`${ut} ${t}`}/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function Wr(r,s){return c(this,arguments,function*({appConfig:t,heartbeatServiceProvider:e},{fid:n}){const i=dt(t),a=gt(t),o=e.getImmediate({optional:!0});if(o){const d=yield o.getHeartbeatsHeader();d&&a.append("x-firebase-client",d)}const l={fid:n,authVersion:ut,appId:t.appId,sdkVersion:lt},h={method:"POST",headers:a,body:JSON.stringify(l)},u=yield mt(()=>fetch(i,h));if(u.ok){const d=yield u.json();return{fid:d.fid||n,registrationStatus:2,refreshToken:d.refreshToken,authToken:ft(d.authToken)}}else throw yield pt("Create Installation",u)})}/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function bt(t){return new Promise(e=>{setTimeout(e,t)})}/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function qr(t){return btoa(String.fromCharCode(...t)).replace(/\+/g,"-").replace(/\//g,"_")}/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const zr=/^[cdef][\w-]{21}$/,fe="";function Gr(){try{const t=new Uint8Array(17);(self.crypto||self.msCrypto).getRandomValues(t),t[0]=112+t[0]%16;const n=Jr(t);return zr.test(n)?n:fe}catch(t){return fe}}function Jr(t){return qr(t).substr(0,22)}/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function z(t){return`${t.appName}!${t.appId}`}/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const wt=new Map;function yt(t,e){const n=z(t);_t(n,e),Yr(n,e)}function _t(t,e){const n=wt.get(t);if(n)for(const r of n)r(e)}function Yr(t,e){const n=Xr();n&&n.postMessage({key:t,fid:e}),Qr()}let S=null;function Xr(){return!S&&"BroadcastChannel"in self&&(S=new BroadcastChannel("[Firebase] FID Change"),S.onmessage=t=>{_t(t.data.key,t.data.fid)}),S}function Qr(){wt.size===0&&S&&(S.close(),S=null)}/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const Zr="firebase-installations-database",es=1,R="firebase-installations-store";let ne=null;function be(){return ne||(ne=q(Zr,es,{upgrade:(t,e)=>{switch(e){case 0:t.createObjectStore(R)}}})),ne}function j(t,e){return c(this,null,function*(){const n=z(t),s=(yield be()).transaction(R,"readwrite"),i=s.objectStore(R),a=yield i.get(n);return yield i.put(e,n),yield s.done,(!a||a.fid!==e.fid)&&yt(t,e.fid),e})}function It(t){return c(this,null,function*(){const e=z(t),r=(yield be()).transaction(R,"readwrite");yield r.objectStore(R).delete(e),yield r.done})}function G(t,e){return c(this,null,function*(){const n=z(t),s=(yield be()).transaction(R,"readwrite"),i=s.objectStore(R),a=yield i.get(n),o=e(a);return o===void 0?yield i.delete(n):yield i.put(o,n),yield s.done,o&&(!a||a.fid!==o.fid)&&yt(t,o.fid),o})}/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function we(t){return c(this,null,function*(){let e;const n=yield G(t.appConfig,r=>{const s=ts(r),i=ns(t,s);return e=i.registrationPromise,i.installationEntry});return n.fid===fe?{installationEntry:yield e}:{installationEntry:n,registrationPromise:e}})}function ts(t){const e=t||{fid:Gr(),registrationStatus:0};return vt(e)}function ns(t,e){if(e.registrationStatus===0){if(!navigator.onLine){const s=Promise.reject(A.create("app-offline"));return{installationEntry:e,registrationPromise:s}}const n={fid:e.fid,registrationStatus:1,registrationTime:Date.now()},r=rs(t,n);return{installationEntry:n,registrationPromise:r}}else return e.registrationStatus===1?{installationEntry:e,registrationPromise:ss(t)}:{installationEntry:e}}function rs(t,e){return c(this,null,function*(){try{const n=yield Wr(t,e);return j(t.appConfig,n)}catch(n){throw ht(n)&&n.customData.serverCode===409?yield It(t.appConfig):yield j(t.appConfig,{fid:e.fid,registrationStatus:0}),n}})}function ss(t){return c(this,null,function*(){let e=yield He(t.appConfig);for(;e.registrationStatus===1;)yield bt(100),e=yield He(t.appConfig);if(e.registrationStatus===0){const{installationEntry:n,registrationPromise:r}=yield we(t);return r||n}return e})}function He(t){return G(t,e=>{if(!e)throw A.create("installation-not-found");return vt(e)})}function vt(t){return is(t)?{fid:t.fid,registrationStatus:0}:t}function is(t){return t.registrationStatus===1&&t.registrationTime+ct<Date.now()}/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function as(r,s){return c(this,arguments,function*({appConfig:t,heartbeatServiceProvider:e},n){const i=os(t,n),a=Hr(t,n),o=e.getImmediate({optional:!0});if(o){const d=yield o.getHeartbeatsHeader();d&&a.append("x-firebase-client",d)}const l={installation:{sdkVersion:lt,appId:t.appId}},h={method:"POST",headers:a,body:JSON.stringify(l)},u=yield mt(()=>fetch(i,h));if(u.ok){const d=yield u.json();return ft(d)}else throw yield pt("Generate Auth Token",u)})}function os(t,{fid:e}){return`${dt(t)}/${e}/authTokens:generate`}/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function ye(t,e=!1){return c(this,null,function*(){let n;const r=yield G(t.appConfig,i=>{if(!Et(i))throw A.create("not-registered");const a=i.authToken;if(!e&&us(a))return i;if(a.requestStatus===1)return n=cs(t,e),i;{if(!navigator.onLine)throw A.create("app-offline");const o=ds(i);return n=ls(t,o),o}});return n?yield n:r.authToken})}function cs(t,e){return c(this,null,function*(){let n=yield Ke(t.appConfig);for(;n.authToken.requestStatus===1;)yield bt(100),n=yield Ke(t.appConfig);const r=n.authToken;return r.requestStatus===0?ye(t,e):r})}function Ke(t){return G(t,e=>{if(!Et(e))throw A.create("not-registered");const n=e.authToken;return fs(n)?Object.assign(Object.assign({},e),{authToken:{requestStatus:0}}):e})}function ls(t,e){return c(this,null,function*(){try{const n=yield as(t,e),r=Object.assign(Object.assign({},e),{authToken:n});return yield j(t.appConfig,r),n}catch(n){if(ht(n)&&(n.customData.serverCode===401||n.customData.serverCode===404))yield It(t.appConfig);else{const r=Object.assign(Object.assign({},e),{authToken:{requestStatus:0}});yield j(t.appConfig,r)}throw n}})}function Et(t){return t!==void 0&&t.registrationStatus===2}function us(t){return t.requestStatus===2&&!hs(t)}function hs(t){const e=Date.now();return e<t.creationTime||t.creationTime+t.expiresIn<e+$r}function ds(t){const e={requestStatus:1,requestTime:Date.now()};return Object.assign(Object.assign({},t),{authToken:e})}function fs(t){return t.requestStatus===1&&t.requestTime+ct<Date.now()}/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function ps(t){return c(this,null,function*(){const e=t,{installationEntry:n,registrationPromise:r}=yield we(e);return r?r.catch(console.error):ye(e).catch(console.error),n.fid})}/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function gs(t,e=!1){return c(this,null,function*(){const n=t;return yield ms(n),(yield ye(n,e)).token})}function ms(t){return c(this,null,function*(){const{registrationPromise:e}=yield we(t);e&&(yield e)})}/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function bs(t){if(!t||!t.options)throw re("App Configuration");if(!t.name)throw re("App Name");const e=["projectId","apiKey","appId"];for(const n of e)if(!t.options[n])throw re(n);return{appName:t.name,projectId:t.options.projectId,apiKey:t.options.apiKey,appId:t.options.appId}}function re(t){return A.create("missing-app-config-values",{valueName:t})}/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const Ct="installations",ws="installations-internal",ys=t=>{const e=t.getProvider("app").getImmediate(),n=bs(e),r=ge(e,"heartbeat");return{app:e,appConfig:n,heartbeatServiceProvider:r,_delete:()=>Promise.resolve()}},_s=t=>{const e=t.getProvider("app").getImmediate(),n=ge(e,Ct).getImmediate();return{getId:()=>ps(n),getToken:s=>gs(n,s)}};function Is(){O(new T(Ct,ys,"PUBLIC")),O(new T(ws,_s,"PRIVATE"))}Is();D(ot,me);D(ot,me,"esm2017");/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const St="BDOU99-h67HcA6JeFXHbSNMu7e2yNNu3RzoMj8TM4W88jITfq7ZmPvIM1Iv-4_l2LxQcYwhqby2xGpWwzjfAnG4",vs="https://fcmregistrations.googleapis.com/v1",Tt="FCM_MSG",Es="google.c.a.c_id",Cs=3,Ss=1;var H;(function(t){t[t.DATA_MESSAGE=1]="DATA_MESSAGE",t[t.DISPLAY_NOTIFICATION=3]="DISPLAY_NOTIFICATION"})(H||(H={}));/**
 * @license
 * Copyright 2018 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
 * in compliance with the License. You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software distributed under the License
 * is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
 * or implied. See the License for the specific language governing permissions and limitations under
 * the License.
 */var K;(function(t){t.PUSH_RECEIVED="push-received",t.NOTIFICATION_CLICKED="notification-clicked"})(K||(K={}));/**
 * @license
 * Copyright 2017 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function b(t){const e=new Uint8Array(t);return btoa(String.fromCharCode(...e)).replace(/=/g,"").replace(/\+/g,"-").replace(/\//g,"_")}function Ts(t){const e="=".repeat((4-t.length%4)%4),n=(t+e).replace(/\-/g,"+").replace(/_/g,"/"),r=atob(n),s=new Uint8Array(r.length);for(let i=0;i<r.length;++i)s[i]=r.charCodeAt(i);return s}/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const se="fcm_token_details_db",As=5,Ve="fcm_token_object_Store";function Rs(t){return c(this,null,function*(){if("databases"in indexedDB&&!(yield indexedDB.databases()).map(i=>i.name).includes(se))return null;let e=null;return(yield q(se,As,{upgrade:(r,s,i,a)=>c(this,null,function*(){var o;if(s<2||!r.objectStoreNames.contains(Ve))return;const l=a.objectStore(Ve),h=yield l.index("fcmSenderId").get(t);if(yield l.clear(),!!h){if(s===2){const u=h;if(!u.auth||!u.p256dh||!u.endpoint)return;e={token:u.fcmToken,createTime:(o=u.createTime)!==null&&o!==void 0?o:Date.now(),subscriptionOptions:{auth:u.auth,p256dh:u.p256dh,endpoint:u.endpoint,swScope:u.swScope,vapidKey:typeof u.vapidKey=="string"?u.vapidKey:b(u.vapidKey)}}}else if(s===3){const u=h;e={token:u.fcmToken,createTime:u.createTime,subscriptionOptions:{auth:b(u.auth),p256dh:b(u.p256dh),endpoint:u.endpoint,swScope:u.swScope,vapidKey:b(u.vapidKey)}}}else if(s===4){const u=h;e={token:u.fcmToken,createTime:u.createTime,subscriptionOptions:{auth:b(u.auth),p256dh:b(u.p256dh),endpoint:u.endpoint,swScope:u.swScope,vapidKey:b(u.vapidKey)}}}}})})).close(),yield Z(se),yield Z("fcm_vapid_details_db"),yield Z("undefined"),ks(e)?e:null})}function ks(t){if(!t||!t.subscriptionOptions)return!1;const{subscriptionOptions:e}=t;return typeof t.createTime=="number"&&t.createTime>0&&typeof t.token=="string"&&t.token.length>0&&typeof e.auth=="string"&&e.auth.length>0&&typeof e.p256dh=="string"&&e.p256dh.length>0&&typeof e.endpoint=="string"&&e.endpoint.length>0&&typeof e.swScope=="string"&&e.swScope.length>0&&typeof e.vapidKey=="string"&&e.vapidKey.length>0}/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const Ds="firebase-messaging-database",Os=1,k="firebase-messaging-store";let ie=null;function _e(){return ie||(ie=q(Ds,Os,{upgrade:(t,e)=>{switch(e){case 0:t.createObjectStore(k)}}})),ie}function Ie(t){return c(this,null,function*(){const e=Ee(t),r=yield(yield _e()).transaction(k).objectStore(k).get(e);if(r)return r;{const s=yield Rs(t.appConfig.senderId);if(s)return yield ve(t,s),s}})}function ve(t,e){return c(this,null,function*(){const n=Ee(t),s=(yield _e()).transaction(k,"readwrite");return yield s.objectStore(k).put(e,n),yield s.done,e})}function Ns(t){return c(this,null,function*(){const e=Ee(t),r=(yield _e()).transaction(k,"readwrite");yield r.objectStore(k).delete(e),yield r.done})}function Ee({appConfig:t}){return t.appId}/**
 * @license
 * Copyright 2017 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const Ms={"missing-app-config-values":'Missing App configuration value: "{$valueName}"',"only-available-in-window":"This method is available in a Window context.","only-available-in-sw":"This method is available in a service worker context.","permission-default":"The notification permission was not granted and dismissed instead.","permission-blocked":"The notification permission was not granted and blocked instead.","unsupported-browser":"This browser doesn't support the API's required to use the Firebase SDK.","indexed-db-unsupported":"This browser doesn't support indexedDb.open() (ex. Safari iFrame, Firefox Private Browsing, etc)","failed-service-worker-registration":"We are unable to register the default service worker. {$browserErrorMessage}","token-subscribe-failed":"A problem occurred while subscribing the user to FCM: {$errorInfo}","token-subscribe-no-token":"FCM returned no token when subscribing the user to push.","token-unsubscribe-failed":"A problem occurred while unsubscribing the user from FCM: {$errorInfo}","token-update-failed":"A problem occurred while updating the user from FCM: {$errorInfo}","token-update-no-token":"FCM returned no token when updating the user to push.","use-sw-after-get-token":"The useServiceWorker() method may only be called once and must be called before calling getToken() to ensure your service worker is used.","invalid-sw-registration":"The input to useServiceWorker() must be a ServiceWorkerRegistration.","invalid-bg-handler":"The input to setBackgroundMessageHandler() must be a function.","invalid-vapid-key":"The public VAPID key must be a string.","use-vapid-key-after-get-token":"The usePublicVapidKey() method may only be called once and must be called before calling getToken() to ensure your VAPID key is used."},g=new W("messaging","Messaging",Ms);/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function Ls(t,e){return c(this,null,function*(){const n=yield Se(t),r=Rt(e),s={method:"POST",headers:n,body:JSON.stringify(r)};let i;try{i=yield(yield fetch(Ce(t.appConfig),s)).json()}catch(a){throw g.create("token-subscribe-failed",{errorInfo:a==null?void 0:a.toString()})}if(i.error){const a=i.error.message;throw g.create("token-subscribe-failed",{errorInfo:a})}if(!i.token)throw g.create("token-subscribe-no-token");return i.token})}function Ps(t,e){return c(this,null,function*(){const n=yield Se(t),r=Rt(e.subscriptionOptions),s={method:"PATCH",headers:n,body:JSON.stringify(r)};let i;try{i=yield(yield fetch(`${Ce(t.appConfig)}/${e.token}`,s)).json()}catch(a){throw g.create("token-update-failed",{errorInfo:a==null?void 0:a.toString()})}if(i.error){const a=i.error.message;throw g.create("token-update-failed",{errorInfo:a})}if(!i.token)throw g.create("token-update-no-token");return i.token})}function At(t,e){return c(this,null,function*(){const r={method:"DELETE",headers:yield Se(t)};try{const i=yield(yield fetch(`${Ce(t.appConfig)}/${e}`,r)).json();if(i.error){const a=i.error.message;throw g.create("token-unsubscribe-failed",{errorInfo:a})}}catch(s){throw g.create("token-unsubscribe-failed",{errorInfo:s==null?void 0:s.toString()})}})}function Ce({projectId:t}){return`${vs}/projects/${t}/registrations`}function Se(n){return c(this,arguments,function*({appConfig:t,installations:e}){const r=yield e.getToken();return new Headers({"Content-Type":"application/json",Accept:"application/json","x-goog-api-key":t.apiKey,"x-goog-firebase-installations-auth":`FIS ${r}`})})}function Rt({p256dh:t,auth:e,endpoint:n,vapidKey:r}){const s={web:{endpoint:n,auth:e,p256dh:t}};return r!==St&&(s.web.applicationPubKey=r),s}/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const Bs=7*24*60*60*1e3;function Us(t){return c(this,null,function*(){const e=yield xs(t.swRegistration,t.vapidKey),n={vapidKey:t.vapidKey,swScope:t.swRegistration.scope,endpoint:e.endpoint,auth:b(e.getKey("auth")),p256dh:b(e.getKey("p256dh"))},r=yield Ie(t.firebaseDependencies);if(r){if(Fs(r.subscriptionOptions,n))return Date.now()>=r.createTime+Bs?$s(t,{token:r.token,createTime:Date.now(),subscriptionOptions:n}):r.token;try{yield At(t.firebaseDependencies,r.token)}catch(s){console.warn(s)}return qe(t.firebaseDependencies,n)}else return qe(t.firebaseDependencies,n)})}function We(t){return c(this,null,function*(){const e=yield Ie(t.firebaseDependencies);e&&(yield At(t.firebaseDependencies,e.token),yield Ns(t.firebaseDependencies));const n=yield t.swRegistration.pushManager.getSubscription();return n?n.unsubscribe():!0})}function $s(t,e){return c(this,null,function*(){try{const n=yield Ps(t.firebaseDependencies,e),r=Object.assign(Object.assign({},e),{token:n,createTime:Date.now()});return yield ve(t.firebaseDependencies,r),n}catch(n){throw n}})}function qe(t,e){return c(this,null,function*(){const r={token:yield Ls(t,e),createTime:Date.now(),subscriptionOptions:e};return yield ve(t,r),r.token})}function xs(t,e){return c(this,null,function*(){const n=yield t.pushManager.getSubscription();return n||t.pushManager.subscribe({userVisibleOnly:!0,applicationServerKey:Ts(e)})})}function Fs(t,e){const n=e.vapidKey===t.vapidKey,r=e.endpoint===t.endpoint,s=e.auth===t.auth,i=e.p256dh===t.p256dh;return n&&r&&s&&i}/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function js(t){const e={from:t.from,collapseKey:t.collapse_key,messageId:t.fcmMessageId};return Hs(e,t),Ks(e,t),Vs(e,t),e}function Hs(t,e){if(!e.notification)return;t.notification={};const n=e.notification.title;n&&(t.notification.title=n);const r=e.notification.body;r&&(t.notification.body=r);const s=e.notification.image;s&&(t.notification.image=s);const i=e.notification.icon;i&&(t.notification.icon=i)}function Ks(t,e){e.data&&(t.data=e.data)}function Vs(t,e){var n,r,s,i,a;if(!e.fcmOptions&&!(!((n=e.notification)===null||n===void 0)&&n.click_action))return;t.fcmOptions={};const o=(s=(r=e.fcmOptions)===null||r===void 0?void 0:r.link)!==null&&s!==void 0?s:(i=e.notification)===null||i===void 0?void 0:i.click_action;o&&(t.fcmOptions.link=o);const l=(a=e.fcmOptions)===null||a===void 0?void 0:a.analytics_label;l&&(t.fcmOptions.analyticsLabel=l)}/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function Ws(t){return typeof t=="object"&&!!t&&Es in t}/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function qs(t){return new Promise(e=>{setTimeout(e,t)})}/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */kt("hts/frbslgigp.ogepscmv/ieo/eaylg","tp:/ieaeogn-agolai.o/1frlglgc/o");kt("AzSCbw63g1R0nCw85jG8","Iaya3yLKwmgvh7cF0q4");function zs(t,e){return c(this,null,function*(){const n=Gs(e,yield t.firebaseDependencies.installations.getId());Js(t,n,e.productId)})}function Gs(t,e){var n,r;const s={};return t.from&&(s.project_number=t.from),t.fcmMessageId&&(s.message_id=t.fcmMessageId),s.instance_id=e,t.notification?s.message_type=H.DISPLAY_NOTIFICATION.toString():s.message_type=H.DATA_MESSAGE.toString(),s.sdk_platform=Cs.toString(),s.package_name=self.origin.replace(/(^\w+:|^)\/\//,""),t.collapse_key&&(s.collapse_key=t.collapse_key),s.event=Ss.toString(),!((n=t.fcmOptions)===null||n===void 0)&&n.analytics_label&&(s.analytics_label=(r=t.fcmOptions)===null||r===void 0?void 0:r.analytics_label),s}function Js(t,e,n){const r={};r.event_time_ms=Math.floor(Date.now()).toString(),r.source_extension_json_proto3=JSON.stringify(e),n&&(r.compliance_data=Ys(n)),t.logEvents.push(r)}function Ys(t){return{privacy_context:{prequest:{origin_associated_product_id:t}}}}function kt(t,e){const n=[];for(let r=0;r<t.length;r++)n.push(t.charAt(r)),r<e.length&&n.push(e.charAt(r));return n.join("")}/**
 * @license
 * Copyright 2017 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function Xs(t,e){return c(this,null,function*(){var n,r;const{newSubscription:s}=t;if(!s){yield We(e);return}const i=yield Ie(e.firebaseDependencies);yield We(e),e.vapidKey=(r=(n=i==null?void 0:i.subscriptionOptions)===null||n===void 0?void 0:n.vapidKey)!==null&&r!==void 0?r:St,yield Us(e)})}function Qs(t,e){return c(this,null,function*(){const n=ti(t);if(!n)return;e.deliveryMetricsExportedToBigQueryEnabled&&(yield zs(e,n));const r=yield Dt();if(ri(r))return si(r,n);if(n.notification&&(yield ii(ei(n))),!!e&&e.onBackgroundMessageHandler){const s=js(n);typeof e.onBackgroundMessageHandler=="function"?yield e.onBackgroundMessageHandler(s):e.onBackgroundMessageHandler.next(s)}})}function Zs(t){return c(this,null,function*(){var e,n;const r=(n=(e=t.notification)===null||e===void 0?void 0:e.data)===null||n===void 0?void 0:n[Tt];if(r){if(t.action)return}else return;t.stopImmediatePropagation(),t.notification.close();const s=ai(r);if(!s)return;const i=new URL(s,self.location.href),a=new URL(self.location.origin);if(i.host!==a.host)return;let o=yield ni(i);if(o?o=yield o.focus():(o=yield self.clients.openWindow(s),yield qs(3e3)),!!o)return r.messageType=K.NOTIFICATION_CLICKED,r.isFirebaseMessaging=!0,o.postMessage(r)})}function ei(t){const e=Object.assign({},t.notification);return e.data={[Tt]:t},e}function ti({data:t}){if(!t)return null;try{return t.json()}catch(e){return null}}function ni(t){return c(this,null,function*(){const e=yield Dt();for(const n of e){const r=new URL(n.url,self.location.href);if(t.host===r.host)return n}return null})}function ri(t){return t.some(e=>e.visibilityState==="visible"&&!e.url.startsWith("chrome-extension://"))}function si(t,e){e.isFirebaseMessaging=!0,e.messageType=K.PUSH_RECEIVED;for(const n of t)n.postMessage(e)}function Dt(){return self.clients.matchAll({type:"window",includeUncontrolled:!0})}function ii(t){var e;const{actions:n}=t,{maxActions:r}=Notification;return n&&r&&n.length>r&&console.warn(`This browser only supports ${r} actions. The remaining actions will not be displayed.`),self.registration.showNotification((e=t.title)!==null&&e!==void 0?e:"",t)}function ai(t){var e,n,r;const s=(n=(e=t.fcmOptions)===null||e===void 0?void 0:e.link)!==null&&n!==void 0?n:(r=t.notification)===null||r===void 0?void 0:r.click_action;return s||(Ws(t.data)?self.location.origin:null)}/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function oi(t){if(!t||!t.options)throw ae("App Configuration Object");if(!t.name)throw ae("App Name");const e=["projectId","apiKey","appId","messagingSenderId"],{options:n}=t;for(const r of e)if(!n[r])throw ae(r);return{appName:t.name,projectId:n.projectId,apiKey:n.apiKey,appId:n.appId,senderId:n.messagingSenderId}}function ae(t){return g.create("missing-app-config-values",{valueName:t})}/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */class ci{constructor(e,n,r){this.deliveryMetricsExportedToBigQueryEnabled=!1,this.onBackgroundMessageHandler=null,this.onMessageHandler=null,this.logEvents=[],this.isLogServiceStarted=!1;const s=oi(e);this.firebaseDependencies={app:e,appConfig:s,installations:n,analyticsProvider:r}}_delete(){return Promise.resolve()}}/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const li=t=>{const e=new ci(t.getProvider("app").getImmediate(),t.getProvider("installations-internal").getImmediate(),t.getProvider("analytics-internal"));return self.addEventListener("push",n=>{n.waitUntil(Qs(n,e))}),self.addEventListener("pushsubscriptionchange",n=>{n.waitUntil(Xs(n,e))}),self.addEventListener("notificationclick",n=>{n.waitUntil(Zs(n))}),e};function ui(){O(new T("messaging-sw",li,"PUBLIC"))}/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function hi(){return c(this,null,function*(){return Ze()&&(yield et())&&"PushManager"in self&&"Notification"in self&&ServiceWorkerRegistration.prototype.hasOwnProperty("showNotification")&&PushSubscription.prototype.hasOwnProperty("getKey")})}/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function di(t,e){if(self.document!==void 0)throw g.create("only-available-in-sw");return t.onBackgroundMessageHandler=e,()=>{t.onBackgroundMessageHandler=null}}/**
 * @license
 * Copyright 2017 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function fi(t=Sr()){return hi().then(e=>{if(!e)throw g.create("unsupported-browser")},e=>{throw g.create("indexed-db-unsupported")}),ge(tt(t),"messaging-sw").getImmediate()}function pi(t,e){return t=tt(t),di(t,e)}/**
 * @license
 * Copyright 2017 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */ui();pn([{"revision":null,"url":"assets/AppSettings-WULxaROV.js"},{"revision":null,"url":"assets/BaseLayout-Db9T0W_r.js"},{"revision":null,"url":"assets/CheckInPanel-C7-pzp7y.js"},{"revision":null,"url":"assets/claims-D-6zPFqc.js"},{"revision":null,"url":"assets/currencies-SJR35BQj.js"},{"revision":null,"url":"assets/CustomIonModal-5G33LXxg.js"},{"revision":null,"url":"assets/Dashboard-B8ldX9GK.js"},{"revision":null,"url":"assets/Dashboard-BMK9eIS7.js"},{"revision":null,"url":"assets/Dashboard-BwUwO-x5.js"},{"revision":null,"url":"assets/Dashboard-CFmyPFzT.js"},{"revision":null,"url":"assets/Detail-CDHfX5zT.js"},{"revision":null,"url":"assets/EmployeeAdvanceBalance-BNlPk1Av.js"},{"revision":null,"url":"assets/EmployeeAdvanceItem-NYnVe_vv.js"},{"revision":null,"url":"assets/EmployeeAvatar-zMm99X4x.js"},{"revision":null,"url":"assets/ExpenseAdvancesTable-CGU7nagf.js"},{"revision":null,"url":"assets/ExpenseClaimItem-DfyQixTZ.js"},{"revision":null,"url":"assets/ExpenseClaimSummary-BeWq8MK4.js"},{"revision":null,"url":"assets/ExpenseItems-DxyJd8cI.js"},{"revision":null,"url":"assets/ExpensesTable-FaK7I2o_.js"},{"revision":null,"url":"assets/ExpenseTaxesTable-CJzn-rjO.js"},{"revision":null,"url":"assets/FileUploaderView-C4tMF-0v.js"},{"revision":null,"url":"assets/FileUploaderView-DrqnjYb4.css"},{"revision":null,"url":"assets/focus-visible-supuXXMI.js"},{"revision":null,"url":"assets/Form-BDiWEqht.js"},{"revision":null,"url":"assets/Form-Cp0W_3fH.js"},{"revision":null,"url":"assets/Form-DVL_nkE0.js"},{"revision":null,"url":"assets/Form-DzMcduP6.js"},{"revision":null,"url":"assets/FormattedField-Dx2k-jzC.js"},{"revision":null,"url":"assets/formatters-Ch330Bw1.js"},{"revision":null,"url":"assets/FormField-7rSNy-En.js"},{"revision":null,"url":"assets/FormView-CS-B2Mga.js"},{"revision":null,"url":"assets/frappe-ui-Be2Kjakw.css"},{"revision":null,"url":"assets/frappe-ui-DZDZpt4w.js"},{"revision":null,"url":"assets/Holidays-KmTMLQWi.js"},{"revision":null,"url":"assets/Home-D4yEmCHE.js"},{"revision":null,"url":"assets/index-BObsDHOH.css"},{"revision":null,"url":"assets/index-BxNz1Obz.js"},{"revision":null,"url":"assets/index9-BChPCECD.js"},{"revision":null,"url":"assets/input-shims-DhYJJN2y.js"},{"revision":null,"url":"assets/InvalidEmployee-CgnbqEES.js"},{"revision":null,"url":"assets/ios.transition-uk4pNZeH.js"},{"revision":null,"url":"assets/LeaveBalance-DM_At4rE.js"},{"revision":null,"url":"assets/LeaveRequestItem-CKxbXhHZ.js"},{"revision":null,"url":"assets/leaves-rPJO3i8A.js"},{"revision":null,"url":"assets/Link-WtJjedfJ.js"},{"revision":null,"url":"assets/List-CbTNuIlK.js"},{"revision":null,"url":"assets/List-ChINSKji.js"},{"revision":null,"url":"assets/List-D4lTQX30.js"},{"revision":null,"url":"assets/List-iHPg9Xfc.js"},{"revision":null,"url":"assets/ListFiltersActionSheet-CICp4Pdf.js"},{"revision":null,"url":"assets/ListView-DrSLrQTT.js"},{"revision":null,"url":"assets/Login-CplK98hV.js"},{"revision":null,"url":"assets/md.transition-CDc9b36N.js"},{"revision":null,"url":"assets/notifications-B1BwxtuP.js"},{"revision":null,"url":"assets/Notifications-qGMxULKM.js"},{"revision":null,"url":"assets/PermissionBalance-CaqQoJLz.js"},{"revision":null,"url":"assets/PermissionListView-CURh9xDq.js"},{"revision":null,"url":"assets/PermissionRequestItem-LV5az5ig.js"},{"revision":null,"url":"assets/PermissionRequestList-D_1G6UfZ.js"},{"revision":null,"url":"assets/PermissionRequestPanel-5g02ng8b.js"},{"revision":null,"url":"assets/permissions-DOYaNnKb.js"},{"revision":null,"url":"assets/Profile-Ca5XWDLJ.js"},{"revision":null,"url":"assets/ProfileInfoModal-C_tKV1BA.js"},{"revision":null,"url":"assets/QuickLinks-DoHwK9eb.js"},{"revision":null,"url":"assets/realtime-BMya6vLA.js"},{"revision":null,"url":"assets/RequestList-xH5hUl5C.js"},{"revision":null,"url":"assets/RequestPanel-Cs-fVcvA.js"},{"revision":null,"url":"assets/requestSummaryFields-CdMCA2LT.js"},{"revision":null,"url":"assets/requestSummaryFields-ZWFfX3pz.css"},{"revision":null,"url":"assets/SalaryDetailTable-3P6Ki1VK.js"},{"revision":null,"url":"assets/SalarySlipItem-B-h-B3rs.js"},{"revision":null,"url":"assets/SemicircleChart-B8MTgycQ.js"},{"revision":null,"url":"assets/status-tap-DlwxxGXU.js"},{"revision":null,"url":"assets/swipe-back-Ds4Z2T8h.js"},{"revision":null,"url":"assets/TabButtons-BKrC3lFY.js"},{"revision":null,"url":"assets/workflow-CgWnsJgA.js"},{"revision":null,"url":"assets/WorkflowActionSheet-CepcMqYJ.css"},{"revision":null,"url":"assets/WorkflowActionSheet-tSPgpAX-.js"},{"revision":"2f97d86dd8bd2c8c822b997a3ac570ad","url":"frappe-push-notification.js"},{"revision":"2e38d96dd227bdc1bfedcac5d3d6cd26","url":"index.html"},{"revision":"b4325950fd0372010e2bcbaf9b746562","url":"manifest.webmanifest"}]);dn();const gi=new URL(location).searchParams.get("config");try{let n=function(){return navigator.userAgent.toLowerCase().includes("chrome")};const t=st(JSON.parse(gi)),e=fi(t);pi(e,r=>{const s=r.data.title;let i={body:r.data.body||""};r.data.notification_icon&&(i.icon=r.data.notification_icon),n()?i.data={url:r.data.click_action}:r.data.click_action&&(i.actions=[{action:r.data.click_action,title:"View Details"}]),self.registration.showNotification(s,i)}),n()&&self.addEventListener("notificationclick",r=>{r.stopImmediatePropagation(),r.notification.close(),r.notification.data&&r.notification.data.url&&clients.openWindow(r.notification.data.url)})}catch(t){console.log("Failed to initialize Firebase",t)}self.skipWaiting();gn();console.log("Service Worker Initialized");
//# sourceMappingURL=sw.js.map
