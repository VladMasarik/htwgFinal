// Used to toggle the menu on small screens when clicking on the menu button
function myFunction() {
  var x = document.getElementById("navDemo");
  if (x.className.indexOf("w3-show") == -1) {
    x.className += " w3-show";
  } else {
    x.className = x.className.replace(" w3-show", "");
  }
}


// Number of registered users
function regUsers() {
  $.ajax({
    url: `/api/groupUserList`,
    success: function (result) {
      document.getElementById("showRegUsers").innerHTML += Object.keys(result["groupList"]).length;
    }
  });
}
window.onload = regUsers;


// Piechart for languages
document.getElementById("langButton").addEventListener("click", function () {

  google.charts.load('current', { 'packages': ['corechart'] });
  google.charts.setOnLoadCallback(drawChart);

  function drawChart() {
    const urlParams = new URLSearchParams(window.location.search);
    const search = urlParams.get('search_term');
    $.ajax({
      url: `/api/languageList?search_term=${search}`,
      success: function (result) {
        //      result = Object.keys(result["languageList"])
        lang = Object.keys(result)
        lang.forEach(function (key) {
          perc = result[key];
        });
        var list = [['Language', 'Percentage']]
        list.push.apply(list, [lang, perc])

        var data = google.visualization.arrayToDataTable(list);

        var options = {
          height: 300
        };

        var chart = new google.visualization.PieChart(document.getElementById('piechart'));
        chart.draw(data, options);
      }

    });

  }
});


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

    const urlParams = new URLSearchParams(window.location.search);
    const searchRepo = urlParams.get('search_term');

    $.ajax({
      url: `/api/repoList?search_term=${searchRepo}`,
      success: function (result) {
        list = result["list"]
        list.forEach(function (repo) {

          var tableBody = document.getElementById("timestamp");
          var row = document.createElement("tr");

          var reponame = document.createElement("td");
          //name {{ repo.name }}
          reponame.appendChild(document.createTextNode(repo));

          var created = document.createElement("td");
          created.style.textAlign = "center";
          //createdtime {{ repo.created_at }}
          var d = new Date(parseInt(repo.created_at, 10));
          var ds = d.toLocaleString("en-GB");
          created.appendChild(document.createTextNode(ds));

          var pushed = document.createElement("td");
          pushed.style.textAlign = "center";
          //pushedtime {{ repo.pushed_at }}
          var d = new Date(parseInt(repo.pushed_at, 10));
          var ds = d.toLocaleString("en-GB");
          pushed.appendChild(document.createTextNode(ds));

          var language = document.createElement("td");
          //language {{ repo.language }}
          language.appendChild(document.createTextNode(repo));

          var size = document.createElement("td");
          //size {{ repo.size }}
          size.appendChild(document.createTextNode(repo.size));

          row.appendChild(reponame);
          row.appendChild(created);
          row.appendChild(pushed);
          row.appendChild(language);
          row.appendChild(size);
          tableBody.appendChild(row);
        });
      }
    });
  }
});