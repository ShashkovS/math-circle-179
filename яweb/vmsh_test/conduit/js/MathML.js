function __MathML() {

    // private methods:
    
    // Проверка поддержки MathML браузером (идея позаимствована из пакета jqMath)
    function Supported() {  /* requires document.body */
        // нарисуем невидимую дробь и проверим, что её высота больше чем у простого текста
        var math  = document.createElement('div');
        var plain = document.createElement('div');
        math.innerHTML  = '<math xmlns="http://www.w3.org/1998/Math/MathML">' + 
                          '<mfrac><mn>1</mn><mn>2</mn></mfrac></math>';
        plain.innerHTML = '12';
        var $both = $([math, plain]);
        $both.css('visibility', 'hidden').appendTo(document.body);
		var res = $(math).height() > $(plain).height() + 2;
		$both.remove();
        return res;
	};
    

    // public methods:
    
    this.Frac = function(n, d) {
        return '<math xmlns="http://www.w3.org/1998/Math/MathML">' + 
                   '<mfrac>' + 
                        '<mn>' + n + '</mn>' + 
                        '<mn>' + d + '</mn>' + 
                   '</mfrac>' + 
                   '</math>';
    }

    this.CheckSupport = function() {
        if (!Supported()) {
            $('body').attr('data-MathML-RenderEngine', 'CSS');
        }
    }
}

MathML = new __MathML();