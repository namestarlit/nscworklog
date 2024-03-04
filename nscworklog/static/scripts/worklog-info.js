$(document).ready(function () {
  let worklogId;
  const textarea = $('.edit-form-container').find('textarea.auto-size');

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
  $(".back-btn").on("click", function () {
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
    $.each(worklog.extras, function (key, value) {
      list.append(`<dt>${key}</dt><dd>${value}</dd>`);
    });

    // Show the button container once the script is loaded
    $(".worklog-info").show();

    worklogInfo.fadeIn();
  }

  // Function to resize the textarea based on content with an adjustment
  function resizeTextarea() {
    const initialHeight = textarea.prop('scrollHeight');
    textarea.height(initialHeight + 2); // Adjust for potential border/padding
  }

  // Attach click event listener to edit button
  $(".worklog-info").on("click", ".edit-btn", function () {
    // Make an Ajax request to get the worklog details
    $.ajax({
      url: `/worklogs/${worklogId}/edit`,
      method: "GET",
      success: function (editFormHtml) {
        console.log(editFormHtml);
        $(".edit-form-container").html(editFormHtml); // Populate form
        // Call resize function on initial load (after content is populated)
        resizeTextarea();
        // Attach event listener for input changes (user typing or pasting)
        textarea.on('input', function () {
          const currentHeight = textarea.height();
          const scrollHeight = textarea.prop('scrollHeight');

          // Only resize if content exceeds current height (avoids unnecessary adjustments)
          if (scrollHeight > currentHeight) {
            textarea.height(scrollHeight + 2); // Adjust for potential border/padding
          }
        });
        $(".edit-form-container").show();
        $(".worklog-info").hide();
      },
      error: function (error) {
        console.error("Error fetching edit form:", error);
      }
    });
  });

  // Add functionality to the "Add extra" button
  $('.add-extra').on("click", function () {
    // Create new label and input elements
    let newLabel1 = $('<label for="extra-key">Key:</label>');
    let newInput1 = $('<input type="text" name="extra-key" class="extra-key">');
    let newLabel2 = $('<label for="extra-value">Value:</label>');
    let newInput2 = $('<input type="text" name="extra-value" class="extra-value">');

    // Add a space between labels and inputs
    newLabel1.append('&nbsp;');
    newLabel2.append('&nbsp;');

    // Add a container for the labels and inputs
    $(".edit-form-container .extra-container").append(newLabel1, newInput1, newLabel2, newInput2);
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

  // Attach click event listener to delete button
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
