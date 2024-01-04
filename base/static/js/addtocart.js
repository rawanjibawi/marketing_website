console.log("hello world mr. rawan jibawi");
// whenever clicking on the button, I want to get the id of the product
let updateBtns = document.getElementsByClassName("update-cart");
for (let i = 0; i < updateBtns.length; i++) {
  updateBtns[i].addEventListener("click", function () {
    console.log("welcome home hiys");
    var productId = this.dataset.products; // Corrected from dataset.product to dataset.products
    var action = this.dataset.action;
    console.log(productId);
    console.log(action);
    if(user){
      console.log("truegusyss");
    }else{
      console.log("false guys");

    }
  });
}
