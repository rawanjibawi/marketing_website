const btns = document.querySelectorAll(".span-container i");
// whenever clicking on the icon, i want to get the id of the product
const addCart = (e) => {
  let product = e.target.dataset.mydata;
  console.log(product);
};
//function should be declared before the addEventListener
btns.forEach(btn=>{
    btn.addEventListener("click", addCart);
})

