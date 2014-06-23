var jsonOSF = JSON.parse('{"geo_data":[{"city": "Charlottesville", "country": "United States", "name": "Center for Research in Reproduction, University of Virginia", "state": "Virginia", "zip": "22908","latitude": 38.029306, "longitude": -78.4766781},{"city": "Ljubljana","country": "Slovenia","name": "UMC Ljubljana, Department of Infectious Diseases","zip":"1525","state": null,"latitude": 46.049865,"longitude": 14.5068921},{"city": "Baltimore","country": "United States","name": "Johns Hopkins University (BPRU) Bayview Campus","zip": "21224 6823","state": "Maryland","latitude": 39.2908608,"longitude": -76.6108073},{"city": "New Haven","country": "United States","name": "VA Connecticut Healthcare System","zip": "06519","state": "Connecticut","latitude": 41.3082138,"longitude": -72.9250518}]}');

function ctLocation(locationJson){
    this.json = locationJson;
    this.coordinates = L.latLng(locationJson["latitude"],locationJson["longitude"]);
    this.marker = L.marker(this.coordinates);
    if (locationJson["state"] !== null){
        this.popup = ("<b>"+locationJson["name"]+"</b><br>"+locationJson["city"]+", "+locationJson["state"]+"<br>"+locationJson["country"]);
    } 
    else {
        this.popup = ("<b>"+locationJson["name"]+"</b><br>"+locationJson["city"]+"<br>"+locationJson["country"]);
    };
    this.marker.bindPopup(this.popup);
};

function ctMap(){
    this.map = L.map('map',{
        worldCopyJump:true
    }).setView(L.latLng(38.0299,-78.4790), 8);

    this.tileLayer = L.tileLayer('http://otile1.mqcdn.com/tiles/1.0.0/map/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
    });
    this.tileLayer.addTo(this.map);
    this.ctLocationList = null;

    var generateLocationList = function(jsonOSF){
        var ctLocationList = new Array();
        for (var x in jsonOSF["geo_data"]){
            ctLocationList.push(new ctLocation(jsonOSF["geo_data"][x]));
        };
        return ctLocationList;
    };

    var zoomFitPoints = function(ctLocationList, map){
        var coordinateList = new Array();
        for (var x in ctLocationList){
            coordinateList.push(ctLocationList[x].coordinates);
        };
        map.fitBounds(coordinateList);
    };
    
    var addMarkers = function(ctLocationList, map){
        for (var x in ctLocationList){
            ctLocationList[x].marker.addTo(map);
        };
    };

    var removeMarkers = function(ctLocationList, map){
        for (var x in ctLocationList){
           map.removeLayer(ctLocationList[x].marker);
        };
    };

    this.updateMap = function(jsonOSF){
        if (this.ctLocationList!==null){
            removeMarkers(this.ctLocationList, this.map);
        };
        this.ctLocationList = generateLocationList(jsonOSF);
        zoomFitPoints(this.ctLocationList, this.map);
        addMarkers(this.ctLocationList, this.map);
    };
};



x = new ctMap();
x.updateMap(jsonOSF);




//The tile layer below is for the OSM tile layer. Swap it out with this.tileLayer in ctMap() to switch to using the OSM tile layer.
//    this.tileLayer = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
//        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
//    });
