$(document).ready(function () {
  // Initial fetching and updating of worklogs
  fetchAndUpdateWorklogs();

  // Handle form submission for adding a new worklog
  $(".new-worklog").submit(function (e) {
    e.preventDefault();
    const form = $(this);
    const formData = form.serialize();
    $.post("/add_worklog", formData)
      .done(function (_) {
        // Fetch and update worklogs after adding a new one
        fetchAndUpdateWorklogs();
        // Clear form input after successful submission
        form.trigger("reset");
      })
      .fail(function (xhr, _, error) {
        if (xhr.status === 500) {
          console.error('Error adding new worklog: ' + JSON.stringify(error));
        }
      });
  });
});

// Function to update worklogs dynamically
function updateWorklogs(data) {
  const workLogList = $("#worklogs-list");
  // Clear existing list items
  workLogList.empty();
  $.each(data, function (_, item) {
    const listItem = $("<li class='worklogs'></li>");
    const link = $("<a></a>").attr("href", "worklogs/" + item._id).text(item.title);
    listItem.append(link);
    workLogList.append(listItem);
  });
}

// Function to fetch and update worklogs
function fetchAndUpdateWorklogs() {
  $.getJSON("/worklogs", function (data) {
    // Filter pending worklogs
    const filteredData = filterPending(data);
    // Sort filtered data
    sortUpdated(filteredData);
    // Update worklogs list with filtered and sorted data
    updateWorklogs(filteredData);
  });
}

// Filter the data to include only items with status "pending"
function filterPending(data) {
  return data.filter(function (item) {
    return item.status === "pending";
  });
}

// Filter the data to include only items with status "completed"
function filterCompleted(data) {
  return data.filter(function (item) {
    return item.status === "completed";
  });
}

// Sort the data based on the "updated_at" field in descending order
function sortUpdated(data) {
  data.sort(function (a, b) {
    return new Date(b.updated_at) - new Date(a.updated_at);
  });
}
