$(document).ready(function () {
  // Initial fetching and updating of worklogs
  fetchAndUpdateWorklogs();

  // Handle form submission for adding a new worklog
  $('.new-worklog').submit(function (e) {
    e.preventDefault();
    const form = $(this);
    const formData = form.serialize();
    $.post('/worklogs', formData)
      .done(function (_) {
        // Fetch and update worklogs after adding a new one
        fetchAndUpdateWorklogs();
        // Clear form input after successful submission
        form.trigger('reset');
      })
      .fail(function (xhr, _, error) {
        if (xhr.status === 500) {
          console.error('Error adding new worklog: ' + JSON.stringify(error));
        }
      });
  });

  // Handle input change event for loading different templates
  $('input[name="item"]').change(function () {
    const selectedId = $(this).attr('id');
    let selectedNav;

    if (selectedId === 'filter-completed') {
      $('.header').text('Completed Worklogs'); // Change header
      $('.content-categories').hide(); // Hide categories section
      $('.add-worklog').hide(); // Hide form section
      $('.edit-form-container').hide(); // Hide worklog form section if displayed
      selectedNav = 'completed';
    } else if (selectedId === 'filter-all') {
      $('.header').text('All Worklogs'); // Change header
      $('.content-categories').hide(); // Hide categories section
      $('.add-worklog').hide(); // Hide form section
      $('.edit-form-container').hide(); // Hide worklog form section if displayed
      selectedNav = 'all';
    } else {
      $('.header').text('Worklogs'); // Change header
      $('.content-categories').show(); // Show categories section
      $('.add-worklog').show(); // Show form section
      $('.edit-form-container').hide(); // Hide worklog form section if displayed
      selectedNav = 'pending';
    }
    fetchAndUpdateWorklogs(selectedNav);
  });

  // Handle input change event for displaying/hiding the form section
  $('.content-categories input[name="nav"]').change(function () {
    const filterNav = $(this).attr('id');
    if (filterNav === 'nav-completed') {
      $('.add-worklog').hide();
    } else {
      $('.add-worklog').show();
    }
    // Fetch and update worklogs based on the selected input tag
    fetchAndUpdateWorklogs(filterNav);
  });
});

// Function to update worklogs dynamically
function updateWorklogs(data) {
  const workLogList = $('#worklogs-list');
  // Clear existing list items
  workLogList.empty();
  $.each(data, function (_, item) {
    const listItem = $('<li class="worklogs"></li>');
    listItem.attr('data-worklog-id', item._id);
    listItem.text(item.title);
    workLogList.append(listItem);
  });
}

// Function to fetch and update worklogs
function fetchAndUpdateWorklogs(nav = 'pending') {
  $.getJSON('/worklogs', function (data) {
    let filteredData;
    if (nav === 'completed') {
      // Filter completed worklogs
      filteredData = filterCompleted(data);
    } else if (nav === 'all') {
      // Return all worklogs
      filteredData = noFilter(data);
    } else {
      // Filter pending worklogs
      filteredData = filterPending(data);
    }
    // Sort filtered data
    sortUpdated(filteredData);
    // Update worklogs list with filtered and sorted data
    updateWorklogs(filteredData);

    $('.page-content').show();
    $('.worklog-info').hide();
  });
}

// Filter the data to include only items with status 'pending'
function filterPending(data) {
  return data.filter(function (item) {
    return item.status === 'pending';
  });
}

// Filter the data to include only items with status 'completed'
function filterCompleted(data) {
  return data.filter(function (item) {
    return item.status === 'completed';
  });
}

// Function to include all items without filtering
function noFilter(data) {
  return data;
}

// Sort the data based on the 'updated_at' field in descending order
function sortUpdated(data) {
  data.sort(function (a, b) {
    return new Date(b.updated_at) - new Date(a.updated_at);
  });
}
