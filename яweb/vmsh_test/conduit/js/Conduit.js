function __Conduit() {

    // private properties:
    var Highlight = false;
    var AreaMode = false;
    var AreaCorner;
    var RequestStack = new Array();
    
    // public properties:
    
    // private methods:
    function MouseOverCell() {
        if(AreaMode) {
            var x = this.cellIndex;
            var y = $(this).parent()[0].sectionRowIndex;
            if (x < AreaCorner.x) {
                var Left   = x;
                var Right  = AreaCorner.x;
            } else {
                var Left   = AreaCorner.x;
                var Right  = x;
            }
            if (y < AreaCorner.y) {
                var Top    = y;
                var Bottom = AreaCorner.y;
            } else {
                var Top    = AreaCorner.y;
                var Bottom = y;
            }
            // Посвечиваем заголовки строк и сами ячейки
            $(this).closest('tbody').children().slice(Top, Bottom+1).each(function(){
                $(this).children('.pupilName').addClass('mouseOver').end().children().slice(Left, Right+1).addClass('mouseOver');
            });
            // Посвечиваем заголовки столбцов
            $('.conduit .headerRow').each(function(){
                $(this).children().slice(Left, Right+1).addClass('mouseOver');
            });
        } else {
            // Подсвечиваем заголовок строки и саму ячейку
            $(this).siblings('.pupilName').andSelf().addClass('mouseOver');
            // Подсвечиваем заголовок столбца
            $('.conduit .headerRow').children(':nth-child('+(this.cellIndex+1)+')').addClass('mouseOver');
        }
    }

    function MouseOverRow() {
        // Подсвечиваем всю строку
        $(this).parent().addClass('mouseOver');
    }

    function MouseOverCol() {
        // Подсвечиваем весь столбец
        $('.conduit tr').children(':nth-child('+(this.cellIndex+1)+')').addClass('mouseOver');
    }

    function MouseUnselect() {
        // Убираем всё выделение, связанное с курсором
        $('.conduit *').removeClass('mouseOver');
    }
    
    function String2Frac(s) {
        // преобразуем строку вида 'n/d/r' к виду $\frac{n}{d}$ в нотации MathML
        var slash1 = s.indexOf('/');
        if (slash1 == -1) {
            return s;
        } else {
            var n = s.substr(0, slash1);
            var slash2 = s.indexOf('/', slash1+1);
            if (slash2 == -1) {
                var d = s.substr(slash1+1);
            } else {
                var d = s.substr(slash1+1, slash2-slash1-1);
            }
            return MathML.Frac(n, d);
        }
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
    
    // Добавление в массив Request запроса на обновление ещё одной ячейки
    function Add2Request(Request, X, Y, Mark) {
        var $Table = $('#conduit_container>.conduit');
        Request.push({  Pupil:    $Table.find('tbody tr').eq(Y).attr('data-pupil'),
                        Problem:  $Table.find('.headerRow').eq(0).children().eq(X).attr('data-problem'),
                        Mark:     Mark
                    });
    }

    // Отправка на сервер запроса на обновление значений набора ячеек.
    // Для варианта update запрос передаётся входным параметром; для варианта rollback подтягивается из стека запросов
    function SendRequest(Type, Request) {
        if (Type === 'update') { 
            // Добавляем запрос в стек
            RequestStack.push(Request);
        } else {    
            Request = RequestStack[RequestStack.length-1];
        }
        $.ajax(
        {
            type:   'POST',
            url:    'ajax/UpdateMark.php',
            data:   {Request: JSON.stringify(Request), Type: Type},
            dataType: 'json',
            context: $('#conduit_container>.conduit'),
            success: function(Response){
                        for(var i = 0, l = Response.length; i < l; i++) {
                            var x = $(this).find('.headerRow').eq(0).children('[data-problem="'+Response[i].Problem+'"]')[0].cellIndex;
                            var $Cell = $(this).find('tr[data-pupil="'+Response[i].Pupil+'"]').children().eq(x);
                            $Cell.attr('data-mark', Response[i].Text).html(String2Frac(Response[i].Text));
                            if (Response[i].Amendment !== undefined){
                                $Cell.attr('title', FormatHint(Response[i].Amendment));
                            } else {
                                $Cell.removeAttr('title');
                            }
                            if (Highlight && $('#autoCaption').val() == Response[i].Text) {
                                $Cell.addClass('highlighted');
                            } else {
                                $Cell.removeClass('highlighted');
                            }
                        }
                        if (Type === 'rollback') {
                            // Удаляем запрос из стека запросов
                            RequestStack.pop();
                            if (RequestStack.length === 0) {
                                $('#undoButton').attr('disabled', 'disabled');
                            }
                        } else {
                            $('#undoButton').removeAttr('disabled');
                        }
                     },
            error:   function(jqXHR, textStatus, errorThrown) {
                        var msg = 'Не удалось обновить данные на сервере: ';
                        alert(msg + jqXHR.status + ' ' + textStatus);
                     }
       });
    }
    
    // Откат последнего изменения
    function Undo() {
        if(RequestStack.length > 0) {
            // Отсылаем на сервер запрос об откате последнего запроса
            SendRequest('rollback');
        }
    }
    
    function MouseClickCell(event) {
        // Координаты нажатия (реально область кондуита начинается с точки (1,0))
        var x = this.cellIndex;
        var y = $(this).parent()[0].sectionRowIndex;
        
        // Текущий запрос
        var Request = new Array();
        
        // Метка, которая будет проставляться
        var Mark;
        if(event.altKey) {
            Mark = '';                      // При зажатом ALT производится очистка ячейки/диапазона
        } else {
            Mark = $('#autoCaption').val(); // В обычном режиме проставляется текст из поля "Метка"
        }
        
        if (AreaMode) {                     // Если уже было начато выделение области, то отсылаем метку по всем ячейкам
            if (x < AreaCorner.x) {
                var Left   = x;
                var Right  = AreaCorner.x;
            } else {
                var Left   = AreaCorner.x;
                var Right  = x;
            }
            if (y < AreaCorner.y) {
                var Top    = y;
                var Bottom = AreaCorner.y;
            } else {
                var Top    = AreaCorner.y;
                var Bottom = y;
            }
            for (var i = Left; i <= Right; i++) {
                for (var j = Top; j<= Bottom; j++) {
                    Add2Request(Request, i, j, Mark);
                }
            }
            AreaMode = false;
            delete AreaCorner;
            // Отсылаем запрос на сервер. Он обновит данные в базе и вернёт новое содержимое ячеек.
            SendRequest('update', Request);
        } else if (event.shiftKey) {    // Если нажат SHIFT, стартуем выделение области
            AreaMode = true;
            AreaCorner = {'x':x, 'y':y};
        } else {                        // В противном случае просто отсылаем метку по текущей ячейке
            // Добавляем в запрос единственную ячейку
            Add2Request(Request, x, y, Mark);
            // Отсылаем запрос на сервер. Он обновит данные в базе и вернёт новое содержимое ячеек.
            SendRequest('update', Request);
        }
    }
    
    function SelectClass() {
        var ClassID = SelectedClass();
        
        // Вспоминаем, с каким листком шла работа в этом классе в последний раз
        var key = 'CLASS_' + ClassID;
        var ListID = localStorage.getItem(key);
        if (ListID === null) {
            ListID = 0;
        }
        
        // Подгружаем список листков для выбранного класса
        $.ajax({
            type: 'POST',
            url:  'ajax/FillListSelector.php',
            data: {Class: ClassID, List: ListID},
            dataType: 'html',
            context: $('#listSelector'),
            success: function(response){
                        $(this).html(response);
                        $(this).change();
                     },
            error:   function(jqXHR, textStatus, errorThrown) {
                        $(this).html('');
                        var msg = 'Не удалось получить данные с сервера: ';
                        alert(msg + jqXHR.status + ' ' + textStatus);
                     }
        });
    }

    // Форматируем всплывающую подсказку о последнем изменении
    function FormatHint(Amendment) {
        return 'Последнее изменение: ' + Amendment.U + ', ' + Amendment.T;
    }
    
    // Запрашиваем с сервера кондуит
    function LoadConduit() {
        var ClassID = SelectedClass();
        var ListID = SelectedList();
        var $conduit = $('#conduit_container>.conduit'),
            $loading = $('#loading');
        
        // Если не выбран листок либо класс, то запрос смысла не имеет
        // Это бывает в случае, когда в списке вообще нет ни одного варианта выбора
        if (ClassID === undefined) {
            alert('Нет доступных классов');
            return;
        }
        if (ListID === undefined) {
            alert('Нет доступных листков');
            return;
        }
        
        // Показываем заставку пока ждём ответа от сервера
        $conduit.css('display','none');
        $loading.css('display','');
        
        // Запрашиваем содержимое кондуита в формате json
        $.ajax(
        {
            type:   'POST',
            url:    'ajax/FillConduit.php',
            data:   {Class: ClassID, List: ListID},
            dataType: 'json',
            success: function(json){
                        // Сохраняем выбор пользователя (класс и листок)
                        SaveSelection();
                        // Очищаем стек запросов
                        RequestArray = new Array();
                        $('#undoButton').attr('disabled', 'disabled');
                        //alert(JSON.stringify(json));
                        // Удаляем старую версию таблицы
                        $conduit.remove();
                        // Дешифруем полученный json и формируем окончательный вид таблицы
                        MakeConduit(json);
                        // Скрываем заставку
                        $loading.css('display','none');
                        // Подсвечиваем сегодняшние метки
                        if (Highlight) {
                            AddHighlight();
                        }
                     },
            error:   function(jqXHR, textStatus, errorThrown) {
                        $conduit.empty();
                        var msg = 'Не удалось получить ответ от сервера: ';
                        alert(msg + jqXHR.status + ' ' + textStatus);
                     }
        });
    }
    
    // На основе полученных с сервера данных (json) формируем таблицу в её окончательном (почти) виде
    function MakeConduit(data) {
        var Pupils = data.P;
        var Problems = data.T;
        var Marks = data.M;
        var $hRow, $Col, $Row, $Cell;
        var PrevGroup;
        var $conduit_container = $('#conduit_container');
        
        var $table = $('<table class="conduit"/>'),
            $colgroup = $('<colgroup/>'),
            $thead = $('<thead/>'),
            $tfoot = $('<tfoot/>'),
            $tbody = $('<tbody/>');

        $table.append($colgroup, $thead, $tfoot, $tbody);

        // Собираем строку с номерами задач.
        $hRow = $('<tr class="headerRow"/>');
        // Ячейка над списком школьников
        $('<td/>').appendTo($hRow);
        $('<col/>').appendTo($colgroup);
        // Номера задач
        for(var i=0, l=Problems.length; i < l; i++) {
            $('<th scope="col" class="problemName" data-problem="' + Problems[i].I + '"/>').
                // Номера задач разбиваем на 2 строки
                html(SplitProblemName(Problems[i].N)).
                appendTo($hRow);
            $Col = $('<col data-sign="' + Problems[i].S + '"/>').appendTo($colgroup);
            if(Problems[i].G != PrevGroup) {
                PrevGroup = Problems[i].G;
                $Col.addClass('problemStart');
            }
        }
        $hRow.appendTo([$thead, $tfoot]);
        
        // Собираем строки с результатами
        for(var j=0, k=Pupils.length; j < k; j++) {
            $Row = $('<tr data-pupil="' + Pupils[j].I + '"/>').appendTo($tbody);
            // Имя школьника
            $('<th scope="row" class="pupilName"/>').
                html(Pupils[j].S+' '+Pupils[j].N).
                // Подсветка курсора
                hover(MouseOverRow, MouseUnselect).
                appendTo($Row);
            // Сданные задачи
            for(var i=0, l=Problems.length; i < l; i++) {
                Mark = Marks[Pupils[j].I + ':' + Problems[i].I];
                if (Mark === undefined) {
                    Mark = {"T":""};
                }
                $Cell = $('<td data-mark="' + Mark.T + '"/>').
                            // Отображаем метку по возможности в виде дроби
                            html(String2Frac(Mark.T)).
                            // Подсветка курсора
                            hover(MouseOverCell, MouseUnselect).
                            // Обработка клика мышью
                            click(MouseClickCell).
                            appendTo($Row);
                if (Mark.A !== undefined){
                    $Cell.attr('title', FormatHint(Mark.A));
                }
            }
        }
        // Вставляем таблицу на место и приделываем к ней плавающую шапку
        $table.appendTo($conduit_container).floatHeader({fadeIn: 0, fadeOut: 0});
        // Для всех заголоков столбцов (в том числе пока не созданных в плавающей шапке) устанавливаем обработку hover
        $conduit_container.on({'mouseover': MouseOverCol, 'mouseout': MouseUnselect}, '.conduit .problemName');
    }

    function AddHighlight() {
        var mark = $('#autoCaption').val();
        $('.conduit td').filter(function(index) {
                                    return (mark === $(this).attr('data-mark'));
                                }).addClass('highlighted');
    }

    function RemoveHighlight() {
        $('.conduit td').removeClass('highlighted');
    }
    
    function SelectedClass() {
        return $('#classSelector option').filter(':selected').val();
    }

    function SelectedList() {
        return $('#listSelector option').filter(':selected').val();
    }
    
    function SaveSelection() {
        var ClassID = SelectedClass();
        var ListID = SelectedList();
        
        // сохраняем последние класс и листок в cookie
        $.cookie('Class', ClassID, {expires: 30});
        $.cookie('List', ListID, {expires: 30});
        
        // Сохраняем, с каким листком идёт работа в этом классе в localStorage
        var key = 'CLASS_' + ClassID;
        localStorage.setItem(key, ListID);
    }
	
    function HM_checked() {
        Highlight = $('#HM_CB')[0].checked;
        if (Highlight) {
            localStorage.setItem('HM_CHECKED', '1');
            AddHighlight();
        } else {
            localStorage.removeItem('HM_CHECKED');
            RemoveHighlight();
        }
    }
    
    function Mark_changed() {
        if (Highlight) {
            RemoveHighlight();
            AddHighlight();
        }
    }   

	// public methods:

    this.onkey = function(e) {
        var keychar = String.fromCharCode(e.which);
        if (e.ctrlKey && keychar === 'Z') {
            Undo();
        } else if (e.which === 27){     // Escape
            AreaMode = false;
            delete AreaCorner;
            MouseUnselect();
        }
    }
        
    this.init = function() {
        
        // Если MathML не поддерживается непосредственно браузером, подключаем CSS-эмулятор
        MathML.CheckSupport();
        
        // Общая настройка панелей
        NavBar.init();
        ToolBar.init();
        
        // Настраиваем выпадающие списки
        $('#classSelector').change(SelectClass);
        $('#listSelector').change(LoadConduit);
        
        // Настраиваем чекбоксы
		$('#HM_CB').change(HM_checked);
        if (localStorage.getItem('HM_CHECKED') != null) {
            $('#HM_CB').attr('checked', 'checked');
            $('#HM_CB').change();
        }
        
        // Настраиваем кнопки
        $('#undoButton').click(Undo).attr('disabled', 'disabled');
        
		// Настраиваем метку
		$('#autoCaption').change(Mark_changed).keyup(Mark_changed);
		
        // Загружаем сам кондуит
        LoadConduit();
    }
    
    // object itself (for access to public methods and properties)
    var self = this;
}

Conduit = new __Conduit();