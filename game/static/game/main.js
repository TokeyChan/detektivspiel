//-------------------- VARIABLES ------------------------

var img_ele = null,
    x_cursor = 0,
    y_cursor = 0,
    x_img_ele = 0,
    y_img_ele = 0;

var map = document.getElementById("map");
var item_popup_window = document.getElementById("item_popup");
var item_popup_close = document.getElementById("item_close");
var popup_button = document.getElementById("popup_button");

var insp_popup_window = document.getElementById("insp_popup");
var insp_popup_close = document.getElementById("insp_close");
var insp_title = document.getElementById("insp_title");
var insp_text = document.getElementById("insp_text");
var insp_button = document.getElementById("insp_button_input");
var insp_input = document.getElementById("insp_text_input");
var inspector_array = [];

var knife = document.getElementById("knife");
var phone = document.getElementById("phone");
var high_heels = document.getElementById("high_heels");

var phone_container = document.getElementById("phone_container");
var phone_close = document.getElementById("phone_close");

var bank = document.getElementById("bank");
var cafe = document.getElementById("cafe");
var park = document.getElementById("park");
var old_but_gold = document.getElementById("old_but_gold");
var twoinone = document.getElementById("twoinone");

var chats_container = document.getElementById("chats_container");
var chat_chooser = document.getElementById("chat_chooser");
var overview_iframe = document.getElementById("overview_iframe"); //löschen?
var overlay_iframe = document.getElementById("overlay_iframe");
var chats_img = document.getElementById("chats_img");
var back_chat = document.getElementById("back_chat");
var felix_chat = document.getElementById("felix_chat");
var sophia_chat = document.getElementById("sophia_chat");
var stripper_chat = document.getElementById("stripper_chat");
var julian_chat = document.getElementById("julian_chat");

var bars = document.getElementById("bars");

var submit = false;

window.onload = function() {
    if (overview_iframe != null) {
      let overview_img = overview_iframe.contentWindow.document.getElementsByTagName('img')[0];
      overview_img.style.width = "275px";
    }
};

//----------------- FUNCTIONS -------------------------
function start_drag() {
  img_ele = this;
  x_img_ele = x_cursor - img_ele.offsetLeft;
  y_img_ele = y_cursor - img_ele.offsetTop;
}

function stop_drag() {
  img_ele = null;
}

function while_drag() {
  x_cursor = window.event.clientX;
  y_cursor = window.event.clientY;
  if (img_ele !== null) {
    if (x_cursor - x_img_ele > -135 && x_cursor-x_img_ele < 5) //oder andersrum
    {
      img_ele.style.left = (x_cursor - x_img_ele) + 'px';
    }
    if (y_cursor - y_img_ele > -150 && y_cursor - y_img_ele < 4)
    img_ele.style.top = (y_cursor - y_img_ele) + 'px';
  }
}


function openItemPopup(name) {
  let request = new XMLHttpRequest();
  request.addEventListener("load", function() {
    let json_response = JSON.parse(this.responseText);
    console.log(json_response);
    if (!("error_message" in json_response))
    {
      document.getElementById("popup_title").innerHTML = json_response['name'];
      document.getElementById("popup_text").innerHTML = json_response['desc_text'];
      document.getElementById("popup_" + name).style.display = "block";
      if ('exam_text' in json_response)
      {
        document.getElementById("popup_text").innerHTML += "<br><br>" + json_response['exam_text'];
      }
      if ('button' in json_response) {
        if ('button_id' in json_response) {
          popup_button.dataset.id = json_response['button_id'];
        } else {
          popup_button.dataset.id = null;
        }
        popup_button.value = json_response['button'];
        popup_button.style.display = "block";
        popup_button.dataset.item_name = json_response['name'];
      }
      item_popup_window.style.display = "block";
    }
  });
  request.open("GET", "http://localhost:8000/items/" + name)
  request.send()
}

function openInspectorPopup() {
  console.log(inspector_array);
  if (inspector_array.length == 0)
    return;
  insp_title.innerHTML = inspector_array[0].title;
  insp_text.innerHTML = inspector_array[0].text;
  insp_popup_window.style.display = "block";

  if (inspector_array[0].button) {
    insp_button_input.value = inspector_array[0].value;
    insp_button_input.style.display = "block";
  }
  else {
    insp_button_input.value = "";
    insp_button_input.style.display = "none";
  }
  if (inspector_array[0].input) {
    insp_text_input.style.display = "block";
    insp_text_input.dataset.submitid = inspector_array[0].submitid;
    submit = true;
  } else {
    insp_text_input.style.display = "none";
    //insp_text_input.dataset.submitid = "";
  }

  if (submit) {
    console.log(insp_button_input);
    insp_button_input.addEventListener("click", function() { insp_submit();});
  } else {
    insp_button_input.onclick = null;
  }
  inspector_array.shift();
}

