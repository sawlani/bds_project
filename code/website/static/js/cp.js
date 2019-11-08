//
// GLOBAL VARIABLES
var activeTracts = [];
var choropleth;
//
//

var svg = d3.select("#my_vis").append("svg")
    .attr("preserveAspectRatio", "xMinYMin meet")
    .attr("viewBox", "0 0 1000 600");

    var projection = d3.geo.albers()
    .center([19, 38.9])
    .parallels([50, 60])
    .scale(5000 * 35);
    // .translate(width/2, height/2);

var path = d3.geo.path().projection(projection);

var color = d3.scale.quantize()
              .range(['#fff','#d6e6e6','#c2dbda','#afcfce','#9cc4c3','#88b8b7','#74adac','#60a1a1','#4a9696','#308b8b','#008080']);


d3.queue()
    .defer(d3.json, "static/data/dc_data.json")
    .await(plotData);

function plotData(error, us) {

  choropleth = svg.selectAll("path")
        .data(us.features)
        .enter().append("path");
  choropleth
        .attr("d", path)
        .attr("id", d => d.properties.TRACT)
        .attr("stroke", "black")
        .attr("class", "map-census-tract")
        .on('click', d => {
            var tract = parseInt(d.properties.TRACT);
            getTractData(tract);
        });
}

function colorChoropleth(data) {

    color.domain(d3.extent(Object.values(data), function(d) {
      return d;
    }));

    choropleth.attr("fill", function(d){
        tract = parseInt(d.properties.TRACT);
        // console.log(data[tract]);
        return color(data[tract]);
    });

}


function showTractDetails(tract) {
    // data = getTractDetails();
    $('#censusDetailsModal .modal-title').text("Census Tract: " + tract);
    $('#censusDetailsModal .modal-body').html(
        `<img class="tract-img" src="static/data/images/tractDetails.png?${Date.now()}">`
    );
    // $('#censusDetailsModal .modal-footer button').attr("value", tract);
    $('#censusDetailsModal').modal('show');
}

function hideTractDetails() {
    $('#censusDetailsModal').modal('hide');
}

// call init
init();

// put all init stuff here
function init() {
    initSlider();
    
    $(document).on('ready', function() {
        setTimeout(getFilteredData, 10); // calling this once initially to get data without changing sliders
    });

}

function initSlider() {
    var priceSlider = document.getElementById('price-slider');
    noUiSlider.create(priceSlider, {
        start: [180000, 680000],
        connect: true,
        range: {
            'min': 20000,
            // '50%': 5000,
            'max': 1e6
        },
        step: 1000,
        margin: 1000,
        tooltips: [wNumb({
            prefix: '$',
            decimals: 0
        }), wNumb({
            prefix: '$',
            decimals: 0
        })]
        // pips: {
        //     mode: 'range',
        //     density: 4
        // }

    });
    priceSlider.noUiSlider.on('change', function (values, handle) {
        getFilteredData();
    });

    var landAreaSlider = document.getElementById('land-area-slider');
    noUiSlider.create(landAreaSlider, {
        start: [0, 20000],
        connect: true,
        range: {
            'min': 0,
            // '50%': 5000,
            'max': 50000
        },
        step: 100,
        margin: 100,
        tooltips: [wNumb({
            postfix: ' sq.ft.',
            decimals: 0
        }), wNumb({
            postfix: ' sq.ft.',
            decimals: 0
        })]
    });
    landAreaSlider.noUiSlider.on('change', function (values, handle) {
        getFilteredData();
    });

    var bedroomSlider = document.getElementById('bedroom-slider');
    noUiSlider.create(bedroomSlider, {
        start: [1, 10],
        connect: true,
        range: {
            'min': 0,
            'max': 24
        },
        step: 1,
        format: wNumb({
            decimals: 0
        }),
        tooltips: true,
    });
    bedroomSlider.noUiSlider.on('change', function (values, handle) {
        getFilteredData();
    });

    var bathroomSlider = document.getElementById('bathroom-slider');
    noUiSlider.create(bathroomSlider, {
        start: [1, 8],
        connect: true,
        range: {
            'min': 0,
            'max': 14
        },
        format: wNumb({
            decimals: 0
        }),
        step: 1,
        tooltips: true,
    });
    bathroomSlider.noUiSlider.on('change', function (values, handle) {
        getFilteredData();
    });


    var predictionYearSlider = document.getElementById('prediction-year-slider');
    noUiSlider.create(predictionYearSlider, {
        start: 2022,
        connect: [true, false],
        range: {
            'min': 2019,
            'max': 2025
        },
        step: 1,
        tooltips: wNumb({
            prefix: 'Year: '
        }),
        format: wNumb({
          decimals: 0
        }),
        pips: {
            mode: 'range',
            density: 16
        }
    });
    predictionYearSlider.noUiSlider.on('change', function (values, handle) {
        getFilteredData();
    });

    var budgetSlider = document.getElementById('budget-slider');
    noUiSlider.create(budgetSlider, {
        start: 6e6,
        connect: [true, false],
        range: {
            'min': 50000,
            'max': 10e6
        },
        step: 1000,
        tooltips: [wNumb({
            prefix: '$',
            decimals: 0
        })]
    });
    budgetSlider.noUiSlider.on('change', function (values, handle) {
        getFilteredData();
    });

    // var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    // var predictionMonthSlider = document.getElementById('prediction-month-slider');
    // noUiSlider.create(predictionMonthSlider, {
    //     start: 6,
    //     connect: [true, false],
    //     range: {
    //         'min': 0,
    //         'max': 11
    //     },
    //     step: 1,
    //     tooltips: true,
    //     format: {
    //         to: value => months[parseInt(value)],
    //         from: value => value
    //     },
    // });
    // predictionMonthSlider.noUiSlider.on('change', function (values, handle) {
    //     getFilteredData();
    // });

}

