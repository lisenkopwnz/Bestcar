$(document).ready(function() {
    // Обработчик события change для чек-боксов
    $('#checkbox1, #checkbox2').on('change', function() {
        // Если первый чек-бокс отмечен, второй снимается
        if ($('#checkbox1').is(':checked')) {
            $('#checkbox2').prop('checked', false);
        }
        // Если второй чек-бокс отмечен, первый снимается
        else if ($('#checkbox2').is(':checked')) {
            $('#checkbox1').prop('checked', false);
        }
    });

    $('#jsonForm').on('submit', function(e) {
        e.preventDefault(); // Предотвращаем стандартное поведение формы

        var formData = {
            checkbox1: $('#checkbox1:checked').val() || '',
            checkbox2: $('#checkbox2:checked').val() || ''
        };
        console.log(formData);
        $.ajax({
            url: '/your-server-endpoint/', // Замените на URL вашего серверного endpoint
            type: 'POST',
            data: JSON.stringify(formData),
            contentType: 'application/json; charset=utf-8',
            success: function(response) {
                // Очищаем предыдущие выводы
                $('#output').empty();

                // Выводим ответ сервера
                $('#output').append('<p>Server Response:</p>');
                $('#output').append('<pre>' + JSON.stringify(response, null, 2) + '</pre>');
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.error('Error:', textStatus, errorThrown);
            }
        });
    });
});