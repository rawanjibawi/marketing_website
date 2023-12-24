console.log("hello world");
const observer = new IntersectionObserver((entries)=>{
    entries.forEach((entry)=>{
        console.log(entry);
        if(entry.isIntersecting){
            console.log("intersecting");
            entry.target.classList.remove("hide");
            entry.target.classList.add("show");
        }else{
            console.log("not intersecting");
            entry.target.classList.add("hide");
            entry.target.classList.remove("show");
        }
    });
});

const hiddenEelements= document.querySelectorAll('.hide');
console.log(hiddenEelements);
hiddenEelements.forEach((el)=> observer.observe(el));
