const searchInput=document.getElementById("searchInput");

if(searchInput){

searchInput.addEventListener("keyup",function(){

const value=this.value.toLowerCase();

const rows=document.querySelectorAll("#movieTable tbody tr");

rows.forEach(row=>{

const movie=row.children[1].innerText.toLowerCase();

row.style.display=movie.includes(value)?"":"none";

});

});

}

const cards=document.querySelectorAll(".card");

cards.forEach((card,index)=>{

card.style.opacity="0";

card.style.transform="translateY(40px)";

setTimeout(()=>{

card.style.transition=".6s";

card.style.opacity="1";

card.style.transform="translateY(0)";

},index*150);

});

const rows=document.querySelectorAll("#movieTable tbody tr");

rows.forEach((row,index)=>{

row.style.opacity="0";

row.style.transform="translateX(-20px)";

setTimeout(()=>{

row.style.transition=".5s";

row.style.opacity="1";

row.style.transform="translateX(0)";

},index*100);

});

cards.forEach(card=>{

card.addEventListener("mouseenter",()=>{

card.style.transform="translateY(-8px)";

});

card.addEventListener("mouseleave",()=>{

card.style.transform="translateY(0)";

});

});

const today=document.getElementById("today");

if(today){

today.innerHTML=new Date().toLocaleString("en-US",{

weekday:"long",

month:"long",

day:"numeric",

year:"numeric",

hour:"2-digit",

minute:"2-digit"

});

}

const live=document.querySelector(".status");

if(live){

setInterval(()=>{

live.style.opacity=live.style.opacity==="0.6"?"1":"0.6";

},800);

}

window.addEventListener("load",()=>{

document.body.style.opacity="1";

});

document.querySelectorAll("tbody tr").forEach(row=>{

row.addEventListener("mouseenter",()=>{

row.style.transform="scale(1.01)";

});

row.addEventListener("mouseleave",()=>{

row.style.transform="scale(1)";

});

});

document.querySelectorAll(".sidebar nav a").forEach(link=>{

link.addEventListener("click",()=>{

document.querySelectorAll(".sidebar nav a").forEach(a=>a.classList.remove("active"));

link.classList.add("active");

});

});

console.log("IMDb Dashboard Loaded Successfully");