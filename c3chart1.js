var chart = c3.generate({
  bindto: '#chart1',
  size: {
    width: 680,
    height: 400
  },
  data: {
    url: 'archetypeSuccess.csv',
    type: 'bar'
  },
  axis: {
    x: {
      type: 'categorized',
      categories: ['2/7 to 2/20', '2/21 to 3/6', '3/7 to 3/20', '3/20 to 4/3', '4/4 to 4/17', '4/18 to 5/2'],
    },
  },
  color: {
    pattern: ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728']
  },
  legend: {
    position: 'right'
  }
});
