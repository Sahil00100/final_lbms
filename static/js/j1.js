
var btn1=document.getElementById('order-btn');
var btn2=document.getElementById('mybtn');
function myfunc(){
    document.getElementById('order-btn').style.display="none";
    document.getElementById('mybtn').style.display="inline";

}

function myfunc2(){
    document.getElementById('order-btn').style.display="inline";
    document.getElementById('mybtn').style.display="none";
    alert('Order Canceled');
}


