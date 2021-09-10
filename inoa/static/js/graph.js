google.charts.load('current', {packages: ['corechart', 'line']});
google.charts.setOnLoadCallback(drawLogScales)


function drawLogScales(id) {
    var dataGraphic = document.getElementById('A'+id)

    console.log(dataGraphic)
    var data = new google.visualization.DataTable();
   
    var text

    data.addColumn('date', 'X');
    data.addColumn('number', 'Ação');


    for(var i=1;i<dataGraphic.children.length;i++){
        var plot = []
        text = dataGraphic.children[i].textContent
        text = text.split('-')

        var dateText = text[0]
        var priceText = text[1]
        var dates = []
        dateText = dateText.replace(":", " ")
        dateText = dateText.split(' ')
        for (var count = 0; count < dateText.length;count++){

            //retricoes
            if(dateText[count] === " "){
                continue
            }
            if(dateText[count] === ""){
                continue
            }
            if(dateText[count] === "de"){
                continue
            }
            if(dateText[count] === "às"){
                continue
            }
            if(dateText[count] === "\n"){
                continue
            }


            if(dateText[count] === "Janeiro"){
                dates.push(1)
                continue
            }
            if(dateText[count] === "Fevereiro"){
                dates.push(2)
                continue
            }
            if(dateText[count] === "Março"){
                dates.push(3)
                continue
            }
            if(dateText[count] === "Abril"){
                dates.push(4)
                continue
            }
            if(dateText[count] === "Maio"){
                dates.push(5)
                continue
            }
            if(dateText[count] === "Junho"){
                dates.push(6)
                continue
            }
            if(dateText[count] === "Julho"){
                dates.push(7)
                continue
            }
            if(dateText[count] === "Agosto"){
                dates.push(8)
                continue
            }
            if(dateText[count] === "Setembro"){
                dates.push(9)
                continue
            }
            if(dateText[count] === "Outubro"){
                dates.push(10)
                continue
            }
            if(dateText[count] === "Novembro"){
                dates.push(11)
                continue
            }
            if(dateText[count] === "Dezembro"){
                dates.push(12)
                continue
            }

            dates.push(dateText[count])
        }

        
        plot.push([new Date(parseInt(dates[2]), dates[1], parseInt(dates[0]),parseInt(dates[3]),parseInt(dates[4])),parseFloat(priceText)])
        data.addRows(plot)
    }
    
    var options = {
        hAxis: {
            title: 'Time'
        },
        width: 900,
        height: 500,
        vAxis: {
            title: 'Popularity'
        }
    };

    var chart = new google.visualization.LineChart(document.getElementById('chart_div'));

    chart.draw(data, options);
}
