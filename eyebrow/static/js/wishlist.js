$(document).ready(function () {
    //add to wishlist using ajax
$(document).on('click',"#addtowishlist",function() {
    var _vm = $(this);
    var product_id = $(this).attr('pid');


    console.log(product_id+'prod id')


      

    // Ajax
    $.ajax({
        url: '/cart/wishlist/add-to-wishlist',
        data:{
            'id':product_id,
        },
        dataType:'json',
        beforeSend:function() {
            _vm.attr('disabled', true);
        },
        success:function(res){
            console.log(res);
            _vm.attr('disabled', false);           
        }

    });
    // end ajax

});

// end of add to wishlist

// Delete item from wishlist
$(document).on('click',".delete-wish",function(){
    var _pId=$(this).attr('data-item');
    var _vm=$(this);
    console.log(_pId+'jhdskfkjfa')
    //Ajax
    $.ajax({
        url: '/cart/delete-from-wishlist',
        data:{
            'id':_pId,
        },
        dataType:'json',
        beforeSend:function() {
            _vm.attr('disabled', true);
        },
        success:function(res){
            console.log(res);
            _vm.attr('disabled', false);           
        },
        success:function(res){
            $("#cartList").html(res.data);
            console.log(res.data)
        }

    });
    //end ajax
});
// end of delete item
});