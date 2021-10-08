// ---------------------------- vars --------------------------------//
var map = document.getElementById("map");
map.addEventListener("click", function() {
  document.getElementById("back_to_map").click();
});

var left_dimmer = document.getElementById("dimmer_left");
var right_dimmer = document.getElementById("dimmer_right");
var whole_dimmer = document.getElementById("dimmer_whole");

var background_dimmer = document.getElementById("background-dimmer");

var question_container = document.getElementById("question-container");
var video_container = document.getElementById("video-container");

var video_player = document.getElementById("video");
var video_dimmer = document.getElementById("video-dimmer");

var insp_popup_window = document.getElementById("insp_popup");
var insp_popup_close = document.getElementById("insp_close");
var insp_title = document.getElementById("insp_title");
var insp_text = document.getElementById("insp_text");
var insp_text_input = document.getElementById("insp_text_input");
var insp_button_input = document.getElementById("insp_button_input");
var inspector_array = [];


var question_transforms = [
  "",
  "translate(212px, 279px)",
  "translate(212px, 351px)",
  "translate(212px, 423px)",
  "translate(212px, 496px)",
  "translate(212px, 568px)"
]

var interrupt_active = false;
//insp_popup_window.style.display = "block";

// --------------------------- functions --------------------------------//


function ask_question(questionnr)
{
  hide_dimmer();
  hide_questions();
  let request = new XMLHttpRequest();
  request.addEventListener("load", function() {
    let json_response = JSON.parse(this.responseText);
    handle_server_response(json_response);
  });
  request.open("GET", "http://localhost:8000/questions/" + questionnr) //POST ?
  request.send()
}

function get_questions(personid)
{
  let request = new XMLHttpRequest();
  request.addEventListener("load", function() {
    let json_response = JSON.parse(this.responseText);
    handle_server_response(json_response);
  });
  request.open("GET", "http://localhost:8000/questions/person/" + personid)
  request.send()
}

function handle_server_response(response)
{
  console.log(response);
  switch (response['type'])
  {
    case "BEGINNING":
      show_frame();
      hide_questions();
      hide_dimmer();
      if ('INTERRUPT' in response)
        add_interrupt(response['INTERRUPT']);
      play_video(response['video_title'], personid=response['person'], questions=null, beginning=true);
      break;

    case "QUESTIONS":
      if (response['questions'].length == 0) {
        let insp = {
          'title': "Fertig",
          'text':"Ich fürchte diese Person hat uns zimindest im Moment nichts mehr zu erzählen..."
        };
        inspector_array.push(insp);
        openInspectorPopup();
        return;
      }

      add_questions(response['questions']);
      show_dimmer();
      show_frame();
      break;

    case "VIDEO":
      show_frame();
      if ('INTERRUPT' in response)
        add_interrupt(response['INTERRUPT']);
      if (response['follow_up'].length > 0)
        play_video(response['video_title'], personid=null, questions=response['follow_up']);
      else
        play_video(response['video_title'], personid=response['person']);
      hide_questions();
      break;

    case "FORBIDDEN":
      let insp = {
        'title':'Genug',
        'text':"Ich glaube wir haben für jetzt einmal genügend Fragen gestellt. Lass uns lieber später wiederkommen und stattdessen jemand anderes befragen!"
      };
      inspector_array.push(insp);
      openInspectorPopup();
      break;

    case "INSPECTOR":
      inspector_array.push(response['insp']);
      openInspectorPopup();
      break;

  }
}

function play_video(video_title, personid=null, questions=null, beginning=false)
{
  let source = document.createElement("source");
  source.setAttribute('src', '/static/game/videos/' + video_title.charAt(0) + '/' + video_title);
  source.setAttribute('type', 'video/mp4');
  video.appendChild(source);
  video.load();
  video.play();


  video.onended = function() {
    check_events();
    video.removeChild(source);
    if (personid != null) {
      get_questions(personid);
      show_dimmer();
    } else if (questions != null && questions.length > 0){
      add_questions(questions);
      show_dimmer();
    }
  };

  if (beginning)
    confirm_beginning(personid);
}

function add_interrupt(interrupt)
{
  interrupt_active = true;
  inspector_array.push(interrupt['inspector']);
  video.addEventListener("timeupdate", function() {
    let current_time = video.currentTime;
    if (current_time > interrupt['stop_time'] && current_time < interrupt['stop_time'] + 0.5 && inspector_array.length > 0)
    {
      video.pause();
      openInspectorPopup(interrupting=true);
      video.currentTime = interrupt['resume_time'];
      //video.removeEventListener("timeupdate", add_interrupt);
    }
  });
}



