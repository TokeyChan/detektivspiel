var main_container = document.getElementById("main_container");
var bar_container = document.getElementById("bar_container");

var felix_dimmer = document.getElementById("felix_dimmer");
var sophia_dimmer = document.getElementById("sophia_dimmer");
var julian_dimmer = document.getElementById("julian_dimmer");
var stripper_dimmer = document.getElementById("stripper_dimmer");
var honey_dimmer = document.getElementById("honey_dimmer");

var felix_button = document.getElementById("felix_button");
var sophia_button = document.getElementById("sophia_button");
var julian_button = document.getElementById("julian_button");
var stripper_button = document.getElementById("stripper_button");
var honey_button = document.getElementById("honey_button");

var insp_popup_window = document.getElementById("insp_popup");
var insp_title = document.getElementById("insp_title");
var insp_text = document.getElementById("insp_text");
var insp_close = document.getElementById("insp_close");

var note = document.getElementById("note");
var inspector_array = [];

var felix_bars = bar_container.cloneNode(true);
felix_bars.id = "felix_bars";
felix_bars.style.display = "none";
main_container.appendChild(felix_bars);

var sophia_bars = bar_container.cloneNode(true);
sophia_bars.id = "sophia_bars";
sophia_bars.style.display = "none";
main_container.appendChild(sophia_bars);

var julian_bars = bar_container.cloneNode(true);
julian_bars.id = "julian_bars";
julian_bars.style.display = "none";
main_container.appendChild(julian_bars);

var stripper_bars = bar_container.cloneNode(true);
stripper_bars.id = "stripper_bars";
stripper_bars.style.display = "none";
main_container.appendChild(stripper_bars);

var honey_bars = bar_container.cloneNode(true);
honey_bars.id = "honey_bars";
honey_bars.style.display = "none";
main_container.appendChild(honey_bars);

var felix_locked,
    sophia_locked,
    julian_locked,
    stripper_locked,
    honey_locked = false;


felix_dimmer.addEventListener("click", function() {
  if (!felix_locked)
  {
    felix_bars.style.display = "block";
    felix_button.style.display = "block";
    felix_locked = true;
  }
  else
  {
    felix_bars.style.display = "none";
    felix_button.style.display = "none";
    felix_locked = false;
  }
});

sophia_dimmer.addEventListener("click", function() {
  if (!sophia_locked)
  {
    sophia_bars.style.display = "block";
    sophia_button.style.display = "block";
    sophia_locked = true;
  }
  else
  {
    sophia_bars.style.display = "none";
    sophia_button.style.display = "none";
    sophia_locked = false;
  }
});

julian_dimmer.addEventListener("click", function() {
  if (!julian_locked)
  {
    julian_bars.style.display = "block";
    julian_button.style.display = "block";
    julian_locked = true;
  }
  else
  {
    julian_bars.style.display = "none";
    julian_button.style.display = "none";
    julian_locked = false;
  }
});

stripper_dimmer.addEventListener("click", function() {
  if (!stripper_locked)
  {
    stripper_bars.style.display = "block";
    stripper_button.style.display = "block";
    stripper_locked = true;
  }
  else
  {
    stripper_bars.style.display = "none";
    stripper_button.style.display = "none";
    stripper_locked = false;
  }
});

honey_dimmer.addEventListener("click", function() {
  if (!honey_locked)
  {
    honey_bars.style.display = "block";
    honey_button.style.display = "block";
    honey_locked = true;
  }
  else
  {
    honey_bars.style.display = "none";
    honey_button.style.display = "none";
    honey_locked = false;
  }
});


var buttons = document.getElementsByClassName("continue_button");
for (let i = 0; i < buttons.length; i++)
{
  buttons[i].addEventListener("click", function() {
    if (!confirm("Bist Du dir sicher?"))
      return;

    let form = document.getElementById("submit_form");

    if (felix_locked) {
      let input = document.createElement('input');
      input.type = "hidden";
      input.name = "chosen";
      input.value = "felix";
      form.appendChild(input);
    }
    if (sophia_locked) {
      let input = document.createElement('input');
      input.type = "hidden";
      input.name = "chosen";
      input.value = "sophia";
      form.appendChild(input);
    }
    if (julian_locked) {
      let input = document.createElement('input');
      input.type = "hidden";
      input.name = "chosen";
      input.value = "julian";
      form.appendChild(input);
    }
    if (stripper_locked) {
      let input = document.createElement('input');
      input.type = "hidden";
      input.name = "chosen";
      input.value = "stripper";
      form.appendChild(input);
    }
    if (honey_locked) {
      let input = document.createElement('input');
      input.type = "hidden";
      input.name = "chosen";
      input.value = "honey";
      form.appendChild(input);
    }
    form.submit();
  });
}

let link = document.getElementById("link");
let note_text = document.getElementById("note_text");
note.addEventListener("click", function() {
  link.click();
});
note_text.addEventListener("click", function() {
  link.click();
});

function openInspectorPopup() {
    console.log(inspector_array);
    if (inspector_array.length == 0)
      return;
    insp_title.innerHTML = inspector_array[0].title;
    insp_text.innerHTML = inspector_array[0].text;
    insp_popup_window.style.display = "block";

    inspector_array.shift();
}

insp_close.addEventListener("click", function() {
  if (inspector_array.length == 0) {
    insp_popup_window.style.display = "none";
  } else {
    openInspectorPopup();
  }
});
// ----------------------------- ON LOAD ------------------------

window.addEventListener("load", function() {
  var insp_array = [];
  let request = new XMLHttpRequest();
  request.addEventListener("load", function() {
    console.log(this.responseText);
    let json_response = JSON.parse(this.responseText);
    for (let i = 0; i < json_response.length; i++)
    {
      if ("inspector" in json_response[i])
      {
        for (let j = 0; j < json_response[i].inspector.length; j++)
        {
          inspector_array.push(json_response[i].inspector[j]);
        }
        console.log(inspector_array);
        openInspectorPopup();
      }
    }
  });
  request.open("GET", "http://localhost:8000/events/decision")
  request.send()
});
