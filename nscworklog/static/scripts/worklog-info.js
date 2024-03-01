$(document).ready(function () {
  let worklogId;

  // Attach click event listener to worklogs list (delegated to its parent)
  $("#worklogs-list").on("click", ".worklogs", function () {
    worklogId = $(this).data("worklog-id");

    // send GET request to /worklogs/worklogID to get the worklog object
    $.ajax({
      url: `/worklogs/${worklogId}`,
      type: 'GET',
    })
      .then(function (response) {
        updateWorklogDetails(response);

        // Hide the worklog list and show the detailed view
        $(".page-content").hide();
        $(".worklog-info").show();
      })
      .catch(function (error) {
        console.log("Error", error);
      })
  });

  // Attach click event listener to go back button in the detailed view
  $(".go-back-btn").on("click", function () {
    // Show the worklog list and hide the detailed view
    $(".worklogs-wrapper").show();
    $(".worklog-info").hide();
  });

  // Function to update worklog details dynamically
  function updateWorklogDetails(worklog) {
    const worklogInfo = $(".worklog-info");
    worklogInfo.attr("data-worklog-id", worklog._id);
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

    // Show the button container once the script is loaded
    $(".worklog-info").show();

    worklogInfo.fadeIn();
  }

  // Attach click event listener to edit button
  $(".edit-btn").on("click", function () {
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

  // Handle form submission asynchronously
  $(document).on("submit", "#edit-worklog-form", function (event) {
    event.preventDefault();

    const formData = $(this).serialize();
    const worklogId = $(".worklog-info").data("worklog-id");

    $.ajax({
      url: `/worklogs/${worklogId}`, // Replace with your actual update endpoint
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

  // Attach click event listener to delee button
  $(".delete-btn").on("click", function () {
    // Retrive the worklogId from the data attribute
    const worklogId = $(".worklog-info").data("worklog-id");

    // send DELETE request to /worklogs/worklogId
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
});
