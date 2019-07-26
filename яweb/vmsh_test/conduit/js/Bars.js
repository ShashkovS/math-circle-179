function __NavBar(currentTab) {

    // private methods:
    
    function hide() {
        $('.navbar').toggleClass('hidden');
        $('.toolbar').toggleClass('hidden');
        if ($('.navbar').hasClass('hidden')) {
            $(this).html('&#9660;&nbsp;Панель навигации');
        } else {
            $(this).html('&#9650;&nbsp;Свернуть');
        }
    }
    
    // public methods:
    
    this.relogin = function() {
        $.ajax({
                url:        'dummy.php',
                username:   'logout',
                password:   'logout',
                success:    function() {
                                location.reload(true);
                            },
                error:      function() {
                                $('body').html('');
                                alert('Выход произведён успешно');
                            }
              });
    }

    this.logout = function() {
        $.ajax({
                url:        'logout/logout.php',
                username:   'logout',
                password:   'logout',
                success:    function() {
                                $('body').html('');
                                alert('Выход произведён успешно');
                            }
              });
    }
    
    this.init = function() {
        $('#'+currentTab).addClass('current');
        
        if (window.opera !== undefined) {
            this.relogin =  function() {
                                alert('В Opera данная функция не поддерживается');
                            };
        }
    }
}

function __ToolBar() {

    // private methods:
    
    function hide() {
        $('.toolbar').toggleClass('hidden');
        if ($('.toolbar').hasClass('hidden')) {
            $(this).html('&#9660;&nbsp;Панель инструментов');
        } else {
            $(this).html('&#9650;&nbsp;Свернуть');
        }
    }
    
    // public methods:
    
    this.init = function() {
        $('.toolbar .hide span').click(hide);
        
        // Привязываем и настраиваем datepicker
        $.datepicker.setDefaults($.datepicker.regional["ru"]);
		$('#autoCaption').datepicker({  constrainInput: false,
                                        showButtonPanel: true,
                                        showOtherMonths: true,
                                        navigationAsDateFormat: true,
                                        changeMonth: true
                                     });
        //var now = $.datepicker.formatDate($("#autoCaption").datepicker("option", "dateFormat"), new Date());
        //$('#autoCaption').val(now);
        $('#autoCaption').val('+');
    }
}

