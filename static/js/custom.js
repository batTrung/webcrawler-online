$(function(){

	// Folder Tree
	var stopPropagation = function(){
		var a=this.originalEvent;
		this.isPropagationStopped=j,a&&a.stopPropagation&&a.stopPropagation()}

		$(".file-tree li.is-file > span").on("click", function(a){a.stopPropagation()});
		$(".file-tree li.is-folder > span").on("click", function(a){
			$(this).parent("li").find("ul:first").slideToggle(
				400,
				function(){
					$(this).parent("li").toggleClass("open")
				});
			a.stopPropagation()
		});

		
})
