
initSlider();
$("#designSearch").click(() => getImages());

var galleries = ["Food", "Indoors", "Outdoors"];
var indices = {};
var numImages = 4;
var imgwidth = 100 / numImages;
var slideId = 'slideshow-container';

function openTab(evt, type) {
  for(i=0;i<galleries.length;i++) {
    var gallery = document.getElementById(galleries[i] + "_gallery");
    gallery.style.display = (type == galleries[i]) ? 'block' : 'none';
  }
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
  indices = {}

  $.ajax({
      url: "/fetch_designs",
      type: "get",
      data: {
          land_area_start: landAreaSlider.noUiSlider.get()[0],
          land_area_end: landAreaSlider.noUiSlider.get()[1],
          timings_start: timingSlider.noUiSlider.get()[0],
          timings_end: timingSlider.noUiSlider.get()[1],
          labels: galleries,
          cuisine: cuisineSelector.value
      },
      success: function(response) {
          images = response.img
          labels = response.labels
          for(var i=0; i<galleries.length; i++){
            displayGallery(images[i], labels[i], galleries[i])
          }
      },
      error: function(xhr) {
          //Do Something to handle error
      }
  });

  for(i = 0;i<galleries.length;i++){
    var gallery = document.getElementById(galleries[i] + "_gallery");
    gallery.style.display = (i == 0) ? 'block' : 'none';
  }
}

function displayGallery(images, img_labels, label) {
  var photoIndex = [];
  var gallery = document.getElementById(label + '_gallery');
  gallery.innerHTML = '';
  for (i=0;i<images.length;i++){
    var currSlideContainer = getSlideContainer(i, label);

    var para = document.createElement('h4');
    para.setAttribute('class', 'row-label');

    var node = document.createTextNode(img_labels[i]);
    para.appendChild(node);

    currSlideContainer.appendChild(para);

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
  indices[label] = photoIndex;
}

function getSlide(image) {
  var slide = document.createElement('div');
  slide.setAttribute('class', 'slide');

  var img = document.createElement('img');
  img.setAttribute('class', 'gallery-image');
   img.setAttribute('src', image);
  // img.setAttribute('src', './static/data/images/' + image);
  img.setAttribute('onclick', 'getBusinessDetails(\'' + image.slice(0,-4) + '\')');
  var width = imgwidth.toString() + '%';
  img.setAttribute('width', width);     
  slide.appendChild(img);

  return slide;
}

function getSlideContainer(index, label){
  var slideContainer = document.createElement('div');
  slideContainer.setAttribute('class', slideId);

  var prev = document.createElement('a');
  prev.setAttribute('class', 'prev');
  prev.setAttribute('onclick', "showSlides(-1," + index.toString() + ",\'" + label + "\')");
  prev.appendChild(document.createTextNode('<'));

  var next = document.createElement('a')
  next.setAttribute('class', 'next');
  next.setAttribute('onclick', "showSlides(1," + index.toString() + ",\'" + label + "\')");
  next.appendChild(document.createTextNode('>'));

  slideContainer.appendChild(prev);
  slideContainer.appendChild(next);

  return slideContainer;
}

function showSlides(flag, index, label) {
  var x = document.getElementById(label + '_gallery').getElementsByClassName(slideId)[index].getElementsByClassName('slide');
  var photoIndex = indices[label];
  photoIndex[index] = photoIndex[index] + flag * numImages
  if(photoIndex[index] >= x.length) photoIndex[index] = photoIndex[index] - flag * numImages;
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

function getBusinessDetails(photo_id){
  $.ajax({
      url: "/fetch_business_details",
      type: "get",
      data: {
          photo_id: photo_id
      },
      success: function(response) {
        $('#business_details_modal .modal-content').html(response);
        $('#business_details_modal').modal("show");
      },
      error: function(xhr) {
          //Do Something to handle error
      }
  });
}
