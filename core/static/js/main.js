function drawChart(rawData) {
    let data = google.visualization.arrayToDataTable(rawData.map((el, idx) => {
        return [el[0], idx === 0 ? el[1] : parseFloat(el[1])]
    }));

    let options = {
        title: 'Расходы',
        pieHole: 0.4,

        backgroundColor: {
            fill: '474747',
        },
        chartArea: {
            width: '90%'
        },
        // colors: ['orange', 'blue', 'orange'],
        // forceIFrame: true,
        legend: { 
            position: 'right',
            textStyle: { color: 'white',
                fontSize: 13,
                maxLines: 200
            },
        },
        titleTextStyle:{
            color: 'white',
                fontSize: 13,
        },

    };

    let chart = new google.visualization.PieChart(document.getElementById('main-page__expense-chart'));
    chart.draw(data, options);
}
