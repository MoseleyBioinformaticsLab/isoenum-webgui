var extractTableHeader = function(tableID) {
    var header = [];
    var tableHead = $(tableID).find('thead');

    $.each($(tableHead).find('tr > th'), function(index, value) {
        header.push($(value).html())
    });
    return header
};


var rowToJSON = function(tableID, rowID) {
    var header = extractTableHeader(tableID);
    var row = $('tr#' + rowID);
    var jsonObject = {};

    $(row).find('td').each(function(index, value) {
        if (header[index] !== "Update/Remove") {
            jsonObject[header[index]] = $(value).html();
        }
        jsonObject["record_id"] = rowID;
    });
    return jsonObject;
};


var tableToJSON = function(tableID) {
    var jsonArray = [];

    var tableBody = $(tableID).find('tbody');
    var header = extractTableHeader(tableID);

    $.each($(tableBody).find('tr'), function(index, value) {
        var jObject = {};
        jObject["id"] = $(this).attr("id");

        for(var i=0 ; i < header.length; i++) {
            jObject[header[i]] = $(this).find('td').eq(i).html()
        }
        jsonArray.push(jObject);
    });
    return jsonArray;
};
