function drawChart(rawData) {
    let data = google.visualization.arrayToDataTable(rawData.map((el, idx) => {
        return [el[0], idx === 0 ? el[1] : parseFloat(el[1])]
    }));

    let options = {
        title: 'Расходы',
        pieHole: 0.4,
    };

    let chart = new google.visualization.PieChart(document.getElementById('main-page__expense-chart'));
    chart.draw(data, options);
}
