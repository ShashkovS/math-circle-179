function __UploadManager() {

    // private properties:
    var rulersize = 1;
    
    // public properties:
   
    // private methods:
    
    // public methods:

    this.init = function() {
        
        // Общая настройка панелей
        NavBar.init();
        
        var width = localStorage.getItem('XML_WIDTH');
        if (width != null) {
            $('#XML').width(width);
        }
        var height = localStorage.getItem('XML_HEIGHT');
        if (height != null) {
            $('#XML').height(height);
        }
        if (localStorage.getItem('TYPE_LISTOK') != null) {
            $('#type_listok').attr('checked','checked').change();
        }
        
        if(document.getElementById("XML").onscroll.name != '') {
            $('#XML').resizable(
            {
                resize: self.resizeRuler,
                stop:   function() {
                            if (typeof(localStorage) != 'undefined') {
                                localStorage.setItem('XML_WIDTH', $("#XML").width());
                                localStorage.setItem('XML_HEIGHT', $("#XML").height());
                            }
                        },
                handles: 'se'
            });
            $('#Ruler').removeAttr('hidden');
            self.resizeRuler();
            self.scrollRuler();
        } else {
            $('#XML').resizable(
            {
                handles: 'se'
            });
        }
        
        $('#uploadForm').ajaxForm(
        {
            dataType:   'json',
            success:    function(response){
                            if (response.code == 0) { // загрузка прошла успешно
                                $('#XML').val('');
                                // Если загружался список класса, то надо обновить classSelector
                                if ($('#typeSelector input').filter(':checked').val() == 'class') {
                                    $('#classSelector select').append('<option value="'+response.result.value+'">'+response.result.text+'</option>');
                                }
                            }
                            alert(response.message);
                        },
            error:      function(jqXHR, textStatus, errorThrown) {
                            var msg = "Не удалось получить ответ от сервера: ";
                            alert(msg + jqXHR.status + " " + textStatus);
                        }
        });
    }

    this.resizeRuler = function() {
        var $Ruler = $('#Ruler');
        $Ruler.height($('#XML').height());
        // Проверяем, что вся линейка заполнена
        var cur = $Ruler.scrollTop();
        $Ruler.scrollTop(cur + 1);
        while ($Ruler.scrollTop() <= cur) {
            var text = $Ruler.html();
            for(var i = 0; i < 50; i++) {
                text += "<br/>"+(++rulersize);
            }
            $Ruler.html(text).scrollTop(cur + 1);
        }
        $Ruler.scrollTop(cur);
    }
    
    this.scrollRuler = function() {
        var $Ruler = $('#Ruler');
        var desired = $('#XML').scrollTop();
        $Ruler.scrollTop(desired);
        while ($Ruler.scrollTop() < desired) {
            var text = $Ruler.html();
            for(var i = 0; i < 50; i++) {
                text += "<br/>"+(++rulersize);
            }
            $Ruler.html(text).scrollTop(desired);
        }
    }
    
    this.selectClass = function() {
        var ClassSelector = document.getElementById('classSelector').getElementsByTagName('select')[0],
            ClassIdx = ClassSelector.selectedIndex,
            ClassID = ClassSelector.options[ClassIdx].value;
        $.cookie('UploadClass', ClassID, {expires: 30});
    }
    
    this.changeType = function() {
        if (document.getElementById('type_class').checked) {
            $('#classSelector').attr('hidden','hidden');
            localStorage.removeItem('TYPE_LISTOK');
        } else {
            $('#classSelector').removeAttr('hidden');
            localStorage.setItem('TYPE_LISTOK', 1);
        }
    }
    
    // object itself (for access to public methods and properties)
    var self = this;
}

UploadManager = new __UploadManager();