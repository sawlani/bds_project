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
          displayGallery(response.img, response.labels)
          // $('#food_gallery').html(response.img)
      },
      error: function(xhr) {
          //Do Something to handle error
      }
  });
}

var photoIndex = [];
var numImages = 4;
var imgwidth = 100 / numImages;
var slideId = 'slideshow-container';

function displayGallery(images) {
  var gallery = document.getElementById('food_gallery');

  for (i=0;i<images.length;i++){
    var currSlideContainer = getSlideContainer(i);

    for(j=0;j<images[i].length;j++){
      var slide = getSlide(images[i][j]); 
      slide.style.display = 'none';

      if(j < numImages){
        slide.style.display = 'block';
      }

      currSlideContainer.appendChild(slide);
    }
    gallery.appendChild(currSlideContainer);
    currSlideContainer.style.display = 'block'
    photoIndex.push(0);
  }
}

function getSlide(image) {
  var slide = document.createElement('div');
  slide.setAttribute('class', 'slide');

  var img = document.createElement('img');
  img.setAttribute('class', 'gallery-image');
  img.setAttribute('src', './static/data/images/' + image);
  var width = imgwidth.toString() + '%';
  img.setAttribute('width', width);     
  slide.appendChild(img);

  return slide;
}

function getSlideContainer(index){
  var slideContainer = document.createElement('div');
  slideContainer.setAttribute('class', slideId);

  var prev = document.createElement('a');
  prev.setAttribute('class', 'prev');
  prev.setAttribute('onclick', "showSlides(-1," + index.toString() + ")");
  prev.appendChild(document.createTextNode('<'));

  var next = document.createElement('a')
  next.setAttribute('class', 'next');
  next.setAttribute('onclick', "showSlides(1," + index.toString() + ")");
  next.appendChild(document.createTextNode('>'));

  slideContainer.appendChild(prev);
  slideContainer.appendChild(next);

  return slideContainer;
}

function showSlides(flag, index) {
  var x = document.getElementsByClassName(slideId)[index].getElementsByClassName('slide');
  photoIndex[index] = photoIndex[index] + flag * numImages
  if(photoIndex[index] >= x.length) photoIndex[index] = photoIndex[index] % x.length;
  if(photoIndex[index] < 0) photoIndex[index] = 0;
  
  for (i = 0; i < x.length; i++) {
     x[i].style.display = "none";  
  }
  for(i=0;i < numImages; i++) {
    if(photoIndex[index] + i < x.length){
      x[photoIndex[index] + i].style.display = "block";
    }
  }  
}
