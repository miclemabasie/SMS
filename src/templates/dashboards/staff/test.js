var subject_list = {{ subject_list|safe|escape }};
var attendance_list = {{ attendance_list }};

    var barChartData = {
labels  : subject_list,
datasets: [
{
label               : 'Attendance Per Subject',
backgroundColor     : '#17A2B8',
borderColor         : 'rgba(60,141,188,0.8)',
pointRadius          : false,
pointColor          : '#3b8bba',
pointStrokeColor    : 'rgba(60,141,188,1)',
pointHighlightFill  : '#fff',
pointHighlightStroke: 'rgba(60,141,188,1)',
data                : attendance_list
}, 

]
}
var barChartCanvas = $('#barChart').get(0).getContext('2d')
var temp0 = barChartData.datasets[0]
//var temp1 = areaChartData.datasets[1]
barChartData.datasets[0] = temp0
// barChartData.datasets[1] = temp0

var stackedBarChartOptions = {
responsive              : true,
maintainAspectRatio     : false,
scales: {
xAxes: [{
  stacked: true,
}],
yAxes: [{
  stacked: true
}]
}
}

var barChart = new Chart(barChartCanvas, {
  type: 'bar', 
  data: barChartData,
  options: stackedBarChartOptions
})