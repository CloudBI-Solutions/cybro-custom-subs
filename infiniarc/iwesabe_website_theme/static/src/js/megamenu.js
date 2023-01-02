
$(document).ready(function() {
	$(document).on('click', '.mega-dropdown-menu', function (e) {
		e.stopPropagation();
	});
	
	$(".mega-dropdown-menu .sub-items a").on('click',function (e) {
		$(".mega-dropdown-menu")[0].scrollTop = 0
	});
});