function confirm_beginning(personid)
{
  var request = new XMLHttpRequest();
  request.addEventListener("load", function() {
    let json_response = JSON.parse(this.responseText);
    if (json_response['status'] != 'OKAY')
    {
      confirm_beginning(personid);
    }
  });
  request.open("GET", "http://localhost:8000/questions/confirm/" + personid)
  request.send()
}


//---------------------------- HTML STUFF -----------------------------

function hide_frame()
{
  video_container.style.zIndex = 1;
  video_container.style.display = "none";
}

function show_frame()
{
  video_container.style.zIndex = 25;
  video_container.style.display = "block";
}

function show_dimmer()
{
  video_dimmer.style.display = "block";
}

function hide_dimmer()
{
  video_dimmer.style.display = "none";
}

function add_questions(question_list)
{
  let nodes = Array.from(question_container.childNodes)
  for (let i = 0; i < nodes.length; i++)
  {
    if (nodes[i].nodeType == 1) //if is div
    {
      question_container.removeChild(nodes[i]);
    }
  }

  for (let i = 0; i < question_list.length; i++)
  {
    let question_div = document.createElement("div");
    if (i == 0) {
      question_div.id = "first_question";
    } else {
      question_div.classList.add("question");
    }
    question_div.dataset.questionid = question_list[i]['id'];
    question_div.style.transform = question_transforms[i];

    let question_span = document.createElement("span");
    question_span.innerHTML = question_list[i]['text'];
    if (question_list[i]['text'].length > 60) {
      question_div.style.lineHeight = "30px";
    }


    question_div.appendChild(question_span);

    question_container.appendChild(question_div);
  }

  let question_one = document.getElementById("first_question");
  let questions = Array.from(document.getElementsByClassName("question"));
  questions.unshift(question_one);

  for(let i = 0; i < questions.length; i++)
  {
    questions[i].addEventListener("click", function() {
      ask_question(questions[i].dataset.questionid);
      //hide_frame();
    });
  }
  question_container.style.display = "block";
}

function hide_questions()
{
  question_container.style.display = "none";
}

function openInspectorPopup(interrupting=false) {
    console.log(inspector_array);
    let submit = false;
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
      insp_text_input.dataset.submitid = "";
    }

    inspector_array.shift();

    if (interrupting) {
      insp_button_input.addEventListener("click", function() {play()});
      insp_close.addEventListener("click", function() {play()});
    } else {
      insp_button_input.removeEventListener("click", play);
      insp_close.removeEventListener("click", play);
    }
    if (submit) {
      insp_button_input.onclick = function() {insp_submit();};
    } else {
      insp_button_input.onclick = null;
    }
}

function insp_submit() {
  let request = new XMLHttpRequest();
  request.addEventListener("load", function() {
    handle_server_response(JSON.parse(this.responseText));
  });
  request.open("GET", "http://localhost:8000/submit/" + insp_text_input.dataset.submitid + "/" + insp_text_input.value.replace(" ", ""));
  request.send();
}

function play() {
  if (interrupt_active) {
    video.play();
    interrupt_active = false;
  }
}

// --------------------------- event-listeners --------------------------------//

background_dimmer.addEventListener("click", function() {
  hide_frame();
  video.pause();
  let video_nodes = video.childNodes;
  for (let i = 0; i < video_nodes.length; i++)
  {
    video.removeChild(video_nodes[i]);
  }
});

if (left_dimmer != null)
{
  left_dimmer.addEventListener("click", function(e) {
    //show_frame();
    get_questions(this.dataset.personid);
  });
}
if (right_dimmer != null)
{
  right_dimmer.addEventListener("click", function() {
    //show_frame();
    get_questions(this.dataset.personid);
  });
} else if (whole_dimmer != null) {
  whole_dimmer.addEventListener("click", function() {
    //show_frame();
    get_questions(this.dataset.personid);
  });
}

insp_popup_close.addEventListener("click", function() {
  if (inspector_array.length == 0) {
    insp_popup_window.style.display = "none";
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

// ----------------------------- ON LOAD ------------------------

var place_name = window.location.pathname.split('/')[window.location.pathname.split('/').length - 2];

window.addEventListener("load", function() {
  check_events();
});

function check_events()
{
  console.log("CHECK EVENTS");
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
  request.open("GET", "http://localhost:8000/events/" + place_name)
  request.send()
}