function insp_submit() {
  if (submit) {
    let request = new XMLHttpRequest();
    request.open("GET", "http://localhost:8000/submit/" + insp_text_input.dataset.submitid + "/" + insp_text_input.value.replace(" ", "_"));
    request.send();
    submit = false;
  }
}

function send_item(name) {
  let request = new XMLHttpRequest();
  request.addEventListener("load", function() {
    let json_response = JSON.parse(this.responseText);
    console.log(json_response);
    if (!(json_response['status'] == 'OKAY')) {
      send_item(name);
    } else {
      popup_button.value = "Wurde ins Labor geschickt";
      popup_button.disabled = true;
    }
  });
  request.open("GET", "http://localhost:8000/items/send/" + name)
  request.send()
}

function show_chat(name) {
  chat_chooser.style.display = "none";
  chats_img.src = "/static/game/images/" + name + "_chat.png";
  chats_container.style.display = "block";
  overlay_iframe.src = "/static/game/images/" + name + "_overlay.png"

  overlay_iframe.onload = function() {
    overlay_document = overlay_iframe.contentWindow.document;
    let overlay_img = overlay_document.getElementsByTagName('img')[0];
    overlay_img.style.width = "275px";
  };

  overlay_iframe.style.display = "block";
  back_chat.style.display = "block";
  approve_chat(name);
}

function approve_chat(name)
{
  let request = new XMLHttpRequest();
  request.addEventListener("load", function() {

  });
  request.open("GET", "http://localhost:8000/chat/" + name)
  request.send()
}

// -------------------- EVENT LISTENERS ----------------------- //

item_popup_close.addEventListener("click", function() {
  item_popup_window.style.display = "none";
  document.getElementById("popup_knife").style.display = "none";
  document.getElementById("popup_high_heels").style.display = "none";
  document.getElementById("popup_phone").style.display = "none";
  popup_button.style.display = "none";
  popup_button.disabled = false;
});

insp_popup_close.addEventListener("click", function() {
  if (inspector_array.length == 0) {
    insp_popup_window.style.display = "none";
    if (phone_container != null) {
      phone_container.style.display = "none";
    }
  } else {
    openInspectorPopup();
  }
});

insp_button_input.addEventListener("click", function() {
  if (inspector_array.length == 0) {
    insp_popup_window.style.display = "none";
  } else {
    openInspectorPopup();
  }
});

popup_button.addEventListener("click", function() {
  if (this.dataset.item_name == "High Heels") {
    send_item("High_Heels");
  } else if (this.dataset.id == "chats_button") {
    phone_container.style.display = "block";
  } else {
    send_item(this.dataset.item_name);
  }

});

if (knife != null)
  knife.addEventListener("click", function() {openItemPopup("knife");});
if (phone != null)
  phone.addEventListener("click", function() {openItemPopup("phone");});
if (high_heels != null)
  high_heels.addEventListener("click", function() {openItemPopup("high_heels");});

var places = [bank, cafe, park, old_but_gold, twoinone];



for (let i = 0; i < places.length; i++)
{
  if (places[i] != null)
  {
    let submitter = document.getElementById("go_to_" + places[i].id);
    places[i].addEventListener("click", function() {
      submitter.click();
    });
  }
}

if (phone_close != null) {
  phone_close.addEventListener("click", function() {
    phone_container.style.display = "none";
  });
  felix_chat.addEventListener("click", function() {show_chat("felix");});
  stripper_chat.addEventListener("click", function() {show_chat("stripper");});
  julian_chat.addEventListener("click", function() {show_chat("julian");});
  sophia_chat.addEventListener("click", function() {show_chat("sophia");});
  back_chat.addEventListener("click", function() {
    chats_container.style.display = "none";
    overlay_iframe.style.display = "none";
    back_chat.style.display = "none";
    chat_chooser.style.display = "block";
  });
}

bars.addEventListener("click", function() {
  let decide_submit = document.getElementById("decide_submit");
  if (decide_submit != null) {
    decide_submit.click();
  } else {
    inspector_array.push({'title':'Warte, warte!', 'text':'Halte ein! Glaubst du wirklich wir sind schon soweit um jemanden festzunehmen? Da merkt man ja doch, wie unerfahren du noch bist... <br> Wir sollten noch viel mehr in Erfahrung bringen, bevor wir anfangen hier irgendjemanden zu verhaften!'});
    openInspectorPopup();
  }
});

map.setAttribute("draggable", false);
map.addEventListener('mousedown', start_drag);
map.addEventListener('mousemove', while_drag);
map.addEventListener('mouseup', stop_drag);

// ----------------------------- ON LOAD ------------------------

window.addEventListener("load", function() {
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
        openInspectorPopup();
      }
    }
  });
  request.open("GET", "http://localhost:8000/events/main")
  request.send()
});
