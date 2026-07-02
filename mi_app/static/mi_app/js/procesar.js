$(document).ready(function(){
    var weatherData = [];

    cargarValores();

    $('.comboIndicador').change(function(){
        var selectedCode = $(this).val();
        if (selectedCode) {
            var cityInfo = weatherData.find(function(item){
                return item.code === selectedCode;
            });
            if (cityInfo) {
                mostrarClima(cityInfo);
            }
        }
    });

    function cargarValores(){
        $.ajax({
            method:'GET',
            url:'https://api.boostr.cl/weather.json',
            dataType:'JSON',
            success:function(data){
                weatherData = data.data || [];
                var $select = $('.comboIndicador');
                $select.empty();
                $select.append('<option value="">(Seleccione una ciudad)</option>');
                weatherData.forEach(function(item){
                    $select.append('<option value="'+item.code+'">'+item.city+'</option>');
                });
                if (weatherData.length) {
                    mostrarClima(weatherData[0]);
                    $select.val(weatherData[0].code);
                }
            },
            error:function(e){
                console.log("Error de comunicación API.");
                $('.respuesta').text('No se pudo cargar la información del clima.');
            }
        });
    }

    function mostrarClima(city){
        $('.climaTemperatura').text('Temperatura: ' + city.temperature + '°');
        $('.climaCondicion').text('Condición: ' + city.condition);
        $('.climaHumedad').text('Humedad: ' + city.humidity + '%');
        $('.climaActualizado').text('Actualizado: ' + city.updated_at);
        $('.respuesta').text('Clima en ' + city.city);
    }
});