var chart = c3.generate({
  bindto: '#chart2',
  size: {
    width: 650,
    height: 400
  },
  data: {
    x: 'name',
    url: 'bestCards.csv',
    type: 'bar'
  },
  legend: {
    show: false
  },
  axis: {
    x: {
      type: 'categorized',
      show: true,
      height: 170
    },
    rotated: true
  },

  tooltip: {
    value: function(value, ratio, id) {
      var img = document.createElement('img');
      img.src = "http://mtgimage.com/card/" + id + ".jpg";
      return img;
    }
  },
  color: {
    pattern: ['#1f77b4']
  },
});