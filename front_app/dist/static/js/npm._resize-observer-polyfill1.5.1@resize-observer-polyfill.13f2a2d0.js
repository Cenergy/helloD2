(window.webpackJsonp=window.webpackJsonp||[]).push([["npm._resize-observer-polyfill1.5.1@resize-observer-polyfill"],{"0655":function(t,e,n){"use strict";n.r(e),function(t){var n=function(){if("undefined"!=typeof Map)return Map;function t(t,e){var n=-1;return t.some((function(t,i){return t[0]===e&&(n=i,!0)})),n}return Object.defineProperty(e.prototype,"size",{get:function(){return this.__entries__.length},enumerable:!0,configurable:!0}),e.prototype.get=function(e){var n=t(this.__entries__,e),i=this.__entries__[n];return i&&i[1]},e.prototype.set=function(e,n){var i=t(this.__entries__,e);~i?this.__entries__[i][1]=n:this.__entries__.push([e,n])},e.prototype.delete=function(e){var n=this.__entries__,i=t(n,e);~i&&n.splice(i,1)},e.prototype.has=function(e){return!!~t(this.__entries__,e)},e.prototype.clear=function(){this.__entries__.splice(0)},e.prototype.forEach=function(t,e){void 0===e&&(e=null);for(var n=0,i=this.__entries__;n<i.length;n++){var r=i[n];t.call(e,r[1],r[0])}},e;function e(){this.__entries__=[]}}(),i="undefined"!=typeof window&&"undefined"!=typeof document&&window.document===document,r=void 0!==t&&t.Math===Math?t:"undefined"!=typeof self&&self.Math===Math?self:"undefined"!=typeof window&&window.Math===Math?window:Function("return this")(),o="function"==typeof requestAnimationFrame?requestAnimationFrame.bind(r):function(t){return setTimeout((function(){return t(Date.now())}),1e3/60)},s=2,a=["top","right","bottom","left","width","height","size","weight"],c="undefined"!=typeof MutationObserver,h=(u.prototype.addObserver=function(t){~this.observers_.indexOf(t)||this.observers_.push(t),this.connected_||this.connect_()},u.prototype.removeObserver=function(t){var e=this.observers_,n=e.indexOf(t);~n&&e.splice(n,1),!e.length&&this.connected_&&this.disconnect_()},u.prototype.refresh=function(){this.updateObservers_()&&this.refresh()},u.prototype.updateObservers_=function(){var t=this.observers_.filter((function(t){return t.gatherActive(),t.hasActive()}));return t.forEach((function(t){return t.broadcastActive()})),0<t.length},u.prototype.connect_=function(){i&&!this.connected_&&(document.addEventListener("transitionend",this.onTransitionEnd_),window.addEventListener("resize",this.refresh),c?(this.mutationsObserver_=new MutationObserver(this.refresh),this.mutationsObserver_.observe(document,{attributes:!0,childList:!0,characterData:!0,subtree:!0})):(document.addEventListener("DOMSubtreeModified",this.refresh),this.mutationEventsAdded_=!0),this.connected_=!0)},u.prototype.disconnect_=function(){i&&this.connected_&&(document.removeEventListener("transitionend",this.onTransitionEnd_),window.removeEventListener("resize",this.refresh),this.mutationsObserver_&&this.mutationsObserver_.disconnect(),this.mutationEventsAdded_&&document.removeEventListener("DOMSubtreeModified",this.refresh),this.mutationsObserver_=null,this.mutationEventsAdded_=!1,this.connected_=!1)},u.prototype.onTransitionEnd_=function(t){var e=t.propertyName,n=void 0===e?"":e;a.some((function(t){return!!~n.indexOf(t)}))&&this.refresh()},u.getInstance=function(){return this.instance_||(this.instance_=new u),this.instance_},u.instance_=null,u);function u(){function t(){a&&(a=!1,i()),c&&n()}function e(){o(t)}function n(){var t=Date.now();if(a){if(t-h<s)return;c=!0}else c=!(a=!0),setTimeout(e,r);h=t}var i,r,a,c,h;this.connected_=!1,this.mutationEventsAdded_=!1,this.mutationsObserver_=null,this.observers_=[],this.onTransitionEnd_=this.onTransitionEnd_.bind(this),this.refresh=(i=this.refresh.bind(this),c=a=!(r=20),h=0,n)}var f=function(t,e){for(var n=0,i=Object.keys(e);n<i.length;n++){var r=i[n];Object.defineProperty(t,r,{value:e[r],enumerable:!1,writable:!1,configurable:!0})}return t},d=function(t){return t&&t.ownerDocument&&t.ownerDocument.defaultView||r},p=y(0,0,0,0);function v(t){return parseFloat(t)||0}function l(t){for(var e=[],n=1;n<arguments.length;n++)e[n-1]=arguments[n];return e.reduce((function(e,n){return e+v(t["border-"+n+"-width"])}),0)}function _(t){var e=t.clientWidth,n=t.clientHeight;if(!e&&!n)return p;var i,r=d(t).getComputedStyle(t),o=function(t){for(var e={},n=0,i=["top","right","bottom","left"];n<i.length;n++){var r=i[n],o=t["padding-"+r];e[r]=v(o)}return e}(r),s=o.left+o.right,a=o.top+o.bottom,c=v(r.width),h=v(r.height);if("border-box"===r.boxSizing&&(Math.round(c+s)!==e&&(c-=l(r,"left","right")+s),Math.round(h+a)!==n&&(h-=l(r,"top","bottom")+a)),(i=t)!==d(i).document.documentElement){var u=Math.round(c+s)-e,f=Math.round(h+a)-n;1!==Math.abs(u)&&(c-=u),1!==Math.abs(f)&&(h-=f)}return y(o.left,o.top,c,h)}var b="undefined"!=typeof SVGGraphicsElement?function(t){return t instanceof d(t).SVGGraphicsElement}:function(t){return t instanceof d(t).SVGElement&&"function"==typeof t.getBBox};function m(t){return i?b(t)?y(0,0,(e=t.getBBox()).width,e.height):_(t):p;var e}function y(t,e,n,i){return{x:t,y:e,width:n,height:i}}var w=(g.prototype.isActive=function(){var t=m(this.target);return(this.contentRect_=t).width!==this.broadcastWidth||t.height!==this.broadcastHeight},g.prototype.broadcastRect=function(){var t=this.contentRect_;return this.broadcastWidth=t.width,this.broadcastHeight=t.height,t},g);function g(t){this.broadcastWidth=0,this.broadcastHeight=0,this.contentRect_=y(0,0,0,0),this.target=t}var E=function(t,e){var n,i,r,o,s,a,c,h=(i=(n=e).x,r=n.y,o=n.width,s=n.height,a="undefined"!=typeof DOMRectReadOnly?DOMRectReadOnly:Object,c=Object.create(a.prototype),f(c,{x:i,y:r,width:o,height:s,top:r,right:i+o,bottom:s+r,left:i}),c);f(this,{target:t,contentRect:h})},O=(M.prototype.observe=function(t){if(!arguments.length)throw new TypeError("1 argument required, but only 0 present.");if("undefined"!=typeof Element&&Element instanceof Object){if(!(t instanceof d(t).Element))throw new TypeError('parameter 1 is not of type "Element".');var e=this.observations_;e.has(t)||(e.set(t,new w(t)),this.controller_.addObserver(this),this.controller_.refresh())}},M.prototype.unobserve=function(t){if(!arguments.length)throw new TypeError("1 argument required, but only 0 present.");if("undefined"!=typeof Element&&Element instanceof Object){if(!(t instanceof d(t).Element))throw new TypeError('parameter 1 is not of type "Element".');var e=this.observations_;e.has(t)&&(e.delete(t),e.size||this.controller_.removeObserver(this))}},M.prototype.disconnect=function(){this.clearActive(),this.observations_.clear(),this.controller_.removeObserver(this)},M.prototype.gatherActive=function(){var t=this;this.clearActive(),this.observations_.forEach((function(e){e.isActive()&&t.activeObservations_.push(e)}))},M.prototype.broadcastActive=function(){if(this.hasActive()){var t=this.callbackCtx_,e=this.activeObservations_.map((function(t){return new E(t.target,t.broadcastRect())}));this.callback_.call(t,e,t),this.clearActive()}},M.prototype.clearActive=function(){this.activeObservations_.splice(0)},M.prototype.hasActive=function(){return 0<this.activeObservations_.length},M);function M(t,e,i){if(this.activeObservations_=[],this.observations_=new n,"function"!=typeof t)throw new TypeError("The callback provided as parameter 1 is not a function.");this.callback_=t,this.controller_=e,this.callbackCtx_=i}var A="undefined"!=typeof WeakMap?new WeakMap:new n,T=function t(e){if(!(this instanceof t))throw new TypeError("Cannot call a class as a function.");if(!arguments.length)throw new TypeError("1 argument required, but only 0 present.");var n=h.getInstance(),i=new O(e,n,this);A.set(this,i)};["observe","unobserve","disconnect"].forEach((function(t){T.prototype[t]=function(){var e;return(e=A.get(this))[t].apply(e,arguments)}}));var x=void 0!==r.ResizeObserver?r.ResizeObserver:T;e.default=x}.call(this,n("9d8b"))}}]);