$(document).ready(function () {
  // Function to load HTML templates into the worklogs block section
  function loadWorklogsTemplate(templateName) {
    $.ajax({
      url: "../templates/" + templateName,
      dataType: "html",
      success: function (data) {
        $(".worklogs").html(data); // Load the HTML template into the worklogs block section
      },
      error: function (_, _, error) {
        console.error("Error loading template: " + error);
      }
    });
  }

  // Default template to load when index.html is rendered
  loadWorklogsTemplate("pending-worklogs.html");

  // Handle input change event for loading different templates
  $("input[name='item']").change(function () {
    const selectedId = $(this).attr("id");
    switch (selectedId) {
      case "filter-worklogs":
        loadWorklogsTemplate("pending-worklogs.html");
        break;
      case "filter-completed":
        loadWorklogsTemplate("completed-worklogs.html");
        break;
      case "filter-all":
        loadWorklogsTemplate("all-worklogs.html");
        break;
      default:
        console.error("Invalid input ID");
        break;
    }
  });
});
