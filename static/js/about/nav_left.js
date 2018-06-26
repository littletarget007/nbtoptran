// JavaScript Document

/*$(function() {
	$('.left_list ul.nav_yi').children('li').click(function(){
		$(this).children('.nav_er').slideToggle().addClass('shang').parent('li').siblings().children('.nav_er').hide(0);
		$(this).find('.nav_san').hide();
	})
	$('.left_list ul.nav_yi li .nva_f1').click(function(e){
		$(this).children('.nav_san').slideToggle();
		e.stopPropagation();
		$('.left_list ul.nav_yi li .nva_f1').css('nva_f1');
	})

})*/
$(function() {
	$('.zuo_yi li dl.zuo_er dd.cur').parent('dl').show();
	$('.zuo_yi li dl.zuo_er dd.cur').parent('dl').siblings('span').addClass('shang').parent('li').siblings().find('span').removeClass('shang');
	$('.zuo_yi li span').click(function(){
		$(this).next('dl').slideToggle().parent('li').siblings().children('dl').slideUp();
		if($(this).hasClass('shang')){
			$(this).removeClass('shang');
		}else{
			$(this).addClass('shang');
			$(this).parent('li').siblings().find('span').removeClass('shang');
		}
	});
	$('.zuo_yi li dl dd.zuo_san').click(function(e){
		$(this).children('.zuo_si').slideToggle();
		if($(this).hasClass('shang')){
			$(this).removeClass('shang');
		}else{
			$(this).addClass('shang');
			$(this).parent('li').siblings().find('span').removeClass('shang');
		}
		e.stopPropagation();
		/*$('.left_list ul.nav_yi li .nva_f1').css('nva_f1');*/
	})

})
