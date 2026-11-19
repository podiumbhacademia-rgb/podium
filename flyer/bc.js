// código de barras decorativo
const w=[1,2,1,3,1,1,2,1,4,1,2,1,1,3,2,1,1,2,1,1,3,1,2,2,1,1,4,1,1,2,1,3,1,1,2,1,2,1,1,3,1,2];
document.querySelectorAll('.bc').forEach((el)=>{el.innerHTML=w.map((x,i)=>`<span style="width:${x}px;opacity:${i%7===3?0:1}"></span>`).join('');});
