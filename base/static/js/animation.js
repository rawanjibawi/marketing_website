const observer = new IntersectionObserver((entries)=>{
    entries.forEach((entry)=>{
        if(entry.isIntersecting){
            entry.target.classList.remove("hide");
            entry.target.classList.add("show");
        }else{
            entry.target.classList.add("hide");
            entry.target.classList.remove("show");
        }
    });
});

const hiddenEelements= document.querySelectorAll('.hide');
hiddenEelements.forEach((el)=> observer.observe(el));
console.log("line 9");