var XMLHttpRequestObject = false;

if (window.XMLHttpRequest) {
  XMLHttpRequestObject = new XMLHttpRequest();
} else if (window.ActiveXObject) {
  XMLHttpRequestObject = new ActiveXObject("Microsoft.XMLHTTP");
}

  var url = "index/xhr";
  var elems = document.getElementsByClassName("doneclass");

  if(XMLHttpRequestObject) {
  XMLHttpRequestObject.open("GET", url);
  XMLHttpRequestObject.onreadystatechange = function() {
    if (XMLHttpRequestObject.readyState == 4 &&
    XMLHttpRequestObject.status == 200) {
      x = XMLHttpRequestObject.responseText;
      if ( x=="False" ) {
        document.getElementById("taskFilter").innerHTML = "Show Completed tasks";
        document.getElementById("taskFilter").value="f";
        for(var i = 0; i != elems.length; ++i)
        {
          elems[i].style.visibility = "hidden";
          elems[i].style.display ='none'
        }
      }
      else {
        document.getElementById("taskFilter").innerHTML = "Hide Completed tasks";
        document.getElementById("taskFilter").value="t";
        for(var i = 0; i != elems.length; ++i)
        {
          elems[i].style.visibility = "visible";
          elems[i].style.display ='table-row'
        }
      }
    }
  }
  XMLHttpRequestObject.send(null);
  }

function ShowHideDoneTasks() {
  val = document.getElementById("taskFilter").value;
  val1 = (val == "t") ? "f" : "t";

  var url = "index/xhrval" + val1;
  var elems = document.getElementsByClassName("doneclass");

  if(XMLHttpRequestObject) {
  XMLHttpRequestObject.open("GET", url);
  XMLHttpRequestObject.onreadystatechange = function() {
    if (XMLHttpRequestObject.readyState == 4 &&
    XMLHttpRequestObject.status == 200) {
      x = XMLHttpRequestObject.responseText;
      document.getElementById("taskFilter").value=val1;
      if (x=="False") {
        document.getElementById("taskFilter").innerHTML = "Show Completed tasks";
        for(var i = 0; i != elems.length; ++i)
        {
          elems[i].style.visibility = "hidden";
          elems[i].style.display ='none'
        }
      }
      else {
        document.getElementById("taskFilter").innerHTML = "Hide Completed tasks";
        for(var i = 0; i != elems.length; ++i)
        {
          elems[i].style.visibility = "visible";
          elems[i].style.display ='table-row'
        }
      }
    }
  }
  XMLHttpRequestObject.send(null);
  }
}
