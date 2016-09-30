$(document).ready(function(){
	var code = $(".codemirror-textarea")[0];
	var editor = CodeMirror.fromTextArea(code,{
		lineNumbers : true,
		styleActiveLine : true,
		matchBrackets : true,
		indentUnit : 4,
		tabindex: 4,
		autofocus: true,
		showCursorWhenSelecting: true,
		smartIndent: true,
		addModeClass: true,
		keyMap: 'sublime',
		scrollbarStyle: 'simple',
	});
	editor.setOption("fullScreen", true);
	editor.setSize(700,500);
	editor.setOption("theme","monokai");
	$('#reset').click(function(){
		editor.setValue("");
		$('#input').val("");
		$('#output').val("");
		$("#domain").val('null');
		
	});
	$('#domain').change(function(){
		var mode = $(this).val();		
		editor.setOption("mode",mode.split("|")[0]);
	});
	var mode = $('#domain').val();
	if(mode != null){
		editor.setOption("mode",mode.split("|")[0]);
	}
});