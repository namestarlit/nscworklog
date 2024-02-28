$(document).ready(function () {
  $(".worklogs").click(function() {
    const worklog_id = $(this).attr("id");
    $.getJSON("/worklog_info", )
  });
});

document.getElementById('add-extras').addEventListener('click', function () {
  var extrasDiv = document.getElementById('extras');
  var newEntry = document.createElement('div');
  newEntry.className = 'extras-entry';
  newEntry.innerHTML = `
      {{ form.extras.label }} 
      <div>{{ form.extras[0].key(size=20) }}</div>
      <div>{{ form.extras[0].value(size=20) }}</div>
  `;
  extrasDiv.appendChild(newEntry);
});