function getFilteredData(censusTracts=[]) {
    // e.preventDefault();
    // var Slider = document.getElementById('price-slider');
    // var landAreaSlider = document.getElementById('land-area-slider');
    // var bedroomSlider = document.getElementById('bedroom-slider');
    // var priceSlider = document.getElementById('price-slider');
    // var landAreaSlider = document.getElementById('land-area-slider');
    // var bedroomSlider = document.getElementById('bedroom-slider');
    // var bathroomSlider = document.getElementById('bathroom-slider');
    // var predictionYearSlider = document.getElementById('prediction-year-slider');
    // $.ajax({
    //     url: "/fetch_filtered_data",
    //     type: "get",
    //     data: {
    //         price_start: priceSlider.noUiSlider.get()[0],
    //         price_end: priceSlider.noUiSlider.get()[1],
    //         land_area_start: landAreaSlider.noUiSlider.get()[0],
    //         land_area_end: landAreaSlider.noUiSlider.get()[1],
    //         bedrooms_start: bedroomSlider.noUiSlider.get()[0],
    //         bedrooms_end: bedroomSlider.noUiSlider.get()[1],
    //         bathrooms_start: bathroomSlider.noUiSlider.get()[0],
    //         bathrooms_end: bathroomSlider.noUiSlider.get()[1],
    //         prediction_year: predictionYearSlider.noUiSlider.get(),
    //         census_tracts: censusTracts
    //     },
    //     success: function(response) {
    //         colorChoropleth(response);
    //     },
    //     error: function(xhr) {
    //         //Do Something to handle error
    //     }
    // });
}

function getTractData(censusTract) {
    // e.preventDefault();
    var priceSlider = document.getElementById('price-slider');
    var landAreaSlider = document.getElementById('land-area-slider');
    var bedroomSlider = document.getElementById('bedroom-slider');
    var bathroomSlider = document.getElementById('bathroom-slider');
    var predictionYearSlider = document.getElementById('prediction-year-slider');
    $.ajax({
        url: "/fetch_tract_data",
        type: "get",
        data: {
            price_start: priceSlider.noUiSlider.get()[0],
            price_end: priceSlider.noUiSlider.get()[1],
            land_area_start: landAreaSlider.noUiSlider.get()[0],
            land_area_end: landAreaSlider.noUiSlider.get()[1],
            bedrooms_start: bedroomSlider.noUiSlider.get()[0],
            bedrooms_end: bedroomSlider.noUiSlider.get()[1],
            bathrooms_start: bathroomSlider.noUiSlider.get()[0],
            bathrooms_end: bathroomSlider.noUiSlider.get()[1],
            prediction_year: predictionYearSlider.noUiSlider.get(),
            census_tract: censusTract
        },
        success: function(response) {
            showTractDetails(response);
        },
        error: function(xhr) {
            //Do Something to handle error
        }
    });
}



// Toggling the active tracts
// $("#toggleActive").click(function() {
//     toggleTractActive(this);
// });

// function toggleTractActive(button) {
//     var tract = $(button).val();
//     console.log(tract)
//     var index = activeTracts.indexOf(tract);
//     if(index !== -1) {
//         activeTracts.splice(index, 1);
//     } else {
//         activeTracts.push(tract);
//     }
//     console.log(activeTracts);
// }

// Response to Build Portfolio Button
$("#buildPortfolio").click(() => getPortolioData(activeTracts));

function getPortolioData(censusTracts=[]){
  var priceSlider = document.getElementById('price-slider');
  var landAreaSlider = document.getElementById('land-area-slider');
  var bedroomSlider = document.getElementById('bedroom-slider');
  var bathroomSlider = document.getElementById('bathroom-slider');
  var predictionYearSlider = document.getElementById('prediction-year-slider');
  var budgetSlider = document.getElementById('budget-slider');
  $.ajax({
      url: "/fetch_portfolio",
      type: "get",
      data: {
          price_start: priceSlider.noUiSlider.get()[0],
          price_end: priceSlider.noUiSlider.get()[1],
          land_area_start: landAreaSlider.noUiSlider.get()[0],
          land_area_end: landAreaSlider.noUiSlider.get()[1],
          bedrooms_start: bedroomSlider.noUiSlider.get()[0],
          bedrooms_end: bedroomSlider.noUiSlider.get()[1],
          bathrooms_start: bathroomSlider.noUiSlider.get()[0],
          bathrooms_end: bathroomSlider.noUiSlider.get()[1],
          prediction_year: predictionYearSlider.noUiSlider.get(),
          census_tracts: censusTracts,
          total_budget: budgetSlider.noUiSlider.get()
      },
      success: function(response) {
          $('#portfolioModal .modal-content').html(response);
          $('#portfolioModal').modal("show");
      },
      error: function(xhr) {
          //Do Something to handle error
      }
  });
}
