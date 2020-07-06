var probs = d3.select('#probs').text()
console.log(probs)
var myClasses = d3.select('#classes').text()
console.log(myClasses)

var labelNames = d3.select('#labelNames').text()
console.log(labelNames)
var test = labelNames.split("'");
var names = [];
var temp = [];
for (var i=0; i<test.length; i++) {
    if (test[i] === "[") {
        temp.push(test[i])
    }
    else if (test[i] === ", ") {
        temp.push(test[i]);
    }
    else if (test[i] === "]"){
        temp.push(test[i])
    }
    else {
        names.push(test[i])
    }
}

// var test_classes = myClasses.split("'");
// var classes = [];
// var temp = [];
// for (var i=0; i<test_classes.length; i++) {
//     if (test_classes[i] === "[") {
//         temp.push(test_classes[i])
//     }
//     else if (test_classes[i] === ", ") {
//         temp.push(test_classes[i]);
//     }
//     else if (test_classes[i] === "]"){
//         temp.push(test_classes[i])
//     }
//     else {
//         classes.push(test_classes[i])
//     }
// }

var test_probs = probs.split(" ");
var myProbs = [];
var temp = [];
for (var i=0; i<test_probs.length; i++) {
    if (i===0) {
        myProbs.push(test_probs[0].slice(1,))
    }
    else if (i===test_probs.length-1) {
        myProbs.push(test_probs[test_probs.length-1].slice(0,(test_probs[test_probs.length-1].length)-1))
    }
    else {
        myProbs.push(test_probs[i])
    }
}
var myProbs = myProbs.map(d => +(d*100).toFixed(2))
// var myProbsNums = myProbs.map(d=> +d)
// myProbsNums.map(d => (d*100).toFixed(2))
var tbody = d3.select("tbody");
for (var i = 0; i<myProbs.length; i++) {
    var row = tbody.append("tr");
    var cell = row.append("td");
    cell.text(names[i]);
    var cell = row.append("td");
    cell.text(myProbs[i]);
};

var trace1 = {
    x:myProbs,
    y: names,
    type:'bar',
    orientation: 'h'

}
var layout1 = {
    title:{text: "Class Probability"},
    xaxis: {title: "Probability (%)"},
    // yaxis: {title: "Flower Class"},
    margin : {
        l: 140
    }
}
data1 = [trace1];
var config = {responsive: true}
Plotly.newPlot("myPlot",data1,layout1,config);