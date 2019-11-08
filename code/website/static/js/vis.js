// 
initSlider();
$("#designSearch").click(() => getImages());

function openTab(evt, type) {
	// Declare all variables
	var i, tabcontent, tablinks;

	// Get all elements with class="tabcontent" and hide them
	tabcontent = document.getElementsByClassName("tabcontent");
	for (i = 0; i < tabcontent.length; i++) {
		tabcontent[i].style.display = "none";
	}

	// Get all elements with class="tablinks" and remove the class "active"
	tablinks = document.getElementsByClassName("tablinks");
	for (i = 0; i < tablinks.length; i++) {
		tablinks[i].className = tablinks[i].className.replace(" active", "");
	}

	// Show the current tab, and add an "active" class to the button that opened the tab
	document.getElementById(type).style.display = "block";
	evt.currentTarget.className += " active";
}

function initSlider() {

    var landAreaSlider = document.getElementById('land-area-slider');
    noUiSlider.create(landAreaSlider, {
        start: [0, 50],
        connect: true,
        range: {
            'min': 0,
            // '50%': 5000,
            'max': 100
        },
        step: 1,
        margin: 1,
        tooltips: [wNumb({
            postfix: ' miles',
            decimals: 0
        }), wNumb({
            postfix: ' miles',
            decimals: 0
        })]
    });

    var timingSlider = document.getElementById('timings-slider');
    noUiSlider.create(timingSlider, {
        start: [600, 1260],
        connect: true,
        range: {
            'min': 0,
            'max': 1440
        },
        step: 15,
        margin: 15,
        tooltips: true,
        format: {
        	from: Number,
        	to: function(value) {
        		return toClock(value);
        	}
        }
    });
}

function toClock(value) {
	var hours = Math.floor(value / 60);
    var minutes = Math.floor(value - (hours * 60));
    var ampm = "";  
    
    if(hours.length == 1) {hours = '12' + hours;}
    if(hours > 12) {ampm = "PM"; hours = hours-12;}
    else if(hours == 12){ampm = "PM";}
    else if(hours < 12){
        ampm = "AM"; 
        if(hours == 0)  hours =  12;            
                               
    }      
    if(minutes == 0){minutes = '0' + minutes;}               
    var combo = hours+':'+minutes + ampm;
    return combo
}

function getImages(){
  var landAreaSlider = document.getElementById('land-area-slider');
  var timingSlider = document.getElementById('timings-slider');
  var cuisineSelector = document.getElementById('cuisine-selector');
  console.log(cuisineSelector.value)
  $.ajax({
      url: "/fetch_designs",
      type: "get",
      data: {
          land_area_start: landAreaSlider.noUiSlider.get()[0],
          land_area_end: landAreaSlider.noUiSlider.get()[1],
          timings_start: timingSlider.noUiSlider.get()[0],
          timings_end: timingSlider.noUiSlider.get()[1],
          cuisine: cuisineSelector.value
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
