import{s as b}from"./progressbar.esm-DqFWAGu0.js";import{s as y}from"./basecomponent.esm-CrbkcW-f.js";import{B as S,o as t,c as r,m as h,a as e,l as C,q as n,t as B,e as u,b as I,x as g,k as M,F as P,j as z,h as D,y as U,s as $,u as j,v as A}from"./index-DtLmOhiI.js";import{_ as V}from"./_plugin-vue_export-helper-DlAUqK2U.js";var N={root:"p-progress-spinner",spinner:"p-progress-spinner-svg",circle:"p-progress-spinner-circle"},R=S.extend({name:"progressspinner",classes:N}),F={name:"BaseProgressSpinner",extends:y,props:{strokeWidth:{type:String,default:"2"},fill:{type:String,default:"none"},animationDuration:{type:String,default:"2s"}},style:R,provide:function(){return{$parentInstance:this}}},m={name:"ProgressSpinner",extends:F,inheritAttrs:!1,computed:{svgStyle:function(){return{"animation-duration":this.animationDuration}}}},Q=["fill","stroke-width"];function W(s,v,a,l,i,o){return t(),r("div",h({class:s.cx("root"),role:"progressbar"},s.ptmi("root")),[(t(),r("svg",h({class:s.cx("spinner"),viewBox:"25 25 50 50",style:o.svgStyle},s.ptm("spinner")),[e("circle",h({class:s.cx("circle"),cx:"50",cy:"50",r:"20",fill:s.fill,"stroke-width":s.strokeWidth,strokeMiterlimit:"10"},s.ptm("circle")),null,16,Q)],16))],16)}m.render=W;const w=s=>($("data-v-b73f1a56"),s=s(),j(),s),E={class:"container"},H={class:"flex flex-col gap-8 mt-4"},J=w(()=>e("div",{class:"w-full flex-auto flex flex-row border-2 border-solid border-surface-200 dark:border-surface-700 rounded-md bg-[#1e2d4b] font-medium p-4"},[e("div",{class:"app-logo"},[e("svg",{class:"app-icon",width:"64",height:"64",viewBox:"0 0 512 512",version:"1.1",xmlns:"http://www.w3.org/2000/svg","xmlns:xlink":"http://www.w3.org/1999/xlink","xml:space":"preserve","xmlns:serif":"http://www.serif.com/",x:"0px",y:"0px"},[e("g",null,[e("path",{d:"M480,352v48c0,44.1-35.9,80-80,80h-48c-8.8,0-16-7.2-16-16s7.2-16,16-16h48c26.5,0,48-21.5,48-48v-48c0-8.8,7.2-16,16-16S480,343.2,480,352z M400,32h-48c-8.8,0-16,7.2-16,16s7.2,16,16,16h48c26.5,0,48,21.5,48,48v48c0,8.8,7.2,16,16,16s16-7.2,16-16v-48C480,67.9,444.1,32,400,32z M160,448h-48c-26.5,0-48-21.5-48-48v-48c0-8.8-7.2-16-16-16s-16,7.2-16,16v48c0,44.1,35.9,80,80,80h48c8.8,0,16-7.2,16-16S168.8,448,160,448z M160,32h-48c-44.1,0-80,35.9-80,80v48c0,8.8,7.2,16,16,16s16-7.2,16-16v-48c0-26.5,21.5-48,48-48h48c8.8,0,16-7.2,16-16S168.8,32,160,32z",fill:"#fff"}),e("path",{class:"st1",d:"M367.8,356.6c-0.7-28.5-12.5-55.6-32.7-75.6c-5.3-5.4-11.2-10.2-17.5-14.3c11.8-14.2,18.3-32.1,18.3-50.6c0-44.1-35.9-80-80-80s-80,35.9-80,80c0,18.8,6.7,36.5,18.3,50.6c-6.3,4.1-12.1,8.9-17.4,14.2c-21.2,20.9-33,49.5-32.9,79.2c0,8.8,7.2,16,16,16h192.3c8.8,0,16-7.2,16-16C368.2,358.8,368,357.7,367.8,356.6z M255.8,168c26.5,0,48,21.5,48,48c0,26.5-21.5,48-48,48c-8.9,0-17.7-2.5-25.3-7.2l-0.1,0c-14.1-8.7-22.6-24.1-22.6-40.7C207.8,189.5,229.4,168,255.8,168zM177.4,344c3.1-15.4,10.7-29.6,22-40.6c6.1-6.2,13.5-11.5,21.6-15.3c0.4,0.2,0.9,0.4,1.4,0.6c1,0.5,2.1,0.9,3.1,1.3c4.8,2,9.8,3.4,14.8,4.4c2.1,0.4,4.2,0.8,6.4,1.1l0.6,0c2.8,0.3,5.6,0.6,8.5,0.6c2.9,0,5.7-0.3,8.6-0.6c0.2,0,0.3,0,0.5,0c2.2-0.3,4.3-0.6,6.4-1.1c5-1,10-2.5,14.7-4.4c1.1-0.4,2.2-0.8,3.2-1.3c0.4-0.2,0.9-0.4,1.3-0.6c8.1,3.9,15.5,9.2,21.8,15.5c11.1,11,18.7,25.1,21.8,40.5H177.4z",fill:"#2196f3"}),e("path",{class:"st2",d:"M460.2,272H51.8c-9.4,0-17-7.2-17-16s7.6-16,17-16h408.3c9.4,0,17,7.2,17,16S469.5,272,460.2,272z",fill:"#df0000"})])])]),e("div",{class:"flex flex-col w-full"},[e("div",{class:"flex justify-between"},[e("h1",{class:"app-name"},"CrowdQuant"),e("a",{href:"https://support.devdj.pl/issue/new",target:"_blank",class:"lnk-blue"},"Report Issue")]),e("div",{class:"app-details"},[e("div",{class:"app-version"},[e("p",{class:"detail-name"},"Version:"),e("span",{class:"detail-value"},"1.2.0")]),e("div",{class:"app-author pb-4"},[e("p",{class:"detail-name"},"Powered By:"),e("span",{class:"detail-value"},[e("a",{href:"https://devdj.pl",target:"_blank"},"DevDJ")])]),e("div",{class:"build-number"},[e("p",{class:"detail-name"},"Build Number:"),e("span",{class:""},"821525839563")]),e("div",{class:"build-date"},[e("p",{class:"detail-name"},"Build Date:"),e("span",{class:""},"24.05.2024, 12:58:52")]),e("div",{class:"chromium-version"},[e("p",{class:"detail-name"},"Chromium Version:"),e("span",null,"124.0.2478.80")])])])],-1)),T={class:"w-full flex-auto flex flex-col border-2 border-solid border-surface-200 dark:border-surface-700 rounded-md bg-[#1e2d4b] font-medium p-4"},q=w(()=>e("p",{class:"section-title"},"Update",-1)),G={class:"section-content items-center justify-center w-full p-4"},L={key:0,class:"text-base/4 font-bold error-message"},O={key:1,class:"up-to-date"},K={key:3,class:"update-content w-full"},X={class:"update-status-info"},Y={class:"downloading-dots"},Z=U('<div class="section-header w-full" data-v-b73f1a56><h3 class="section-title" data-v-b73f1a56>Update 1.2.0</h3><span class="update-date" data-v-b73f1a56>24.05.2024</span></div><div class="section-content" data-v-b73f1a56><div class="changelog w-full" data-v-b73f1a56><p data-v-b73f1a56>- Added RTSP Recognition</p><p data-v-b73f1a56>- Added Camera Recognition</p><p data-v-b73f1a56>- Integration with DevDJ Api</p><p data-v-b73f1a56>- Integration with CyberSecurity System</p><p data-v-b73f1a56>- Improved GUI changes</p><p data-v-b73f1a56>- Improved Optymalization</p><p data-v-b73f1a56>...</p></div></div>',2),ee={name:"CheckUpdate",components:{ProgressSpinner:m,ProgressBar:b}},se=C({...ee,setup(s){const v=n(!1),a=n(!1),l=n(!1),i=n(""),o=n(0);let d=null;const _=async()=>{a.value=!0;try{const p=await fetch("https://api.devdj.pl/v1/app/update/check?app=CrowdQuant&version=1.2.0");if(p.status===200){const f=p.json();f.status=="out-of-date"?d=setInterval(()=>{let c=o.value+Math.floor(Math.random()*10)+1;c>=100&&(c=100),o.value=c},2e3):(f.status=="up-to-date",a.value=!1),d!==null&&(clearInterval(d),d=null)}else a.value=!0,l.value=!0,i.value="An error occurred while checking for updates."}catch{a.value=!1,l.value=!0,i.value="An error occurred while checking for updates."}},k=A(),x=()=>{k.push("/changelog")};return(p,f)=>(t(),r("div",E,[e("div",H,[J,e("div",T,[e("div",{class:"section-header w-full"},[q,e("button",{class:"lnk-blue",onClick:_},"Check for Updates")]),e("div",G,[l.value?(t(),r("span",L,B(i.value),1)):u("",!0),!v.value&&!a.value&&!l.value?(t(),r("span",O,"CrowdQuant is up to date.")):u("",!0),a.value?(t(),I(g(m),{key:2,class:"checking-spinner",strokeWidth:"4","aria-label":"Checking for Updates"})):u("",!0),v.value?(t(),r("div",K,[e("span",X,[M("Downloading Update"),e("span",Y,[(t(),r(P,null,z(3,c=>e("span",{class:"dot",key:c})),64))])]),D(g(b),{class:"update-progress",value:o.value},null,8,["value"])])):u("",!0)])]),e("div",{class:"update-changelog w-full flex-auto flex flex-col border-2 border-solid border-surface-200 dark:border-surface-700 rounded-md bg-[#131824] font-medium"},[Z,e("div",{class:"section-action-buttons"},[e("button",{class:"lnk-blue btn-small",onClick:x},"Show More")])])])]))}}),oe=V(se,[["__scopeId","data-v-b73f1a56"]]);export{oe as default};
