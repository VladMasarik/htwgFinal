// Used to toggle the menu on small screens when clicking on the menu button
function myFunction() {
    var x = document.getElementById("navDemo");
    if (x.className.indexOf("w3-show") == -1) {
      x.className += " w3-show";
    } else { 
      x.className = x.className.replace(" w3-show", "");
    }
  }

// Piechart for languages
google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);

function drawChart() {
    var data = google.visualization.arrayToDataTable([
      ['Language', 'No'],
      ['HTML',     5],
      ['JavaScript',      2],
      ['Python',  2],
      ['Java', 2],
      ['CSS',    3]
    ]);
    
    var options = {
    };

    var chart = new google.visualization.PieChart(document.getElementById('piechart'));

    chart.draw(data, options);
}

// Table for repositories
document.getElementById("reposButton").addEventListener("click", function () {
  document.getElementById("visible").innerHTML = "";
  if (!document.getElementById("timestamp").hasChildNodes()) {
      var table = document.getElementById("timestamp");
      var header = table.createTHead();
      var firstrow = header.insertRow(0);
      header.style.fontSize = "15px";
      header.style.textAlign = "center";
      header.style.backgroundColor = "rgb(75,9,88)";
      header.style.color = "white";
      header.style.borderColor = "#ddd";
      header.style.borderSytle = "solid";

      var cells = new Array(4);

      cells[0] = firstrow.insertCell(0);
      cells[1] = firstrow.insertCell(1);
      cells[2] = firstrow.insertCell(2);
      cells[3] = firstrow.insertCell(3);
      cells[4] = firstrow.insertCell(4);

      cells[0].style.width = "40%";
      cells[1].style.width = "15%";
      cells[2].style.width = "15%";
      cells[3].style.width = "15%";
      cells[4].style.width = "15%";

      cells[0].style.padding = "20px";
      cells[0].innerHTML = "<b>Name</b>";
      cells[1].innerHTML = "<b>Created</b>";
      cells[2].innerHTML = "<b>Pushed</b>";
      cells[3].innerHTML = "<b>Language</b>";
      cells[4].innerHTML = "<b>Size</b>";

// foreach repo in repolist

              var tableBody = document.getElementById("timestamp");
              var row = document.createElement("tr");

              var reponame = document.createElement("td");
              //name {{ repo.name }}
              reponame.appendChild(document.createTextNode(repo.name));

              var created = document.createElement("td");
              created.style.textAlign = "center";
              //createdtime {{ repo.created_at }}
              var d = new Date(parseInt(repo.createdtime, 10));
              var ds = d.toLocaleString("en-GB");
              created.appendChild(document.createTextNode(ds));

              var pushed = document.createElement("td");
              pushed.style.textAlign = "center";
              //pushedtime {{ repo.pushed_at }}
              var d = new Date(parseInt(repo.createdtime, 10));
              var ds = d.toLocaleString("en-GB");
              pushed.appendChild(document.createTextNode(ds));

              var language = document.createElement("td");
              //language {{ repo.language }}
              language.appendChild(document.createTextNode(repo.language));

              var size = document.createElement("td");
              //size {{ repo.size }}
              size.appendChild(document.createTextNode(repo.size));

              row.appendChild(reponame);
              row.appendChild(created);
              row.appendChild(pushed);
              row.appendChild(language);
              row.appendChild(size);
              tableBody.appendChild(row);

  }
});