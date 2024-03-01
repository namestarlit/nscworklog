$(document).ready(function () {
  // Attach click event listener to delete buttons
  $(".delete-btn").on("click", function () {
    // Retrieve the worklog ID from the data attribute
    const worklogId = $(this).closest(".worklog-info").data("worklog-id");

    // Send an AJAX request to delete the worklog
    $.ajax({
      url: `/worklogs/${worklogId}`, // Replace with your actual delete endpoint
      type: "DELETE"
    })
      .then(function (response) {
        console.log("Success", response);
        window.location.href = '/home';
      })
      .catch(function () {
        console.log("Error", response);
      })
  });
});

$(document).ready(function () {
  // Attach click event listener to delete buttons
  $(".delete-btn").on("click", function () {
    // Retrieve the worklog ID from the data attribute
    const worklogId = $(this).closest(".worklog-info").data("worklog-id");

    // Send an AJAX request to delete the worklog
    $.ajax({
      url: `/worklogs/${worklogId}`, // Replace with your actual delete endpoint
      type: "DELETE"
    })
      .then(function (response) {
        console.log("Success", response);
        window.location.href = '/home';
      })
      .catch(function () {
        console.log("Error", response);
      })
  });
});
