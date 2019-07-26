function __Graphics() {

    // private properties:
    var all_data;
    var hide;

    var plot;       // график крупным планом
    var plot_conf;
    var overview;   // "обзор" всех данных внизу страницы
    var overview_conf;
    
    var all_selected = true;

    // public properties:
    
    // private methods:

    function Redraw() {
        var data = new Array();
        for(var j = 0, l = all_data.length; j < l; ++j) {
            if (!hide[j]) {
                data.push(all_data[j]);
            }
        }

        plot     = $.plot($("#MainPlot"), data, plot_conf);
        overview = $.plot($("#overview"), data, overview_conf);

        // легенду рисуем только один раз
        plot_conf.legend.show = false;
    }

    function UpdateLegend(pos) { 
        if (pos.x === undefined) {
            return;
        }
        var axes = plot.getAxes();
        if (pos.x < axes.xaxis.min || pos.x > axes.xaxis.max ||
            pos.y < axes.yaxis.min || pos.y > axes.yaxis.max) {
            return;
        }  
        var x = pos.x.toFixed();
        $('#legend .legendSolved').each(function(i){
                                            $(this).html(all_data[i].data[x][1]);
                                        });
    }
    
    // Получаем с сервера список дат и успехов школьников
    function GetData() {
        $.ajax({
            type:   'POST',
            url:    'ajax/GetStats.php',
            data:   {Class: SelectedClass()},
            dataType: 'json',
            success: function(json){
                        // Сохраняем выбор пользователя (класс)
                        SaveSelection();
                        // Дешифруем полученный json и рисуем графики
                        DrawPlot(json);
                     },
            error:   function(jqXHR, textStatus, errorThrown) {
                        //$('#conduit').html('');
                        var msg = 'Не удалось получить ответ от сервера: ';
                        alert(msg + jqXHR.status + ' ' + textStatus);
                     }
        });
    }
    
    // Форматируем метку на оси абсцисс
    function FormatTick(s) {
        return MathML.Frac(s.substr(6, 2), s.substr(4, 2));
    }
    
    // Парсим данные сервера и рисуем график
    function DrawPlot(json) {
        
        var Dates = json.D, L = Dates.length;
        var Pupils = json.P;
        
        //alert(JSON.stringify(json));
        
        hide = new Array();
        all_data = new Array();
        
        var counter = 0;
        for (Pupil in Pupils) {
            var Data = new Array();
            for (var i = 0; i < L; ++i) {
                Data.push([i,Pupils[Pupil][i]]);
            }
            all_data.push({
                label: Pupil,
                color: counter++,
                data:  Data
            });
            hide.push(false);
        }
        
        var ticks = new Array();
        for (var i = 0; i < L; ++i) {
            ticks.push([i, FormatTick(Dates[i])]);
        }
        var new_conf = {
            xaxis: {
                ticks: ticks
            },
            legend: {
                show: true
            }
        };
        $.extend(true, plot_conf, new_conf);
        
        // рисуем графики в первый раз
        Redraw();

        // Переделываем легенду: 
        // Добавляем в начало каждой строки checkbox
        $('#legend td.legendColorBox').before(  function(i){
                                                    return '<td><input class="legendCheckbox" type="checkbox" onclick="Graphics.SingleCheck('+ i +');" checked="checked"></td>';
                                                });
        // Добавляем в конец каждой строки количество сданных задач
        $('#legend td.legendLabel').after('<td class="legendSolved" style="padding-left:2pt;padding-right:2pt;min-width:2em" >--</td>');
    }
    
    function SelectedClass() {
        return $('#classSelector option').filter(':selected').val();
    }
    
    // сохраняем последний класс в cookie
    function SaveSelection() {
        $.cookie('Class', SelectedClass(), {expires: 30});
    } 
    
    // public methods:
    
    this.SingleCheck = function(i) {
        hide[i] = !hide[i];
        Redraw();
    }
    
    this.MultiCheck = function() {
        var state = ($('#SA_CB').attr('checked') === 'checked');
        if (state) {
            $('#legend .legendCheckbox').attr('checked', 'checked');
        } else {
            $('#legend .legendCheckbox').removeAttr('checked');
        }
        for(var i = 0, l = hide.length; i < l; ++i) {
            hide[i] = !state;
        }
        Redraw();
    }
    
    this.init = function() {
        
        MathML.CheckSupport();
        
        plot_conf = {
            series: {
                lines: { 
                    show: true,
                    lineWidth: 2 
                }
            },
            crosshair: { mode: "x" },
            grid: { 
                hoverable: true, 
                autoHighlight: false 
            },
            yaxis: {
                min: 0,
                max: 30
            },
            legend: {
                noColumns: 3,
                container: $("#legend")
            }
        };

        overview_conf = {
            series: {
                lines: { 
                    show: true,
                    lineWidth: 1
                },
                shadowSize: 0
            },
            xaxis: {
                ticks: []
            },
            yaxis: {
                ticks: []
            },
            selection: {
                mode: "x"
            }, 
            legend: {
                show: false
            }
        };
        
        $('#classSelector').change(GetData);
        
        // Общая настройка панелей
        NavBar.init();
        
        // событие - новое выделение на overview    
        $("#overview").bind("plotselected", function (event, ranges) {
                                                var r = ranges.xaxis;
                                                // перемещаем обзор в новую область
                                                var new_conf = {
                                                    xaxis: {
                                                        min: r.from,
                                                        max: r.to
                                                    }
                                                };
                                                $.extend(true, plot_conf, new_conf);
                                                Redraw();
                                            });
        
        // событие - курсор над графиком
        var sleep = false;
        $("#MainPlot").bind("plothover", function (event, pos, item) {
                                                if (!sleep) {
                                                    sleep = true;
                                                    UpdateLegend(pos);
                                                    setTimeout(function(){sleep = false}, 50);
                                                }
                                            });
        
        GetData();
    }
    
    // object itself (for access to public methods and properties)
    //var self = this;
}

Graphics = new __Graphics();