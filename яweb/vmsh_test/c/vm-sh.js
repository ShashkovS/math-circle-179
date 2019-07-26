(function(){

    function Conduit() {
    // private properties:
    var AreaMode = false, AreaCorner, num;
    
    // public properties:
    
    // private methods:
    function MouseOverCell() {
        // Подсвечиваем саму ячейку
        $(this).addClass('mouseOver');
        // Подсвечиваем заголовок строки
        $(this).siblings('.pupilName').addClass('mouseOver');
        // Подсвечиваем заголовок столбца
        $(this).closest('table').find('.headerRow').children(':nth-child('+(this.cellIndex+1)+')').addClass('mouseOver');
    }

    function MouseOverRow() {
        // Подсвечиваем всю строку
        $(this).parent().addClass('mouseOver');
    }

    function MouseOverCol() {
        // Подсвечиваем саму ячейку
        $(this).addClass('mouseOver');
        // Подсвечиваем остальной столбец
        $(this).closest('table').find('tr').children(':nth-child('+(this.cellIndex+1)+')').addClass('mouseOver');
    }

    function MouseUnselect() {
        // Убираем всё выделение, связанное с курсором
        $(this).closest('table').find('*').removeClass('mouseOver');
    }
    
    function SplitProblemName(str) {
        // Разбиваем имя задачи на 2 строки. Если первый символ --- цифра, то вторая строка начнётся с первой нецифры.
        var re = /(^[0-9]+)(?![0-9])(.*$)/;
        var result = re.exec(str);
        if ((result === null) || (result[2] === '')) {
            return str + "<br/>" + "&nbsp;";
        } else {
            return result[1] + "<br/>" + result[2];
        }
    }
    
    
    // Запрашиваем с сервера кондуит
    function LoadConduit($conduit_container, ListID) {
        var ClassID = 1;
        // Запрашиваем содержимое кондуита в формате json
        $.ajax(
        {
            type:   'POST',
            url:    '//www.shashkovs.ru/vmsh_test/c/FillConduit.php',
//            data:   {Class: ClassID, List: 2*ListID-1},
            data:   {Class: ClassID, List: ListID},
            dataType: 'json',
            success: function(json){
                        MakeConduit(json, $conduit_container);
                        // Скрываем заставку и показываем кондуит; делаем заголовочную строку кондуита плавающей
                        //$conduit.css('display','');
                     },
            error:   function(jqXHR, textStatus, errorThrown) {
                        $conduit_container.removeAttr('data-loaded').toggleClass('nodisplay');
                        var msg = 'Не удалось получить ответ от сервера: ';
                        alert(msg);
                     }
        });
    }
    
    function FormatMark(mark) {
        return (mark.length>3)?'+':mark;
    }
    
    // На основе полученных с сервера данных (json) формируем таблицу в её окончательном (почти) виде
    function MakeConduit(data, $conduit_container) {
        var Pupils = data.P, Problems = data.T, Marks = data.M, $hRow, $Row, $Col, PrevGroup, VisitMark;
        var $condTable = $('<table class="conduit"/>'),$colgroup = $('<colgroup/>'),$thead = $('<thead/>'),$tfoot = $('<tfoot/>'),$tbody = $('<tbody/>');
        $condTable.append($colgroup, $thead, $tfoot, $tbody);

                
        // Собираем строку с номерами задач.
        $hRow = $('<tr class="headerRow"/>');
        // Ячейка над списком школьников
        $('<td/>').appendTo($hRow);
        $('<col/>').appendTo($colgroup);
        // Номера задач
        for(var i=1, l=Problems.length; i < l; i++) {
            $('<th scope="col" class="problemName"/>').
                       // Номера задач разбиваем на 2 строки
                       html(SplitProblemName(Problems[i].N)).
                       // Подсветка курсора
                       hover(MouseOverCol, MouseUnselect).
                       appendTo($hRow);
            $Col = $('<col/>', {'data-sign': Problems[i].S});
            if(Problems[i].G != PrevGroup) {
                PrevGroup = Problems[i].G;
                $Col.addClass('problemStart');
            }
            $Col.appendTo($colgroup);
        }
        $hRow.appendTo([$thead, $tfoot]);
        
        // Собираем строки с результатами
        for(var j=0, k=Pupils.length; j < k; j++) {
            // Если школьника не было на занятии, не показываем его совсем
            // VisitMark = Marks[Pupils[j].I + ':' + Problems[0].I];
            // if ((VisitMark === undefined) || (VisitMark.T === '')) {
            //     continue;
            // }
            VisitMark = false;
            $Row = $('<tr/>');
            // Имя школьника
            $('<th scope="row" class="pupilName"/>').
                       html(Pupils[j].S+' '+Pupils[j].N).
                       // Подсветка курсора
                       hover(MouseOverRow, MouseUnselect).
                       appendTo($Row);
            // Сданные задачи
            for(var i=1, l=Problems.length; i < l; i++) {
                Mark = Marks[Pupils[j].I + ':' + Problems[i].I];
                if (Mark === undefined) {
                    Mark = {"T":""};
                }
                if (Mark.T !== "") {
                  VisitMark = true;
                }
                $('<td/>').html(FormatMark(Mark.T)).hover(MouseOverCell, MouseUnselect).appendTo($Row);
            }
            if (VisitMark) {
              $Row.appendTo($tbody);
            }
        }
        $conduit_container.empty();
        $condTable.appendTo($conduit_container);
        $('<img class="spooler_img" src="https://www.shashkovs.ru/vmsh_test/c/up.gif" alt=""/><span class="small_spooler conduit_spooler">Свернуть кондуит</span>').appendTo($conduit_container).on("click", ToggleConduit);
    }

    function ToggleConduit() {
        var $lesson = $(this).closest('.lesson');
        var $conduit_container = $lesson.find('.conduit_container');
        $conduit_container.toggleClass('nodisplay');
        
        if ($conduit_container.attr('data-loaded') !== 'true') {
            $conduit_container.attr('data-loaded', 'true');
            LoadConduit($conduit_container, $lesson.attr('id'));
            $(document).unbind();
        }
    }

    function ToggleSolution() {
        var $lesson = $(this).closest('.lesson');
        var $solution_container = $lesson.find('.solution_container');
        $solution_container.toggleClass('nodisplay');
        
        if ($solution_container.attr('data-loaded') !== 'true') {
            $solution_container.attr('data-loaded', 'true');
            LoadSolution($solution_container, $lesson.attr('id'));
        }
    }

    function LoadSolution($solution_container, ListID) {
        if (ListID.length < 2) {
            ListID = '0'+ListID;
        }
        $.ajax({
                type: 'POST',
                url:  'getdata.php',
                data: {Type: 'solution', Number: ListID},
                dataType: 'html',
                cache:      true,
                success:    function(html){   
                                $solution_container.html(html);   
                                $('<img class="spooler_img" src="//www.shashkovs.ru/vmsh_test/c/up.gif" alt=""/><span class="small_spooler solution_spooler">Свернуть решения</span>').appendTo($solution_container).on("click", ToggleSolution);
                            },
                error:      function(jqXHR, textStatus, errorThrown) {
                                $solution_container.removeAttr('data-loaded').toggleClass('nodisplay');
                                var msg = 'Не удалось загрузить файл с сервера.';
                                alert(msg);
                            }
                });
    }   

    // public methods:
        
    this.init = function() {
        $('.conduit_spooler').on("click", ToggleConduit);
        $('.solution_spooler').on("click", ToggleSolution);
    }
}
window.Conduit = new Conduit();
})();
