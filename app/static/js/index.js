$(function() {
  moment.locale('zh-cn');
  $('.time').each(function(){
    var timestamp = $(this).find('input').val();
    $(this).html(moment.unix(timestamp).fromNow());
  });
  $('.absoluteTime').each(function(){
    var timestamp = $(this).find('input').val();
    $(this).html(moment.unix(timestamp).format('LL'));
  });
  var loading = false,
    currentPage = 1,
    totalPage = $('.totalPage').val();
  $(window).on('scroll',function(){
    var st = $(document).scrollTop();
  	if(st == $(document).height() - $(window).height()){
      if(loading == false){
        loading = true;
        currentPage += 1;
        if(currentPage <= totalPage){
          $('.loading').slideDown(300);
          setTimeout(function fade1() {
            $('#page' + currentPage).show();
            $('.loading').slideUp(300);
            setTimeout(function fade2() {
              loading = false;
            }, 300);
          }, 1800);
        }
      }
  	}
    if(st > 500){
			if( $('#main-container').length != 0  ){
				var w = $(window).width(),mw = $('#main-container').width();
				if( (w-mw)/2 > 70 )
					$('#go-top').css({'left':(w-mw)/2+mw+20});
				else{
					$('#go-top').css({'left':'auto'});
				}
			}
			$('#go-top').fadeIn(function(){
				$(this).removeClass('dn');
			});
		}
    else{
			$('#go-top').fadeOut(function(){
				$(this).addClass('dn');
			});
		}
	});
  $('#go-top .go').on('click',function(){
		$('html,body').animate({'scrollTop':0},500);
	});
});
