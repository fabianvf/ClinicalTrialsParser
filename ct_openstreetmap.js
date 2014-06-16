

var jsonOSF = JSON.parse('{"geo_data":[{"city": "Charlottesville", "country": "United States", "name": "Center for Research in Reproduction, University of Virginia", "state": "Virginia", "zip": "22908","latitude": 40.029306,"longitude": -80.4766781},{"city": "Ljubljana","country": "Slovenia","name": "UMC Ljubljana, Department of Infectious Diseases","zip":"1525","state": null,"latitude": 46.049865,"longitude": 14.5068921},{"city": "Baltimore","country": "United States","name": "Johns Hopkins University (BPRU) Bayview Campus","zip": "21224 6823","state": "Maryland","latitude": 39.2908608,"longitude": -76.6108073},{"city": "New Haven","country": "United States","name": "VA Connecticut Healthcare System","zip": "06519","state": "Connecticut","latitude": 41.3082138,"longitude": -72.9250518}]}');

var coordinateList = new Array();
for (var x in jsonOSF["geo_data"]){
    coordinateList.push(L.latLng(jsonOSF["geo_data"][x]["latitude"],jsonOSF["geo_data"][x]["longitude"]));
};


var map = L.map('map',{
    worldCopyJump:true
}).setView(coordinateList[0], 8);

map.fitBounds(coordinateList);


L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
}).addTo(map);


for (var y in coordinateList){
    studyLocation = L.marker(coordinateList[y]).addTo(map);
    if (jsonOSF["geo_data"][y]["state"] !== null){
        studyLocation.bindPopup("<b>"+ jsonOSF["geo_data"][y]["name"] +"</b><br>"+jsonOSF["geo_data"][y]["city"]+", "+jsonOSF["geo_data"][y]["state"]+"<br>"+jsonOSF["geo_data"][y]["country"]);
    } 
    else {
        studyLocation.bindPopup("<b>"+ jsonOSF["geo_data"][y]["name"] +"</b><br>"+jsonOSF["geo_data"][y]["city"]+"<br>"+jsonOSF["geo_data"][y]["country"]);
    };
};
