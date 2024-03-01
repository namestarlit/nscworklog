$(document).ready(function () {
  // Attach click event listener to edit button
  $(".edit-btn").on("click", function () {
    const worklogId = $(this).closest(".worklog-info").data("worklog-id");

    // Make an Ajax request to get the worklog details
    $.ajax({
      url: `/worklogs/${worklogId}/edit`, // Replace with your actual edit endpoint
      method: "GET",
      success: function (editFormHtml) {
        $(".edit-form-container").html(editFormHtml).slideDown();
        $(".worklog-info").fadeOut();
      },
      error: function (error) {
        console.error("Error fetching edit form:", error);
      }
    });
  });

  // Attach click event listener to delete buttons
  $(".delete-btn").on("click", function () {
    // Retrieve the worklog ID from the data attribute
    const worklogId = $(this).closest(".worklog-info").data("worklog-id");

    $.ajax({
      url: `/worklogs/${worklogId}`,
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

  // Handle form submission asynchronously
  $(document).on("submit", "#edit-worklog-form", function (event) {
    event.preventDefault();

    const formData = $(this).serialize();
    const worklogId = $(".worklog-info").data("worklog-id");

    $.ajax({
      url: `/worklogs/${worklogId}`,
      method: "POST",
      data: formData,
      success: function (updatedWorklog) {
        // Handle success (e.g., update UI, hide edit form)
        updateWorklogDetails(updatedWorklog);
        $(".edit-form-container").slideUp();
      },
      error: function (error) {
        console.error("Error updating worklog:", error);
      }
    });
  });
});

// Function to update worklog details dynamically
function updateWorklogDetails(worklog) {
  const worklogInfo = $(".worklog-info");
  const list = worklogInfo.find("dl");
  list.empty();

  // Populate worklog details dynamically
  list.append(`<dt>Title</dt><dd>${worklog.title}</dd>`);
  list.append(`<dt>Description</dt><dd>${worklog.description}</dd>`);
  // Add other worklog properties dynamically
  $.each(worklog.extras, function (_, item) {
    for (const [key, value] of Object.entries(item)) {
      list.append(`<dt>${key}</dt><dd>${value}</dd>`);
    }
  });
  worklogInfo.fadeIn();
}
