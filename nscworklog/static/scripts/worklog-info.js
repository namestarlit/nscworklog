$(document).ready(function () {
  let worklogId;
  const textarea = $('.edit-form-container').find('textarea.auto-size');

  $('#worklogs-list').on('click', '.worklogs', function () {
    worklogId = $(this).data('worklog-id');

    $.ajax({
      url: `/worklogs/${worklogId}`,
      type: 'GET',
    })
      .then(function (response) {
        updateWorklogDetails(response);

        $('.page-content').hide();
        $('.worklog-info').show();
      })
      .catch(function (error) {
        console.log('Error', error);
      })
  });

  $('.back-btn').on('click', function () {
    $('.worklogs-wrapper').show();
    $('.worklog-info').hide();
  });

  function updateWorklogDetails(worklog) {
    const worklogInfo = $('.worklog-info');
    worklogInfo.attr('data-worklog-id', worklog._id);
    const list = worklogInfo.find('dl');
    list.empty();

    list.append(`<dt>Title</dt><dd>${worklog.title}</dd>`);
    list.append(`<dt>Description</dt><dd>${worklog.description}</dd>`);
    $.each(worklog.extras, function (key, value) {
      list.append(`<dt>${key}</dt><dd>${value}</dd>`);
    });

    $('.worklog-info').show();

    worklogInfo.fadeIn();
  }

  function resizeTextarea() {
    const initialHeight = textarea.prop('scrollHeight');
    textarea.height(initialHeight + 2);
  }

  $('.worklog-info').on('click', '.edit-btn', function () {
    $.ajax({
      url: `/worklogs/${worklogId}/edit`,
      method: 'GET',
      success: function (editFormHtml) {
        console.log(editFormHtml);
        $('.edit-form-container').html(editFormHtml);
        resizeTextarea();
        textarea.on('input', function () {
          const currentHeight = textarea.height();
          const scrollHeight = textarea.prop('scrollHeight');

          if (scrollHeight > currentHeight) {
            textarea.height(scrollHeight + 2);
          }
        });
        $('.edit-form-container').show();
        $('.worklog-info').hide();
      },
      error: function (error) {
        console.error('Error fetching edit form:', error);
      }
    });
  });

  let counter = 0; // Counter to keep track of added extra fields

  $('.edit-form-container').on('click', '.add-extra', function () {
    event.preventDefault();

    // Create new label and input elements
    let newLabel1 = $(`<label for='key-${counter}'>Key:</label>`);
    let newInput1 = $(`<input type='text' name='key-${counter}' class='extra-key'>`);
    let newLabel2 = $(`<label for='value-${counter}'>Value:</label>`);
    let newInput2 = $(`<input type='text' name='value-${counter}' class='extra-value'>`);


    newLabel1.append('&nbsp;');
    newLabel2.append('&nbsp;');

    $('#input-div').append(newLabel1, newInput1, newLabel2, newInput2);

    counter++;
  });

  $(document).on('submit', '#edit-worklog-form', function (event) {
    event.preventDefault();

    const formData = $(this).serialize();
    const worklogId = $('.worklog-info').data('worklog-id');

    $.ajax({
      url: `/worklogs/${worklogId}`,
      method: 'POST',
      data: formData,
      success: function (updatedWorklog) {
        updateWorklogDetails(updatedWorklog);
        $('.edit-form-container').hide();
      },
      error: function (error) {
        console.error('Error updating worklog:', error);
      }
    });
  });

  $('.delete-btn').on('click', function () {
    const worklogId = $('.worklog-info').data('worklog-id');

    $.ajax({
      url: `/worklogs/${worklogId}`,
      type: 'DELETE'
    })
      .then(function (response) {
        console.log('Success', response);
        window.location.href = '/home';
      })
      .catch(function () {
        console.log('Error', response);
      })
  });
});
