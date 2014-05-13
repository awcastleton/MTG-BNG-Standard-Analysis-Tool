var result = $.csv.toArrays("cardCounts.csv");

var csv_as_array = [];
function drawVisualization() {
  $.ajax({
    url: "cardCounts.csv",
    aync: false,
    success: function (csvd) {
        csv_as_array = $.csv2Array(csvd);
    }, 
    dataType: "text",
    complete: function () {
        // use the array of arrays (variable csv_as_array)
       // for further processing
    }
  });
}